import hashlib
import os
import uuid
import io
import sys
import inspect
from urllib.parse import urlparse

class ValidationReport:
    """This class is a simple object wrapper for the pyshacl.validate() return value
    """
    def __init__(self, conforms, report, message):
        """
        Args:
            conforms (bool): Boolean flag indicating a simple pass/fail for SHACL validation
            report (rdflib.Graph): An rdflib.Graph representation of the SHACL validation results
            message (str): A text description of the SHACL validation results
        """
        self.conforms = conforms
        self.report = report
        self.message = message

def default():
    return 'default.html'

def get_file_resource_path(file_name, root_dir=os.path.dirname(__file__), prefix="", stem_dir="data"):
    resource_dir = f"{root_dir}/{stem_dir}"
    fully_qualified_path = f"{prefix}{resource_dir}/{file_name}"
    return fully_qualified_path

def generate_node_id(seed: str = None):
    """Generates a globally unique uuid, typically used in creating a unique IRI for a node to be stored in the knowledge graph.
    """
    if seed is not None:
        md5 = hashlib.md5()
        md5.update(seed.encode('utf-8'))
        return str(uuid.UUID(hex=md5.hexdigest(), version=4))
    else:
        return str(uuid.uuid4())

def generate_placeholder():
    placeholder_value = "{{%s}}" % generate_node_id()
    return placeholder_value

def generate_placeholder_triple():
    placeholder_value = f"{generate_node_id()} {generate_node_id()} {generate_node_id()}"
    return placeholder_value
    
def is_placeholder(string):
    return isinstance(string, str) and string.startswith("{{") and string.endswith("}}")

def generate_default_field_input():
    return { 'title': "", 'labels': [], 'value': generate_placeholder(), 'is_link': False, 'is_required': True }

def get_root_namespace():
    return "https://ncei.noaa.gov/vaip"

def get_pattern_namespace():
    return f"{get_root_namespace()}/pattern"

def get_storage_pattern_namespace():
    return f"{get_pattern_namespace()}/storage"

def get_aiu_pattern_namespace():
    return f"{get_storage_pattern_namespace()}/aiu"

def get_individual_aiu_pattern_namespace(pattern_id: str):
    return f"{get_aiu_pattern_namespace()}/{pattern_id}"

def get_aic_pattern_namespace():
    return f"{get_storage_pattern_namespace()}/aic"

def get_individual_aic_pattern_namespace(id: str):
    return f"{get_aic_pattern_namespace()}/{id}"

def get_aic_member_description_pattern_namespace(aic_id: str):
    return f"{get_individual_aic_pattern_namespace(aic_id)}/member_descriptions"

def get_dip_pattern_namespace():
    return f"{get_storage_pattern_namespace()}/dip"

def get_individual_dip_pattern_namespace(pattern_id: str):
    return f"{get_dip_pattern_namespace()}/{pattern_id}"

def get_process_pattern_namespace():
    return f"{get_pattern_namespace()}/process"

def get_individual_process_pattern_namespace(pattern_id: str):
    return f"{get_process_pattern_namespace()}{pattern_id}"

def get_task_pattern_namespace():
    return f"{get_pattern_namespace()}/task"

def get_individual_task_pattern_namespace(pattern_id: str):
    return f"{get_task_pattern_namespace()}{pattern_id}"

def get_ubl_pattern_namespace():
    return f"{get_pattern_namespace()}/ubl"

def get_individual_ubl_pattern_namespace(pattern_id: str):
    return f"{get_ubl_pattern_namespace()}{pattern_id}"

def get_field_map_pattern_namespace():
    return f"{get_pattern_namespace()}/field_map"
    
def get_session_pattern_namespace():
    return f"{get_pattern_namespace()}/session"

def get_request_pattern_namespace():
    return f"{get_pattern_namespace()}/request"
    
def get_response_pattern_namespace():
    return f"{get_pattern_namespace()}/response"

def get_template_namespace():
    return f"{get_root_namespace()}/template"

def get_storage_template_namespace():
    return f"{get_template_namespace()}/storage"

def get_aiu_template_namespace():
    return f"{get_storage_template_namespace()}/aiu"

def get_individual_aiu_template_namespace(template_id: str):
    return f"{get_aiu_template_namespace()}/{template_id}"

def get_aic_template_namespace():
    return f"{get_storage_template_namespace()}/aic"

def get_individual_aic_template_namespace(id: str):
    return f"{get_aic_template_namespace()}/{id}"

def get_aic_member_description_template_namespace(aic_id: str):
    return f"{get_individual_aic_template_namespace(aic_id)}/member_descriptions"

def get_dip_template_namespace():
    return f"{get_storage_template_namespace()}/dip"

def get_individual_dip_template_namespace(template_id: str):
    return f"{get_dip_template_namespace()}/{template_id}"

def get_process_template_namespace():
    return f"{get_template_namespace()}/process"

def get_individual_process_template_namespace(template_id: str):
    return f"{get_process_template_namespace()}{template_id}"

def get_task_template_namespace():
    return f"{get_template_namespace()}/task"

def get_individual_task_template_namespace(template_id: str):
    return f"{get_task_template_namespace()}{template_id}"

def get_ubl_template_namespace():
    return f"{get_template_namespace()}/ubl"

def get_individual_ubl_template_namespace(template_id: str):
    return f"{get_ubl_template_namespace()}{template_id}"

def get_field_map_template_namespace():
    return f"{get_template_namespace()}/field_map"
    
def get_session_template_namespace():
    return f"{get_template_namespace()}/session"
    
def get_request_template_namespace():
    return f"{get_template_namespace()}/request"
    
def get_response_template_namespace():
    return f"{get_template_namespace()}/response"

def get_record_namespace():
    return f"{get_root_namespace()}/record"

def get_storage_record_namespace():
    return f"{get_record_namespace()}/storage"

def get_aiu_record_namespace():
    return f"{get_storage_record_namespace()}/aiu"

def get_individual_aiu_record_namespace(record_id: str):
    return f"{get_aiu_record_namespace()}/{record_id}"

def get_aic_record_namespace():
    return f"{get_storage_record_namespace()}/aic"

def get_individual_aic_record_namespace(id: str):
    return f"{get_aic_record_namespace()}/{id}"

def get_aic_member_description_record_namespace(aic_id: str):
    return f"{get_individual_aic_record_namespace(aic_id)}/member_descriptions"

def get_aic_member_record_namespace(aic_id: str):
    return f"{get_individual_aic_record_namespace(aic_id)}/members"

def get_dip_record_namespace():
    return f"{get_storage_record_namespace()}/dip"

def get_individual_dip_record_namespace(record_id: str):
    return f"{get_dip_record_namespace()}/{record_id}"
    
def get_session_record_namespace():
    return f"{get_record_namespace()}/session"
    
def get_request_record_namespace():
    return f"{get_record_namespace()}/request"
    
def get_response_record_namespace():
    return f"{get_record_namespace()}/response"

def get_dynamic_namespace(resource):
    return resource.namespace.ontology.get_namespace(f"{resource.iri}/")

def get_iri(resource):
    return resource.iri

def get_core_ontology_file_string(onto_file: str ="vaip-core.owl"):
    return get_file_resource_path(onto_file, prefix="file://")

def get_framework_ontology_file_string(onto_file: str ="vaip-framework.owl"):
    return get_file_resource_path(onto_file, prefix="file://")

def get_skos_ontology_file_string(onto_file: str ="skos-core.owl"):
    return get_file_resource_path(onto_file, prefix="file://")
    
def load_combined_Onto(shapes_file_name="vaip-coreCombined.owl"):
    """
    Returns the combinined core and framework ontonolgies as one file for pyshacl validation.
    """
    shapes_file_path = get_file_resource_path(shapes_file_name, stem_dir="data")
    if os.path.isfile(shapes_file_path):
        shapes_file = open(shapes_file_path, "r")
        shapes_string = shapes_file.read()
        shapes_file.close()
        return shapes_string
    else:
        return None

def load_core_shacl(shapes_file_name="vaip_core_shapes.shacl"):
    """
    Returns the core shacl file for vaip shapes into memory (currently just aiu pattern).
    """
    shapes_file_path = get_file_resource_path(shapes_file_name, stem_dir="data/shacl")
    if os.path.isfile(shapes_file_path):
        shapes_file = open(shapes_file_path, "r")
        shapes_string = shapes_file.read()
        shapes_file.close()
        return shapes_string
    else:
        return None

def order_ancestors(focus, unordered, ordered=[]):
    for ancestor in unordered:
        if ancestor in focus.is_a:
            ordered.append(ancestor)
            unordered.remove(ancestor)
            order_ancestors(ancestor, unordered, ordered)
    return ordered

def get_ordered_ancestors(concept, limit:int):
    focus = concept.node.is_a[0]
    unordered_ancestors = list(focus.ancestors())
    unordered_ancestors.remove(focus)
    ordered_ancestors = order_ancestors(focus, unordered_ancestors, [focus])
    if limit:
        try:
            return ordered_ancestors[0:limit+1]
        except:
            return ordered_ancestors
    return ordered_ancestors

def get_ancestor_definitions(concept, limit=None):
    definition_string=""
    ancestors = get_ordered_ancestors(concept, limit)
    for ancestor in ancestors:
        try:
            definition_string+=f"{ancestor.label[0]}(ancestor {ancestors.index(ancestor)}): {ancestor.definition[0]}\n\n"
        except:
            pass
    return definition_string

def get_ancestor_examples(concept, limit=None):
    example_string=""
    ancestors = get_ordered_ancestors(concept, limit)
    for ancestor in ancestors:
        try:
            example_string+=f"{ancestor.label[0]}(ancestor {ancestors.index(ancestor)}): {ancestor.example[0]}\n\n"
        except:
            pass
    return example_string

def get_properties(resource):
    """Prints all vAIP ontology properties of a given VaipResource instance

    Args:
        resource (VaipResource): The VaipResource to print properties from
    """
    for prop in resource.node.get_properties():
        for value in prop[resource.node]:
            try:
                print(type(value).namespace)
            except:
                pass

def serialize_ontology(ontology, format="rdfxml", to_str=True, qualified_save_path="serialized_graph.owl"):
    if to_str:
        graph_file = io.BytesIO()
    else:
        graph_file = get_file_resource_path(qualified_save_path)
    ontology.save(file = graph_file, format = format)
    if to_str:
        rdf_string = (graph_file.getvalue().decode("utf-8"))
        graph_file.close()
        return rdf_string
    return None

def serialize_world(ontology, format="rdfxml", to_str=True, qualified_save_path="serialized_world_graph.owl"):
    if to_str:
        graph_file = io.BytesIO()
    else:
        graph_file = get_file_resource_path(qualified_save_path)
    ontology.world.save(file = graph_file, format = format)
    if to_str:
        rdf_string = (graph_file.getvalue().decode("utf-8"))
        graph_file.close()
        return rdf_string
    return None

def cast_data_node(value, clazz, prop):
    if prop == 'hasLink':
        data_title = 'Link'
    else:
        data_title = 'Value'
    return {'id': value, 'title': data_title, 'labels': [value], 'properties': {}, 'class':clazz}

def add_vis_node(node, vis_network):
    colors = {"blue" : "#623CEA", "yellow" : "#F7EC59", "red" : "#EF233C", "cyan" : "#61F2C2", "green":"#009933", "orange":"#ff9900", "purple":"#9966ff", "pink":"#ff66cc"}
    shapes = {"blue" : "square", "yellow" : "box", "red" : "triangle", "cyan" : "dot", "cyan" : "diamond", "green":"star", "orange":"triangleDown", "red":"elipse", "pink":"star", "purple":"hexagon"}
    
    hash_value = hash(node['class'])
    color_index = hash_value % len(colors)

    color_key = list(colors.keys())[color_index]
    vis_network.add_node(str(node['id']), label=node['title'], title=build_title(node), shape=shapes[color_key], color=colors[color_key]) #Color & Shape of nodes

    

def add_vis_edge(source, target, label, vis_network):
    vis_network.add_edge(source['id'], target['id'], label=label)

def parse_vis_tree(branch, vis_network, root=True, parent=None, label=None):
    add_vis_node(branch, vis_network)
    if not root:
        add_vis_edge(vis_network.get_node(str(parent['id'])), vis_network.get_node(str(branch['id'])), label, vis_network)
    if branch['properties']:
        for prop_name in branch['properties'].keys():
            for val in branch['properties'][prop_name]:
                parse_vis_tree(val, vis_network, root=False, parent=branch, label=prop_name)

def cast_data_node(value, clazz, prop):
    if prop == 'hasLink':
        data_title = 'Link'
    else:
        data_title = 'Value'
    return {'id': value, 'title': data_title, 'labels': [value], 'properties': {}, 'class':clazz}

def node_tree(node, prop=None, clazz=None, ontologies=[], visited_nodes=None):
    node_branch = {'id': None, 'title': '', 'labels': [], 'properties': {}, 'class':''}
    try:
        node_branch['id'] = node
        node_branch['title'] = node.prefLabel[0]       
        node_branch['labels'] = node.altLabel
        #node_branch['class'] = node.is_a[0].label[0], Removed for combination of core and framework in class
        for subClass in node.is_a :
           node_branch['class'] += f"{subClass.label[0]},"
        
        node_branch['class'] = node_branch['class'].rstrip(",") 
        visited_nodes.add(node)
    except:
        return cast_data_node(node, clazz, prop)
    for node_property in node.get_properties(): #iterate over the node properties (relationships where node is domain)
        if node_property.namespace.ontology in ontologies:
            target_branches = []
            for target in node_property[node]:
                #We cannot restrict edges(relationships) based on if a node is visted or not, only the adding of the node itself.
                if target not in visited_nodes :
                    if len((node.is_a[0].label)) == 0:
                        print(node.is_a[0])
                    if len((node_property.label)) == 0:
                        print(node_property)
                    target_branches.append(node_tree(target, prop=node_property.label[0], clazz=node.is_a[0].label[0], ontologies=ontologies, visited_nodes=visited_nodes))
                else:
                   #This handles branches that intertwine, such as addsMeaningTo relationship betwen semantic and structural representation
                   target_branches.append(node_tree(target, prop=node_property.label[0], clazz=node.is_a[0].label[0], ontologies=ontologies))
                node_branch['properties'][node_property.label[0]] = target_branches
    return node_branch

def build_title(node):
    title=f'Type: {node["class"]}'
    nl = "\n"
    if node['labels']:
        title = f'{title}\nAlternate Labels:\n'
        for label in node['labels']:
            if isinstance(label, str) :
               title += label
            elif isinstance(label, bool) :
               title += str(label)
            elif isinstance(label, int) :
               title += str(label)
            else:
                title += label._name # Node Case
        #title = f'{title}\nAlternate Labels:\n{nl.join(node["labels"])}' # Cant use this because some labels may not be strings
    return title

# These are the subset of all vAIP API classes that are stored as individual named graphs
# and thus need to be loaded on-demand in the load() function defined in this module
ROOT_CLASS_NAMES = [
    "IdentityStoragePattern", "IdentityStorageTemplate", "IdentityStorageRecord",
    "TransformationStoragePattern", "TransformationStorageTemplate", "TransformationStorageRecord",
    "MemberDescriptionPattern", "MemberDescriptionTemplate", "MemberDescriptionRecord",
    "OutputStoragePattern", "OutputStorageTemplate", "OutputStorageRecord",
    "ProcessPattern", "ProcessTemplate", "ProcessRecord",
    "SessionPattern", "SessionTemplate", "SessionRecord",
    "RequestPattern", "RequestTemplate", "RequestRecord",
    "ResponsePattern", "ResponseTemplate", "ResponseRecord"
]
"""The Root VAIP Class Object Types that are available to be loaded.
"""

def inspect_root_classes(class_object):
    """Verify that that the provided class object is a valid VAIP class object Type.
    Valid Types are in ROOT_CLASS_NAMES.

    Args:
        class_object (class): The class object to inspect.

    Returns:
        bool: If class_object is a class and in ROOT_CLASS_NAMES, returns true, else false.
    """
    return inspect.isclass(class_object) and class_object.__name__ in ROOT_CLASS_NAMES

def load(session, iri, as_copy=True):
    """ Load an existing graph into the ontology session. 
    
    Agrs:
        session(Session): The desired Session.
        iri(str): The iri of the graph to load.
        as_copy(bool): If true, makes a copy of the graph with a new iri. If False, uses the original iri.
    """
    g = session.load_named_graph(iri)
    res = g.query(f"""
    SELECT ?type
    WHERE {{
        <{iri}> rdf:type ?type
    }}
    """)
    fmk_type = None
    vaip_type = None
    for r in res:
        if str(r.type).startswith("http://ncei.noaa.gov/vaip/ontologies/vaip-framework#"):
            fmk_type = urlparse(str(r.type)).fragment
        elif str(r.type).startswith("https://ncei.noaa.gov/vaip/ontologies/vaip-core#"):
            vaip_type = urlparse(str(r.type)).fragment
    
    if not fmk_type or not vaip_type:
        raise Exception(f"Unable to load <{iri}>. SPARQL query did not return an rdf:type.")
    
    CLASS_DICT = dict(inspect.getmembers(sys.modules["vaip.ontology"], inspect_root_classes))
    api_class = CLASS_DICT[fmk_type]
    node_id = None if as_copy else iri.rsplit("/", 1)[1]
    # g.serialize(destination=get_file_resource_path(f"{iri.rsplit('/', 1)[1]}.xml"), format="xml")
    instance = api_class.from_rdf(session, g, iri, vaip_type, node_id)
    return instance