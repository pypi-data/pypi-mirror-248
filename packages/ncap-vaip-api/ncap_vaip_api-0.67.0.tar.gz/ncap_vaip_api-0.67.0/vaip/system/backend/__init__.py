from .deploy_agents import SPARQLEndpointAgent
from .trigger_agents import AWSEventBridgeTriggerAgent
from .neptune import NeptuneClient
import os


def sparql_host():
    return os.environ.get("SPARQL_HOST", "localhost")


def sparql_port():
    return os.environ.get("SPARQL_PORT", "8182")


def create_default_agents():
    host = sparql_host()
    port = sparql_port()
    backend = SPARQLEndpointAgent(host, port)
    return set([backend])


def create_default_trigger_agent():
    agent = AWSEventBridgeTriggerAgent()
    return agent


def create_default_query_client():
    client = NeptuneClient(sparql_host(), sparql_port())
    return client
