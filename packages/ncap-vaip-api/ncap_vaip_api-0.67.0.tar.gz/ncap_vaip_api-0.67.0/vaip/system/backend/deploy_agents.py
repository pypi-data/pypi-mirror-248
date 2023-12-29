import typing
import boto3
from os import path
from urllib.parse import urlparse
from .neptune import NeptuneClient


class DeployAgent:
    def deploy(self, resource: "InformationPackage"):
        pass


class SPARQLEndpointAgent(DeployAgent):
    def __init__(self, host: str, port: typing.Union[str, int]):
        self.host = host
        self.port = port
        self.endpoint = f"{host}:{port}"

    def deploy(
        self, resource: "InformationPackage"
    ) -> typing.Dict[typing.Any, typing.Any]:
        named_graph = resource.node.iri
        client = NeptuneClient(self.endpoint, self.port)
        ## IMPORTANT: This drop_graph call is only temporarily in place until the archive workflows support automatic versioning
        client.drop_graph(named_graph)
        rdf = resource.serialize(format="ntriples")
        insert = f"""
        INSERT DATA {{
            GRAPH <{named_graph}> {{
                {rdf}
            }}
        }}
        """
        update = client.update(insert)
        return update["content"]


class S3BucketAgent(DeployAgent):
    def __init__(self, bucket: str, key_prefix: typing.Union[str, None] = None):
        self.bucket = bucket
        self.key_prefix = key_prefix

    def deploy(self, resource: "InformationPackage"):
        s3 = boto3.client("s3")
        content = resource.serialize(format="ntriples")
        object_url = urlparse(resource.node.iri)
        object_path = f"{object_url.path}.nt"
        key = path.join(self.key_prefix, object_path).lstrip("/")
        return s3.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=content.encode("utf-8"),
            StorageClass="STANDARD",
        )


class AWSEventBridgeAgent(DeployAgent):
    def __init__(self, bus_name: str = "default"):
        self.bus_name = bus_name

    def deploy(
        self, resource: "InformationPackage"
    ) -> typing.Dict[typing.Any, typing.Any]:
        eb = boto3.client("events")
        detail = "foo"
        entry = {
            "Detail": detail,
            "DetailType": "vAIP API EventBridge Agent",
            "Source": "api.vaip.system.backend.deploy_agents.AWSEventBridgeAgent",
            "EventBusName": self.bus_name,
        }
        return eb.put_events(Entries=[entry])
