#Using owlready2 to load the core ontology in-memory and then automatically generate Python classes for constructing RDF triples
from owlready2 import World # type: ignore  # pylint: disable=E0401
from . import utils
import typing
from rdflib import Graph
from .system.patterns import task, pattern_metadata, process, aic, session
from .system.backend import create_default_agents, create_default_trigger_agent, create_default_query_client
from .system.backend.deploy_agents import DeployAgent

class Session:
    def __init__(self,
                 from_file=True,
                 core_file_path=utils.get_core_ontology_file_string(),
                 framework_file_path=utils.get_framework_ontology_file_string(),
                 skos_file_path=utils.get_skos_ontology_file_string(),
                 core_onto_iri="https://ncei.noaa.gov/vaip/ontologies/vaip-core#",
                 framework_onto_iri="https://ncei.noaa.gov/vaip/ontologies/vaip-framework#",
                 skos_onto_iri="http://www.w3.org/2004/02/skos/core#",
                 deploy_agents: typing.Set[DeployAgent] = None,
                 query_client = None
                ):
        self.token = f"token-{utils.generate_node_id()}"
        self.context = self._build_context()
        self.deploy_agents = deploy_agents if deploy_agents else create_default_agents()
        self.query_client = query_client if query_client else create_default_query_client()
        self.trigger_agent = create_default_trigger_agent()
        
        if from_file:
            self.core_ontology = self.context.get_ontology(f"{core_file_path}").load()
            self.framework_ontology = self.context.get_ontology(f"{framework_file_path}").load()
            self.skos_ontology = self.context.get_ontology(f"{skos_file_path}").load()
        else:
            self.core_ontology = self.context.get_ontology(f"{core_onto_iri}").load()
            self.framework_ontology = self.context.get_ontology(f"{framework_onto_iri}").load()
            self.skos_ontology = self.context.get_ontology(f"{skos_onto_iri}").load()
        
        self.patterns = {}
        
    def _build_context(self):
        return World()
        
    def load_named_graph(self, iri):
        g = Graph()
        client = self.query_client
        rdf = client.construct_named_graph(iri)
        if len(rdf) == 0:
            raise Exception(f"Unable to load <{iri}>. Provided IRI does not exist in configured graph backend.")
        
        g.parse(data=rdf, format="nt")
        return g

    def _load_system_pattern(self, pattern_key):
        """This function shall load baseline system patterns. In future implementations, this will likely transition
        to a workflow-based deployment
        """
        pmap = dict([
            ('process', process.create_process_pattern),
            ('aiu_task', task.create_aiu_task_pattern),
            ('aic_task', task.create_aic_task_pattern),
            ('dip_task', task.create_dip_task_pattern),
            ('ubl', task.create_ubl_pattern),
            ('field_map', task.create_field_map_pattern),
            ('aic', aic.create_aic_pattern),
            ('session', session.create_session_pattern),
            ('request', session.create_request_pattern),
            ('response', session.create_response_pattern)
        ])
        pattern = pmap[pattern_key](self)
        self.patterns[pattern_key] = pattern
        return self.patterns[pattern_key]

    def get_system_pattern(self, pattern_key: str):
        if pattern_key not in self.patterns:
            self._load_system_pattern(pattern_key)
        return self.patterns[pattern_key]

    def deploy(self, resource):
        response_map = {}
        for agent in self.deploy_agents:
            res = agent.deploy(resource)
            response_map[str(agent)] = res
        return response_map
    
    def trigger_process(self,
                        iri: typing.Union[str, None] = None,
                        process: typing.Union[None, 'ProcessTemplate'] = None,
                        payload: typing.Union[typing.Dict[typing.Any, typing.Any], None] = None):
        if iri is None and process is None:
            print("trigger_process must be called with either an IRI string or a ProcessTemplate instance")
            return None
        if iri is not None and process is not None:
            print("trigger_process cannot be called with both an IRI string and a ProcessTemplate instance")
            return None
            
        if isinstance(iri, str):
            process = utils.load(self, iri, as_copy=False)
        else:
            iri = process.node.iri
        operating_mode = "STANDARD" if process.aiu_task.long_running else "EXPRESS"
        
        trigger_response = self.trigger_agent.trigger(iri=iri, operating_mode=operating_mode, payload=payload)
        # 1. Generate required InputFields of the ProcessTemplate
        # 2. Validate the provided payload contains all required input values for the ProcessTemplate
        # 3. Create a SessionRecord
        # 4. Create a RequestRecord
        #   a. Create a FieldMap in this record containing the payload-provided field values mapped to required InputFields
        #   b. Add bi-directional link with SessionRecord
        
        # Iteration 2 of this story:
        #   Implement event loop functions to monitor SNS topic:
        #       - Filter all SNS messages related to the current Session/Request
        #       - Create ResponseRecords from each SNS message
        #           - Add links across all 3 Session/Request/Response
        return trigger_response

    def create_empty_ontology(self, ontology_root="https://ncei.noaa.gov/vaip/patterns/", ontology_stem=""):
        """
        Given an ontology root and an ontology stem, open a clean ontology in Session's context at the specified path.
        Do not enforce a join character for the two ontology strings, allow for use of # or / (or other) delimiters.
        ontology_path = f"{ontology_root}{ontology_stem}"
        empty_ontology = world.get_ontology(ontology_path)
        return empty_ontology
        """
        return self.context.get_ontology(f"{ontology_root}{ontology_stem}")