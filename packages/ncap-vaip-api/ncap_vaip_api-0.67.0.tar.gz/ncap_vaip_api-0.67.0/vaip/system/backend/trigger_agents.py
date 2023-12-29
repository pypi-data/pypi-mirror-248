import boto3
import typing
import json

class TriggerAgent:
    def trigger(self, iri: str, payload: typing.Union[typing.Dict[typing.Any, typing.Any], None]):
        pass

class AWSEventBridgeTriggerAgent(TriggerAgent):
    def __init__(self, environment_id: str = "archive-main", workflow_id: str = "AIU Workflow", bus_name: str = 'default'):
        self.bus_name = bus_name
        self.environment_id = environment_id
        self.workflow_id = workflow_id

    def trigger(self, iri: str = None, operating_mode: str = None, payload: typing.Dict[typing.Any, typing.Any] = {}):
        eb = boto3.client("events")
        detail = json.dumps({
            'workflow_id': self.workflow_id,
            'environment': self.environment_id,
            'process': iri,
            "operating_mode": operating_mode,
            "input": payload
        })
        entry = {
            "Detail": detail,
            "DetailType": "Workflow Trigger Message",
            "Source": "api.vaip.system.backend.trigger_agents.AWSEventBridgetriggerAgent",
            "EventBusName": self.bus_name
        }
        return eb.put_events(Entries=[entry])