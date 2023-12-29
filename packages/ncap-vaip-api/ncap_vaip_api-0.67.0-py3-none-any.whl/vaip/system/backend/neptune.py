import requests
import logging
import boto3
import os
import re
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
from types import SimpleNamespace
from time import sleep
from io import BytesIO
from rdflib.query import Result
from yurl import URL
from vaip.system.backend.utilities import get_logger
from redis import RedisCluster

log = get_logger()
logging.getLogger("urllib3").setLevel(log.getEffectiveLevel())

# NOTE: urllib3 is a dependency for the requests library, so we should be guaranteed to have it available
# Use a custom HTTPAdapter that is set to retry only when we recieve a HTTP 104 status error response ("Connection reset by peer")
# More error codes can be added here, but the default requests behavior is to not retry on anything
# TODO: This retry setting appears to have no effect at all. DEBUG messages have not shown any retries coming from urllib3, so more investigation is needed
# retry = urllib3.Retry(read=4, backoff_factor=0.2, status_forcelist=[104])
retry_adapter = requests.adapters.HTTPAdapter(max_retries=0)


class NeptuneClient:
    def __init__(
        self,
        neptune_endpoint,
        neptune_port=None,
        access_key=None,
        secret_key=None,
        session_token=None,
        region=None,
        profile=None,
        redis_host=None,
        redis_port=None,
        redis_key_expiry=None,
    ):
        url = URL(neptune_endpoint)
        if not url.scheme:
            url = url.replace(scheme="https")
        if neptune_port:
            url = url.replace(port=neptune_port)
        if not url.port:
            url = url.replace(port=8182)
        self.endpoint = str(url)
        self.session = requests.Session()
        self.session.mount(self.endpoint, retry_adapter)
        if (
            access_key is None
            or secret_key is None
            or session_token is None
            or region is None
        ):
            access_key = os.getenv("AWS_ACCESS_KEY_ID")
            secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
            region = os.getenv("AWS_REGION")
            session_token = os.getenv("AWS_SESSION_TOKEN")
            if (
                access_key is not None
                and secret_key is not None
                and session_token is not None
                and region is not None
            ):
                self.aws_credentials = SimpleNamespace(
                    access_key=access_key,
                    secret_key=secret_key,
                    token=session_token,
                    region=region,
                )
                self.aws_auth = SigV4Auth(self.aws_credentials, "neptune-db", region)
            else:
                if profile is None:
                    profile = os.getenv("AWS_PROFILE", "default")
                    if profile is None:
                        raise Exception(
                            """AWS_PROFILE was not provided to NeptuneClient.
                        Provide an AWS profile name with either the `profile` parameter or an environment variable named `AWS_PROFILE`."""
                        )

                session = boto3.Session(profile_name=profile)
                region = session.region_name
                self.aws_credentials = session.get_credentials()
                self.aws_auth = SigV4Auth(self.aws_credentials, "neptune-db", region)
        else:
            self.aws_credentials = SimpleNamespace(
                access_key=access_key,
                secret_key=secret_key,
                token=session_token,
                region=region,
            )
            self.aws_auth = SigV4Auth(self.aws_credentials, "neptune-db", region)

        if redis_host:
            self.redis = RedisCluster(host=redis_host, port=redis_port)
            self.redis_key_expiry = redis_key_expiry
        else:
            self.redis = None
            self.redis_key_expiry = None

    def _get_signed_aws_headers(self, url, data):
        aws_request = AWSRequest(method="POST", url=url, data=data)
        self.aws_auth.add_auth(aws_request)
        return aws_request.headers

    def _send_post(
        self,
        query,
        query_type="query",
        headers={"Accept": "application/sparql-results+json"},
    ):
        url = f"{self.endpoint}/sparql"
        data = {query_type: query}
        headers = {**headers, **self._get_signed_aws_headers(url, data)}
        try:
            log.debug("NeptuneClient sending POST request")
            r = self.session.post(url, data=data, headers=headers)
            return r
        except requests.ConnectionError as err:
            self.session = requests.Session()
            self.session.mount(self.endpoint, retry_adapter)
            sleep(0.2)  # TODO: see comment above about retries
            r = self.session.post(url, data=data, headers=headers)
            log.error("NeptuneClient caught ConnectionError when attempting POST query")
            return r

    def _send_load(self, s3uri, iamRole):
        data = {
            "source": s3uri,
            "format": "nquads",
            "iamRoleArn": iamRole,
            "region": "us-east-1",
            "failOnError": "TRUE",
            "parallelism": "MEDIUM",
            "updateSingleCardinalityProperties": "FALSE",
            "queueRequest": "TRUE",
            "dependencies": [],
        }
        url = f"{self.endpoint}/loader"
        headers = {
            "Accept": "application/json",
            **self._get_signed_aws_headers(url, data),
        }
        try:
            log.debug("NeptuneClient sending Loader request")
            r = self.session.post(url, data=data, headers=headers)
            return r
        except requests.ConnectionError as err:
            log.error("NeptuneClient caught ConnectionError when attempting POST query")
            return r

    def _handle_neptune_response(self, response):
        log.debug(response.headers.get("content-type"))
        if response.headers.get("content-type") == "application/json":
            json = response.json()
            if "code" in json and "detailedMessage" in json:
                raise Exception(f'{json["code"]}: "{json["detailedMessage"]}"')

    def query(self, query):
        content = None
        status_code = None
        if self.redis is not None:
            content = self.redis.get(query)

        if content is None:
            r = self._send_post(
                query, "query", headers={"Accept": "application/sparql-results+json"}
            )

            if r.status_code == 200 and self.redis is not None:
                log.debug("Not in Cache")
                self.redis.set(query, r.content, ex=self.redis_key_expiry)
            else:
                self._handle_neptune_response(r)
            content = r.content
            status_code = r.status_code
        else:
            status_code = 200

        return {
            "code": status_code,
            "content": Result.parse(BytesIO(content), format="json"),
        }

    def update(self, statement):
        r = self._send_post(statement, "update", headers={"Accept": "application/json"})
        self._handle_neptune_response(r)
        return {"code": r.status_code, "content": r.json()}

    def load(self, s3uri, iamRole):
        r = self._send_load(s3uri, iamRole)
        self._handle_neptune_response(r)

        return {"code": r.status_code, "content": r.json()}

    def create_graph(self, graph_name):
        update = f"CREATE GRAPH <{graph_name}>"
        return self.update(update)

    def drop_graph(self, graph_name):
        update = f"DROP GRAPH <{graph_name}>"
        return self.update(update)

    def insert_rdf(self, graph_name, rdf):
        subgraph = f"GRAPH <{graph_name}> {{ {rdf} }} "
        update = f"INSERT DATA {{ {subgraph} }}"
        return self.update(update)

    def convert_to_nquads(self, graph_name, rdf):
        nquads = ""
        lines = rdf.split("\n")
        for ln in lines:
            if ln != "" and not ln.isspace():
                nq = f"{ln[:-1]} <{graph_name}> .\n"
                nquads = nquads + nq
        return nquads

    def retrieve_named_graph(self, graph_name):
        sparql = f"""
            SELECT ?s ?p ?o
            FROM <{graph_name}>
            WHERE {{
                ?s ?p ?o
            }}
            """
        return self.query(sparql)

    def construct_named_graph(self, graph_name):
        sparql = f"""
        CONSTRUCT {{ ?s ?p ?o }}
        WHERE {{
            GRAPH <{graph_name}>
            {{ ?s ?p ?o }}
        }}
        """
        r = self._send_post(
            sparql, "query", headers={"Accept": "application/n-triples"}
        )
        content = r.content
        return content
