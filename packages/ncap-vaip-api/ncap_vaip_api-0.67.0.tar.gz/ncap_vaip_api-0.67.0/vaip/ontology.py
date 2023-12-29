from __future__ import annotations
import re # !Must Be first, allows ciclial type hints for fields, helping users in the long run.
import owlready2 # type: ignore  # pylint: disable=E0401
import pyshacl
from . import utils
from . import sparql_utils
from pyvis import network as vis
import typing
import types
from caseconverter import snakecase
from rfc3987 import match
from .system.backend.neptune import NeptuneClient
import os
from rdflib import Graph

class VaipResource:
    """The base class for all VAIP classes. Includes basic functions to set common properties among all entity types.
    """
    def __init__(self, session, node_id: str = None):
        self.session = session
        self.node_id = node_id if node_id is not None else utils.generate_node_id()
        self.node = None
        self.namespace = None

    def destroy(self, cascade = True):
        """Destroys the VAIP resource in the owlready2 ontology. This is overridden and then called by classes that extend VaipReource. 
        """
        owlready2.destroy_entity(self.node)

    def relationships(self):
        """Prints all vAIP ontology properties of a given VaipResource instance 
        """
        return utils.get_properties(self)

    def definition(self, ancestors=False, limit=None):
        """Returns the definition of a vaip resource(node).

        Args:
            ancestors (bool, optional): If set toTrue, returns the node and it's ancestors up to the limit if set. If False, returns the primary label and definition of the node. Defaults to False.
            limit (int, optional): Limit defines the maximum depth to produce for the list of ancestors. Defaults to None.

        Returns:
            str: The definition of a vaip resource and or it's ancestors.
        """
        if ancestors:
            return utils.get_ancestor_definitions(self, limit=limit)
        else:
            return f"{self.node.is_a[0].label[0]}: {self.node.is_a[0].definition[0]}" 

    def example(self, ancestors=False, limit=None):
        """Gets the example string of a vaip resource(node).

        Args:
            ancestors (bool, optional): If True, returns ancestor examples as well. If False, returns just the example for the vaip resource. Defaults to False.
            limit (_type_, optional): The depth to return for ancestor examples. Defaults to None.

        Returns:
            str: The example of a vaip resource and ancestor examples if applicable.
        """
        if ancestors:
            return utils.get_ancestor_examples(self, limit=limit)
        else:
            return f"{self.node.is_a[0].label[0]}: {self.node.is_a[0].example[0]}"

    def set_title(self, title: str) -> str:
        """Set the title of a vaip resource(node).

        Args:
            title (str): Value to set the title of a vaip resouce to.

        Returns:
            str: Returns the new current value of the vaip resource title.
        """
        self.node.prefLabel = title
        return self.node.prefLabel[0]

    def set_labels(self, labels: 'list[str]') -> 'list[str]':
        """Sets the array of alternate labels for a vaip resource(node). Existing alternate labels are removed.

        Args:
            labels (list[str]): The list of alternate labels to set for the vaip resource

        Returns:
            list[str]: Returns the new current list of alternal labels.
        """
        self.node.altLabel = list(set(labels))
        return self.node.altLabel

    def add_label(self, label: str) -> 'list[str]':
        """Adds a new alternate label to the vaip resource.

        Args:
            label (str): The label value to append to eexisting alternate labels.

        Returns:
            list[str]: The updated list of alternate labels.
        """
        self.node.altLabel.append(label)
        self.node.altLabel = list(set(self.node.altLabel))
        return self.node.altLabel
        
    def remove_label(self, label: str) -> 'list[str]':
        """Removes an existing alternate label from the existing list if it exists.

        Args:
            label (str): The label value to remove from the list.

        Returns:
            list[str]: The update list of alternate labels.
        """
        if label in self.node.altLabel:
            self.node.altLabel.remove(label)
        return self.node.altLabel
    #This could use a better name as it doesn't actually validate uniqueness, but compares for a match.
    def validate_uniqueness(self, input_title: str, input_labels: 'list[str]') -> bool:
        """Validates whether the combination of title and labels matches for this vaip resource.

        Args:
            input_title (str): The title to compare against the vaip resource.
            input_labels (list[str]): The list of labels to compare against the vaip resource. 

        Returns:
            bool: True if titile and labels match, otherwise False.
        """
        if self.get_title() == input_title and self.get_labels() == input_labels:
            return False
        return True

    def get_title(self) -> str:
        """Get the current title of the vaip resource.

        Returns:
            str: The current title of the vaip resource.
        """
        return self.node.prefLabel[0]
    
    def get_labels(self) -> 'list[str]':
        """Get the current list of alternate labels for the vaip resource.

        Returns:
            list[str]: The current list for the vaip resource.
        """
        return self.node.altLabel

    def serialize(self, format="rdfxml", to_str=True, qualified_save_path="serialized_graph.owl"):
        """
        Serializes an in-memory owlready2 graph that is held as an ontology. Defaults to rdfxml format and returning 
        the serialized graph as in-memory string. String can be chained into other pipelines as needed (i.e. to a rdflib.Graph)
        Alternatively, can provide a file to save the serialization to.
        Allowed serializations by this method are currently only rdfxml, ntriples, nquads (limited by owlready2 support).
        """
        return utils.serialize_ontology(self.namespace.ontology, format=format, to_str=to_str, qualified_save_path=qualified_save_path)
    
    def validate(self):
        #data = self.serialize()
        #self.serialize(to_str=False)
        data = utils.serialize_world(self.namespace.ontology,  format="rdfxml", to_str=True, qualified_save_path="serialized_world_graph.owl")
        #Debug
        #utils.serialize_world(self.namespace.ontology,  format="rdfxml", to_str=False, qualified_save_path="serialized_world_graph.owl")

        #onto_core = utils.serialize_ontology(self.session.core_ontology)
        #onto_framework = utils.serialize_ontology(self.session.framework_ontology)
        onto_core = utils.load_combined_Onto()
        shacl = utils.load_core_shacl()
        #,do_owl_imports=True
        #print(f"\n###################################################################\n{data}\n###################################################################\n")
        conforms, results_graph, results_text = pyshacl.validate(data, ont_graph=onto_core, shacl_graph=shacl, shacl_format='n3')
        return utils.ValidationReport(conforms, results_graph, results_text)

    def visualize(self, notebook=True, filter_menu=True, hierarchical:bool=True, isCDNRemote:bool=True, height:str="750px"):
        """Creates the NetworkX network and styles it.
        Parameters:
        notebook (bool): Are you running in a Juypter Notebook? Yes if True.
        filter_menu (bool): Do you want the filter menu? Yes if True.
        hierarchical (bool): Display the graph in hierarchical mode? Yes if True.
        isCDNRemote (bool): Do you want the JS resources for pyVis to be remote? Yes if True. If notebook is True, isCDNRemote is also True. If False, JS files required by the visualization will be written locally.
        height (string): Height of the graph area. Can be a height in px, em, or percentage. Do not set to 100% if filter_menu is True as the menu may be unaccessable.
        """
        if notebook:
            vis_network = vis.Network(notebook=True, cdn_resources=True, filter_menu=filter_menu)
        else:
            isRemote="local"
            if(isCDNRemote):
                isRemote="remote"
            vis_network = vis.Network(height=height, filter_menu=filter_menu, cdn_resources=isRemote)
        if hierarchical:
            vis_network.set_options("""
            const options = {
                "layout": {
                    "hierarchical": {
                        "enabled": true,
                        "direction": "LR",
                        "sortMethod": "directed"
                        }
                    }
                }""")
        else:
            #vis_network.show_buttons() # do not turn this on without comment out below.
            vis_network.set_options("""
            const options = {
                "physics": {
                    "forceAtlas2Based": {
                    "springLength": 100
                    },
                    "minVelocity": 0.75,
                    "solver": "forceAtlas2Based"
                }
            }""")
        visited_nodes = set()
        root = utils.node_tree(self.node, ontologies=[self.session.core_ontology, self.session.framework_ontology], visited_nodes=visited_nodes)
        utils.parse_vis_tree(root, vis_network)
        
        return vis_network

class TFieldInput(typing.TypedDict):
    """The common data structure of all field types. 
    """
    title: str
    labels: list[str]
    value: str
    is_link: bool
    is_required: bool

class Field(VaipResource):
    """A Field Represents the value unit in the ontology. Fields hold values (or placeholders for values) that together with other qualifiers (like required, namespace, type, id) allow them to provide information to the user. In conjunction with the reference model structure that they are configured in, Fields provide a mechanism to convey information and knowledge to the (human or machine) consumer.
    """
    def __init__(self, parent, VaipClass, value = None, title: str = None, labels: list[str] = [], namespace: str = None, namespace_class: str = None, is_required: bool = True, node_id: str = None):
        """Initialize a Field. It is better to initialize one of the field types rather than this directly. Types: ObjectField, PropertyField, LiteralField, or StatementField

        Args:
            parent (VaipResource): The parent node for the field.
            VaipClass (_type_): The class of the field: ObjectField, PropertyField, LiteralField, or StatementField
            value (_type_, optional): The defualt value for the field.. Defaults to None.
            title (str, optional): The title of the field. Defaults to None.
            labels (list[str], optional): The list of alternate labels for the field. Defaults to [].
            namespace (str, optional): The namespace IRI for the field. Defaults to None. If None, the parent MemberDescription namespace is used.
            namespace_class (str, optional): The namespace class for the field. Defaults to None. If None, the title value is used.
            is_required (bool, optional): If the field is required to be matched to User Busines Logic (UBL) input and output. Defaults to True.
            node_id (str, optional): An optional identifier for the field. This becomes part of the IRI of the underlying owlready2 node. Defaults to None
        """
        self.parent: VaipResource = parent
        super().__init__(parent.session, node_id)
        self.namespace = utils.get_dynamic_namespace(parent.node)
        self.node = VaipClass(self.node_id, namespace=self.namespace)
        self.set_title(title)
        self.set_labels(labels)
        self.set_value(value)
        self.set_namespace(namespace or utils.get_iri(parent.node))       
        self.set_class(namespace_class or self.get_title())
        self.set_required(is_required)

    @classmethod
    def from_rdf(cls, parent, graph, root_iri: str, vaip_type: str, root_node_id: str):
        labels = []
        res = graph.query(f"""
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            SELECT ?label
            WHERE {{
                <{root_iri}> skos:altLabel ?label
            }}
        """)
        for r in res:
            labels.append(str(r))
        
        res = graph.query(f"""
            PREFIX fmk: <http://ncei.noaa.gov/vaip/ontologies/vaip-framework#>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            SELECT ?title ?value ?namespace ?field_class ?required
            WHERE {{
                <{root_iri}> skos:prefLabel ?title .
                <{root_iri}> fmk:hasValue ?value .
                <{root_iri}> fmk:hasNamespace ?namespace .
                <{root_iri}> fmk:hasClass ?field_class .
                OPTIONAL
                {{
                    <{root_iri}> fmk:isRequired ?required .
                }}
            }}
        """)
        for r in res:
            title = str(r.title)
            value = str(r.value)
            namespace = str(r.namespace)
            field_class = str(r.field_class)
            required = bool(r.required) if r.required is not None else None
        
        field = cls(parent, title, labels, value, namespace, field_class, required, root_node_id)
        return field
        
    def set_title(self, title: str):
        """Set the title of the Field

        Args:
            title (str)

        Returns:
            Field: Returns the current Field instance.
        """
        if title is not None:
            super().set_title(title)
            self.node.hasLabel = [title]
        return self
    
    def set_value(self, value):
        """Set the value of the Field

        Args:
            value (_type_) 

        Returns:
            Field: Returns the current Field instance.
        """
        if value is not None:
            self.value = value
            self.node.hasValue = [value]
            self.node.hasBits = [value]
        return self

    def set_namespace(self, field_namespace: str):
        """Sets the namespave IRI of the Field. Must meet the rfc3987 standard. https://datatracker.ietf.org/doc/html/rfc3987.
        If None, the node base IRI is used.

        Args:
            field_namespace (str)

        Raises:
            Exception: Returns "Invalid IRI provided for Namespace" if the provided IRI does not meet rfc3987.

        Returns:
            Field: Returns the current Field instance.
        """
        if field_namespace is not None:
            # Debug print(match(field_namespace, rule="IRI") )
            if(match(field_namespace, rule="IRI") == None):
                raise Exception(f"Invalid IRI provided for Namespace: {field_namespace}")
            self.field_namespace = field_namespace
            self.node.hasNamespace = [field_namespace]
        else:
            self.field_namespace = self.node.base_iri
            self.node.hasNamespace = [self.node.base_iri]
        return self

    def set_class(self, field_class: str):
        """Set the namespace class for the Field.

        Args:
            field_class (str)

        Returns:
            Field: Returns the current Field instance.
        """
        if field_class is not None:
            self.field_class = field_class
            self.node.hasClass = [str(field_class)]
        return self

    def set_required(self, required: bool):
        """Set if a Field is rrequired for User Business Logic Input and Output

        Args:
            required (bool)

        Returns:
            Field: Returns the current Field instance.
        """
        if required is not None:
            self.required = required
            self.node.isRequired = [required]
        return self

    def connect(self, target_field, title: str = None, labels: list[str] = [], namespace: str = None, namespace_class: str = None):
        """Connects the current Field with the target Field by creating a Statement Field and Property Field in the parent Member Description with the provided arguments. Note: The generated Property Field defaults to Required for UBL.

        Args:
            target_field (Field): The Field to connect the current Field to.
            title (str, optional): The title of the Property Field. Defaults to None.
            labels (list[str], optional): The labels to provide to the Property Field. Defaults to [].
            namespace (str, optional): The namspace to create the Property Field in. Defaults to None.
            namespace_class (str, optional): The namespace class for the Property Field. Defaults to the title value used.
        Returns:
            StatementField: The generated Statement Field.
        """
        statement = self.parent.connect(self, target_field, title, labels, namespace, namespace_class)
        return statement
    
    # TODO: Not sure if every type of Field is valid to "add" to all other types of Fields (eg. only objects should be able to `add_literal` ?)

    def add_object(self, title: str = None, labels: list[str] = [], namespace: str = None, namespace_class: str = None, is_required: bool = True, auto_generated: bool = None)->  ObjectField:
        """Add an Object Field as the sub-Field of the curent Field to the parent Member Description.

        Args:
            title (str, optional): Title of the Object Field. Defaults to None.
            labels (list[str], optional): The List of Alternate Labels for the Object Field. Defaults to [].
            namespace (str, optional): The namespace IRI for the Object Field. Defaults to the parent node's namespace.
            namespace_class (str, optional): The namespace class for the Object Field. Defaults to the title value used.
            is_required (bool, optional): If the Object Field is required for UBL. Defaults to True.
            auto_generated (bool, optional): If the Object Field was Autogenerated by the VAIP or not. Defaults to None.

        Returns:
            ObjectField: The new Object Field instance.
        """
        obj_field = self.parent.add_object(title, labels, namespace, namespace_class, is_required, auto_generated)
        setattr(self, obj_field.get_title(), obj_field)
        return obj_field

    def add_literal(self, title: str = None, labels: list[str] = [], namespace: str = None, namespace_class: str = None, is_required: bool = True) ->  LiteralField:
        """Adds a Literal Field as a sub-Field of the current Field instance. If the current parent MemberDescription does not have a "hasProperty" Property Field for the current Field instance, one is automatically generated.
        A Statement Field is generated between the current Field and the new Literal Field.

        Args:
            title (str, optional): Title of the Literal Field. Defaults to None.
            labels (list[str], optional): The List of Alternate Labels for the Literal Field. Defaults to [].
            namespace (str, optional): The namespace IRI for the Literal Field. Defaults to the parent node's namespace.
            namespace_class (str, optional): The namespace class for the Literal Field. Defaults to the title value used.
            is_required (bool, optional): If the Literal Field is required for UBL. Defaults to True.

        Returns:
            LiteralField: The new Literal Field
        """
        prop = self.parent._find_vaip_framework_property_field()
        literal = self.parent.add_literal(title, labels, namespace, namespace_class, is_required)
        setattr(self, literal.get_title(), literal)
        if prop is None:
            prop = self.parent.add_property(title="hasProperty", namespace=self.session.framework_ontology.base_iri, namespace_class="hasProperty")
        self.parent.add_statement(subject = self, predicate = prop, object = literal)
        return literal
    
    def add_property(self, title: str = None, labels: list[str] = [], namespace: str = None, namespace_class: str = None, is_required: bool = True) ->  PropertyField:
        """Add a Property Field as a sub-Field of the current Field instance.

        Args:
            title (str, optional): Title of the Property Field. Defaults to None.
            labels (list[str], optional): The List of Alternate Labels for the Property Field. Defaults to [].
            namespace (str, optional): The namespace IRI for the Property Field. Defaults to the parent node's namespace.
            namespace_class (str, optional): The namespace class for the Property Field. Defaults to the title value used.
            is_required (bool, optional): If the Property Field is required for UBL. Defaults to True.

        Returns:
            PropertyField: The new Propery Field.
        """
        prop = self.parent.add_property(title, labels, namespace, namespace_class, is_required)
        setattr(self, prop.get_title(), prop)
        return prop

class ObjectField(Field):
    """An Object Field represents an instance of a defined Class - this sets Object Fields apart from Literal Fields - whereas Literal Fields hold value, Object Fields hold instances. Object Fields may be leveraged with an autoGeneration capability within the Framework to cover &apos;blank node&apos; capabilities. They may stand alone or more typically be combined with other Field types (such as Property Fields and Literal Fields) within Statement Fields to provide rich relationship context.
    """
    @staticmethod
    def from_field(source: ObjectField, new_parent):
        """Copy and Object Field from an existing one to the new parent Field/Member Description. 

        Args:
            source (ObjectField): The Object Field to copy.
            new_parent (_type_): The Parent Field/MemberDescription

        Returns:
            ObjectField: The new ObjectField
        """
        # When copying with a new namespace, we need to check if the field_namespace is referencing the source field's parent MemberDescription (as a result of auto-promotion)
        copied_namespace = source.field_namespace if source.field_namespace != utils.get_iri(source.parent.node) else utils.get_iri(new_parent.node)
        copied_field = ObjectField(new_parent, source.get_title(), source.get_labels(), copied_namespace, source.field_class, source.required, source.auto_generated)
        return copied_field

    def __init__(self, parent, title: str = None, labels: list[str] = [], namespace: str = None, namespace_class: str = None, is_required: bool = True, auto_generated: bool = False, node_id: str = None):
        """Initialize a new Object Field.

        Args:
            parent (_type_): The Parent Field or MemberDescription
            title (str, optional): Title of the Object Field. Defaults to None.
            labels (list[str], optional): The List of Alternate Labels for the Object Field. Defaults to [].
            namespace (str, optional): The namespace IRI for the Object Field. Defaults to the parent node's namespace.
            namespace_class (str, optional): The namespace class for the Object Field. Defaults to the title value used.
            is_required (bool, optional): If the Object Field is required for UBL. Defaults to True.
            auto_generated (bool, optional): If the field is autogenerated. Defaults to False.
            node_id (str, optional): An optional identifier for the Object Field. This becomes part of the IRI of the underlying owlready2 node. Defaults to None.
        """
        super().__init__(parent, parent.session.core_ontology.DigitalObject, utils.generate_placeholder(), title, labels, namespace, namespace_class, is_required, node_id)
        self.node.is_a.append(parent.session.framework_ontology.ObjectField)
        self.set_auto_generated(auto_generated)

    def set_auto_generated(self, auto_generated):
        """Set Whether the Object Field was autogenerated or not.

        Args:
            auto_generated (bool): _description_

        Returns:
            ObjectField: The updated Object Field
        """
        if auto_generated is not None:
            self.auto_generated = auto_generated
            self.node.isAutoGenerated = [auto_generated]
        return self

class PropertyField(Field):
    """A Property Field represents a predicate statement about something. &apos;hasWeight&apos;, &apos;hasOwner&apos;, &apos;isA&apos;, are all examples of Property Fields. Property Fields may stand alone or more typically be combined with other fields in Statement Fields to provide rich relationship context.
    """
    @staticmethod
    def from_field(source: PropertyField, new_parent):
        """Copy an Property Field from an existing one to the new parent Field/Member Description. 

        Args:
            source (PropertyField): The Property Field to copy.
            new_parent (_type_): The target Parent Field/MemberDescription.

        Returns:
            PropertyField: The new PropertyField
        """
        # When copying with a new namespace, we need to check if the field_namespace is referencing the source field's parent MemberDescription (as a result of auto-promotion)
        copied_namespace = source.field_namespace if source.field_namespace != utils.get_iri(source.parent.node) else utils.get_iri(new_parent.node)
        copied_field = PropertyField(new_parent, source.get_title(), source.get_labels(), copied_namespace, source.field_class, source.required)
        return copied_field

    def __init__(self, parent, title: str = None, labels: list[str] = [], namespace: str = None, namespace_class: str = None, is_required: bool = True, node_id: str = None):
        """Initialize a new Property Field

        Args:
            parent (_type_): The Parent Field or MemberDescription
            title (str, optional): Title of the Property Field. Defaults to None.
            labels (list[str], optional): The List of Alternate Labels for the Property Field. Defaults to [].
            namespace (str, optional): The namespace IRI for the Property Field. Defaults to the parent node's namespace.
            namespace_class (str, optional): The namespace class for the Property Field. Defaults to the title value used.
            is_required (bool, optional): If the Property Field is required for UBL. Defaults to True.
            node_id (str, optional): An optional identifier for the Object Field. This becomes part of the IRI of the underlying owlready2 node. Defaults to None.
        """
        value = title # Properties are valued at pattern creation time
        super().__init__(parent, parent.session.core_ontology.DigitalObject, value, title, labels, namespace, namespace_class, is_required, node_id)
        self.node.is_a.append(parent.session.framework_ontology.PropertyField)

class LiteralField(Field):
    """A Literal Field holds a literal value such as a number, string, or IRI. Literal Fields may work alone or in conjunction with other Fields (such as Object or Property Fields within Statement Fields) to provide higher order context.
    """
    @staticmethod
    def from_field(source: LiteralField, new_parent):
        """Copy a Literal Field from an existing one to the new parent Field/Member Description. 

        Args:
            source (LiteralField): The Literal Field to copy.
            new_parent (_type_): The target Parent Field/MemberDescription

        Returns:
            LiteralField: The new LiteralField
        """
        copied_namespace = source.field_namespace if source.field_namespace != utils.get_iri(source.parent.node) else utils.get_iri(new_parent.node)
        copied_field = LiteralField(new_parent, source.get_title(), source.get_labels(), source.value, copied_namespace, source.field_class, source.required)
        return copied_field

    def __init__(self, parent, title: str = None, labels: list[str] = [], value: str = utils.generate_placeholder(), namespace: str = None, namespace_class: str = None, is_required: bool = True, node_id: str = None):
        """Initialize a new Literal Field

        Args:
            parent (_type_): The Parent Field or MemberDescription
            title (str, optional): Title of the Property Field. Defaults to None.
            labels (list[str], optional): The List of Alternate Labels for the Property Field. Defaults to [].
            value (str, optional): _description_. Defaults to a new UUID.
            namespace (str, optional): The namespace IRI for the Property Field. Defaults to the parent node's namespace.
            namespace_class (str, optional): The namespace class for the Property Field. Defaults to the title value used.
            is_required (bool, optional): If the Property Field is required for UBL. Defaults to True.
            node_id (str, optional): An optional identifier for the Literal Field. This becomes part of the IRI of the underlying owlready2 node. Defaults to None.
        """
        super().__init__(parent, parent.session.core_ontology.DigitalObject, value, title, labels, namespace, namespace_class, is_required, node_id)
        self.node.is_a.append(parent.session.framework_ontology.LiteralField)

class StatementField(Field):
    """A Statement Field is a &apos;derived&apos; Field and reprents a specific contextualization of other Fields (which may include other Statement Fields). Statement Fields provide the ability to hold relationships as data which in turn enables n-ary relationships of various types, contextual materialization, Statement reification, and sparql* behavior (weights applied to statements).
    """
    def __init__(self, parent, title: str = None, labels: list[str] = [], subject: Field = None, predicate: Field = None, object: Field = None, node_id: str = None):
        """Initialize a new Statemnt Field

        Args:
            parent (_type_): The Parent Field or MemberDescription
            title (str, optional): Title of the Statement Field. Defaults to a triple of the titles of the provided subject, predicate and object if all three are provided. Otherwise uses the provided title. Ex: "subjectTitle predicateTitle objectTitle".
            labels (list[str], optional): The List of Alternate Labels for the Statement Field. Defaults to [].
            subject (Field, optional): The target Subject Field. Subject may be an Object Field, Literal Field, Property Field, or Statement Field. Defaults to None.
            predicate (Field, optional): The target Predicate Field. Predicate may be a Property Field or Object Field. Defaults to None.
            object (Field, optional): The target Object Field. Object may be an Object Field, Literal Field, Property Field, or Statement Field. Defaults to None.
            node_id (str, optional): An optional identifier for the Information Package. This becomes part of the IRI of the underlying owlready2 node. Defaults to None.
        """
        # TODO: default title should be a UUID or something similar?
        title = f"{subject.get_title()} {predicate.get_title()} {object.get_title()}" if title is None else title
        value = utils.generate_placeholder_triple() # the hasValue triple doesn't get set until record or template time
        field_namespace = parent.session.framework_ontology.base_iri # StatementFields are never going to have custom namespaces or classes (verify?)
        field_class = parent.session.framework_ontology.StatementField
        super().__init__(parent, parent.session.core_ontology.DigitalObject, value, title, labels, field_namespace, field_class, is_required=None, node_id=node_id)
        self.node.is_a.append(parent.session.framework_ontology.StatementField)
        self.set_subject(subject)
        self.set_object(object)
        self.set_predicate(predicate)

    def set_subject(self, subject: Field):
        """Set the Subject Field. Subject may be an Object Field, Literal Field, Property Field, or Statement Field.

        Args:
            subject (Field)

        Returns:
            StatementField: The updated Statement Field.
        """
        if subject is not None:
            self.subject = subject
            self.node.hasSubject = [subject.node]
        return self
    
    def set_object(self, object: Field):
        """Set the Object Field. Object may be an Object Field, Literal Field, Property Field, or Statement Field.

        Args:
            object (Field)

        Returns:
            StatementField: The updated Statement Field.
        """
        if object is not None:
            self.object = object
            self.node.hasObject = [object.node]
        return self
    
    def set_predicate(self, predicate: Field):
        """Set the Predicate Field. Predicate may be a Property Field or Object Field.

        Args:
            predicate (Field)

        Returns:
            StatementField: The updated Statement Field.
        """
        if predicate is not None:
            self.predicate = predicate
            self.node.hasPredicate = [predicate.node]
        return self

###The following classes define most of the concepts in the vAIP ontology along with methods that are relevant to each.###

### THE INFORMATION OBJECT SET ###

class InformationObject(VaipResource):
    """An Information Object is a Data Object together with its Representation Information. Information Objects are the fundamental building blocks of the system, and system users typically interact with specific types of information objects.
    """
    def __init__(self, session, VaipClass, namespace: owlready2.Namespace, title, labels, node_id: str = None):
        """Initialize an InformationObject.

        Args:
            session (Session): The target VIP Session.
            VaipClass (Class): The VAIP Class to initialize.
            namespace (owlready2.Namespace): The target owlready2.Namespace instance for the Information Object. This is expected to be the parent node's full IRI.
            title (str, optional): The title of the Property Field. Defaults to None. Ex. 'predatorOf'
            labels (list[str], optional): The list of Alternate Labels for the Property Field. Defaults to [].
            node_id (str, optional): An optional identifier for the Information Object. This becomes part of the IRI of the underlying owlready2 node. Defaults to None.
        """
        super().__init__(session, node_id)
        self.namespace = namespace
        self.node = VaipClass(self.node_id, namespace=self.namespace)
        self.set_title(title)
        self.set_labels(labels)
        self._initialize_objects()

    @classmethod
    def from_rdf(cls, session, ontology, graph, root_iri: str, vaip_type: str, root_node_id: str):
        title, labels = sparql_utils.query_title_and_labels(graph, root_iri)
        namespace = ontology.get_namespace(f"{root_iri.rsplit('/', 1)[0]}/")
        instance = cls(session, session.core_ontology[vaip_type], namespace, title, labels, root_node_id)
        instance._hydrate_from_rdf(session, ontology, graph, root_iri, root_node_id)
        return instance
    
    def _hydrate_from_rdf(self, session, ontology, graph, root_iri, root_node_id):
        fmap = dict([
            ("SemanticRepresentation", self.node.hasSemanticRepresentation),
            ("StructureRepresentation", self.node.hasStructureRepresentation),
            ("OtherRepresentation", self.node.hasOtherRepresentation)
        ])
        res = graph.query(f"""
            PREFIX vaip: <https://ncei.noaa.gov/vaip/ontologies/vaip-core#>
            SELECT ?o
            WHERE {{
                <{root_iri}> (vaip:hasSemanticRepresentation|vaip:hasStructureRepresentation|vaip:hasOtherRepresentation) ?o
            }}
        """)
        for r in res:
            iri = str(r.o)
            io_type = sparql_utils.query_vaip_core_class(graph, iri)
            node_id = None if root_node_id is None else iri.rsplit("/", 1)[1]
            io_instance = InformationObject.from_rdf(session, ontology, graph, iri, io_type, node_id)
            predicate = fmap[io_type]
            predicate.append(io_instance.node)
            self.representations.append(io_instance)
        
        res = graph.query(f"""
            PREFIX vaip: <https://ncei.noaa.gov/vaip/ontologies/vaip-core#>
            SELECT ?o
            WHERE {{
                <{root_iri}> vaip:hasDataObject ?o .
            }}
        """)
        for r in res:
            iri = str(r.o)
            do_type = sparql_utils.query_vaip_core_class(graph, iri)
            node_id = None if root_node_id is None else iri.rsplit("/", 1)[1]
            field = LiteralField.from_rdf(self, graph, iri, do_type, node_id)
            self._add_field(field)
        return self
        
    def destroy(self, cascade = True):
        """Destroy the Information Object and all Data Objects and Representations that are related.
        """
        if cascade:
            [data_object.destroy(cascade) for data_object in self.data_objects]
            [representation.destroy(cascade) for representation in self.representations]
            self.data_objects.clear()
            self.representations.clear()
        super().destroy()

    def _initialize_objects(self):
        """Initialize Data Objects and Representaions
        """
        self.data_objects: list[Field] = []
        self.representations: list[InformationObject] = []

    def _add_field(self, data: typing.Union[TFieldInput, LiteralField]): 
        """Add a Field to the Information Object.

        Args:
            data (typing.Union[TFieldInput, LiteralField])

        Raises:
            Exception: Throws an exception if the combination of Title and Alternate Labels is not unique to the set of Data Objects.

        Returns:
            Field: The updated Field that was added to the Information Object.
        """
        field = data
        if type(data) is not LiteralField:
            title = data.get('title', "")
            is_link = data.get('is_link', False)
            labels = data.get('labels', [])
            value = data.get('value', utils.generate_placeholder())
            is_required = data.get('is_required', True)
            if title == "":
                title = f"{self.get_title()} {'Link' if is_link else 'Value'}"
            
            # vaip_class = self.session.core_ontology.DigitalObject if data.isDigital else self.session.core_ontology.PhysicalObject
            field_namespace = "http://www.w3.org/2001/XMLSchema#"
            field_class = "anyURI" if is_link else "string"
            field = LiteralField(self, title, labels, value, field_namespace, field_class, is_required)
        
        for o in self.data_objects:
            if not o.validate_uniqueness(field.get_title(), field.get_labels()):
                raise Exception("Adding a Field with the same title and labels as an existing Field is not allowed")
        
        self.data_objects.append(field)
        self.node.hasDataObject.append(field.node)
        return field

    def copy_from_information_object(self, source, source_field_values = None):
        """Copy 

        Args:
            source (InformationObject): The Information Object to copy.
            source_field_values (_type_, optional): The list of source Field values to copy. Defaults to None.

        Returns:
            InformationObject: The copy of the Information Object.
        """
        fmap = dict([
            (str(self.session.core_ontology.StructureRepresentation), self.add_structure_representation),
            (str(self.session.core_ontology.SemanticRepresentation), self.add_semantic_representation),
            (str(self.session.core_ontology.OtherRepresentation), self.add_extra_representation),
        ])
        for representation in source.representations:
            add_func = fmap[str(representation.node.is_a[0])]
            copied_repr = add_func(representation.get_title(), labels=representation.get_labels(), field=None)
            copied_repr.copy_from_information_object(representation, source_field_values)
        for dobj in source.data_objects:
            field = dobj.from_field(dobj, self)
            self._add_field(field)
            if source_field_values is not None:
                if dobj.node.iri in source_field_values:
                    field.set_value(source_field_values[dobj.node.iri])
        return self

    def remove_data_object(self, data_object):
        """Removes a Data Object from the Inormation Object

        Args:
            data_object (_type_): The Data Object to remove
        """
        self.data_objects.remove(data_object)
        data_object.destroy()

    def add_link_field(self, title: str, labels: list[str] = [], is_required: bool = True, value = utils.generate_placeholder()): 
        """Add a LiteralField with a hasLink relationship to this InformationObject.

        Args:
            title (str): Name of the linked data
            labels (list[str], optional): Additional labels for the linked data. Defaults to None.

        Returns:
            LiteralField: the linked field
        """
        field = self._add_field({ 'title': title, 'labels': labels, 'value': value, 'is_link': True, 'is_required': is_required })
        return field
    
    def add_value_field(self, title: str, labels: list[str] = [], is_required: bool = True, value = utils.generate_placeholder()):
        """Add a LiteralField with a hasValue relationship to this InformationObject.

        Args:
            title (str): Name of the valued data
            labels (list[str], optional): Additional labels for the valued data. Defaults to None.

        Returns:
            LiteralField: the valued field
        """
        field = self._add_field({ 'title': title, 'labels': labels, 'value': value, 'is_link': False, 'is_required': is_required })
        return field
    
    def _validate_duplicate_representation(self, title, labels):
        """Validate the uniqueness of the combination of Title and Alternate Labels.

        Args:
            title (str): The Title to validate
            labels (List[str]): The list of Alternate Labels to validate.

        Raises:
            Exception: Adding RepresentationInformation with the same title and labels as an existing RepresentationInformation is not allowed
        """
        for r in self.representations:
            if not r.validate_uniqueness(title, labels):
                raise Exception("Adding RepresentationInformation with the same title and labels as an existing RepresentationInformation is not allowed")
        
    def add_structure_representation(self, title: str, labels=[], field: typing.Union[TFieldInput, None] = utils.generate_default_field_input()):
        """Adds a Structure Representation to an Information Object.

        Args:
            title (str): The title of the Structure Representation.
            labels (list, optional): The list of Alternate Labels for the Structure Representation. Defaults to [].
            field (typing.Union[TFieldInput, None], optional): The field for the Structure Representation. Defaults to {{ 'title': "", 'labels': [], 'value': generate_placeholder(), 'is_link': False, 'is_required': True }}}.

        Returns:
            InformationObjct: The new Structure Representation.
        """
        self._validate_duplicate_representation(title, labels)

        namespace = utils.get_dynamic_namespace(self.node)
        obj = InformationObject(self.session, self.session.core_ontology.StructureRepresentation, namespace, title, labels)
        if field: obj._add_field(field)
        self.representations.append(obj)
        self.node.hasStructureRepresentation.append(obj.node)
        return obj

    def remove_structure_representation(self, structure_representation):
        """Removes and destroys a Structure Representation.

        Args:
            structure_representation (InformationObject)
        """
        self.representations.remove(structure_representation)
        structure_representation.destroy()

    def add_semantic_representation(self, title: str, labels=[], field: typing.Union[TFieldInput, None] = utils.generate_default_field_input()):
        """Adds a Semantic Representation to the Information Object.

        Args:
            title (str): Title of the Semantic Representation.
            labels (list, optional):The list of Alternate Labels for the Semantic Representation. Defaults to [].
            field (typing.Union[TFieldInput, None], optional): The field for the Semantic Representation. Defaults to {{ 'title': "", 'labels': [], 'value': generate_placeholder(), 'is_link': False, 'is_required': True }}}.

        Returns:
            InformationObject: The new Semantic Representation.
        """
        self._validate_duplicate_representation(title, labels)
        
        namespace = utils.get_dynamic_namespace(self.node)
        obj = InformationObject(self.session, self.session.core_ontology.SemanticRepresentation, namespace, title, labels)
        if field: obj._add_field(field)
        self.representations.append(obj)
        self.node.hasSemanticRepresentation.append(obj.node)
        return obj

    def remove_semantic_representation(self, semantic_representation):
        """Removes and destroys a Semantic Representation from the Information Object.

        Args:
            semantic_representation (InformationObject)
        """
        self.representations.remove(semantic_representation)
        semantic_representation.destroy()

    def add_extra_representation(self, title: str, labels=[], field: typing.Union[TFieldInput, None] = utils.generate_default_field_input()):
        """Adds an Other Representation to the Information Object.

        Args:
            title (str): The title of the Extra Representation.
            labels (list, optional): The List of Alternate Labels for the Extra Representaion. Defaults to [].
            field (typing.Union[TFieldInput, None], optional): The Field for the Other Representation.  Defaults to {{ 'title': "", 'labels': [], 'value': generate_placeholder(), 'is_link': False, 'is_required': True }}}.

        Returns:
            InformationObject: The new Other Representation
        """
        self._validate_duplicate_representation(title, labels)

        namespace = utils.get_dynamic_namespace(self.node)
        obj = InformationObject(self.session, self.session.core_ontology.OtherRepresentation, namespace, title, labels)
        if field: obj._add_field(field)
        self.representations.append(obj)
        self.node.hasOtherRepresentation.append(obj.node)
        return obj

    def remove_extra_representation(self, extra_representation):
        """Removes and destroys a Other Representation from the Information Object.

        Args:
            extra_representation (InformationObject)
        """
        self.representations.remove(extra_representation)
        extra_representation.destroy()

### THE INFORMATION PACKAGE SET ###

class InformationPackage(VaipResource):
    """InformationPackages represent patternable storage in the knowledge graph.
    All resources in the knowledge graph are representable as whole InformationPackages.
    """
    def __init__(self, session, VaipClass, namespace: typing.Union[owlready2.Namespace, str], title, labels, node_id: str = None):
        """Initialize an Information Package.

        Args:
            session (_type_): The VAIP Session.
            VaipClass (_type_): The VAIP Class for the Information Package. 
            namespace (_type_): The target namespace for the Information Package.
            title (str): The title of the Information Package.
            labels (list[str]): The list of alternate labels to be assigned to the Information Package.
            node_id (str, optional): An optional identifier for the Information Package. This becomes part of the IRI of the underlying owlready2 node. Defaults to None.
        """
        super().__init__(session, node_id)
        if (type(namespace) == owlready2.Namespace):
            self.ontology = namespace.ontology
            self.namespace = namespace
        else:
            self.ontology = session.context.get_ontology(f"{namespace}/{self.node_id}")
            self.namespace = self.ontology.get_namespace(f"{namespace}/{self.node_id}/")
        self.node = VaipClass(self.node_id, namespace=self.namespace)
        self._initialize_objects()
        self.set_title(title)
        self.set_labels(labels)
    
    @classmethod
    def from_rdf(cls, session, graph, root_iri: str, vaip_type: str, root_node_id: str):
        namespace = root_iri.rsplit("/", 2)[0]
        title, labels = sparql_utils.query_title_and_labels(graph, root_iri)
        instance = cls(session, title, labels, root_node_id)
        #instance = cls(session, session.core_ontology[vaip_type], namespace, title, labels, root_node_id)
        instance._hydrate_from_rdf(session, graph, root_iri, root_node_id)
        return instance

    def _hydrate_from_rdf(self, session, graph, root_iri, root_node_id):
        fmap = dict([
            ("ContentInformationObject", self.node.hasContentInformation),
            ("PackagingInformationObject", self.node.packagedBy),
            ("FixityPreservation", self.node.hasFixity),
            ("AccessRightsPreservation", self.node.hasAccessRights),
            ("ContextPreservation", self.node.hasContext),
            ("ProvenancePreservation", self.node.hasProvenance),
            ("ReferencePreservation", self.node.hasReference)
        ])
        res = graph.query(f"""
            PREFIX vaip: <https://ncei.noaa.gov/vaip/ontologies/vaip-core#>
            SELECT ?o
            WHERE {{
                <{root_iri}> (vaip:hasContentInformation|vaip:packagedBy|vaip:hasFixity|vaip:hasAccessRights|vaip:hasContext|vaip:hasProvenance|vaip:hasReference) ?o
            }}
        """)
        for r in res:
            iri = str(r.o)
            io_type = sparql_utils.query_vaip_core_class(graph, iri)
            node_id = None if root_node_id is None else iri.rsplit("/", 1)[1]
            io_instance = InformationObject.from_rdf(session, self.ontology, graph, iri, io_type, node_id)
            predicate = fmap[io_type]
            predicate.append(io_instance.node)
            self.information_objects.append(io_instance)
            for field in io_instance.data_objects:
                self.node.hasLiteralField.append(field.node)
            if io_type == "ContentInformationObject":
                self.content = io_instance
        return self
        
    def destroy(self, cascade = True):
        """Destroys the Information Package and all Informatio Objects related to the Information Package.
        """
        if cascade:
            self.remove_content()
            [information_object.destroy(cascade) for information_object in self.information_objects]
            self.information_objects.clear()
        super().destroy(cascade)

    def _initialize_objects(self):
        """Initialize Information Objects list.
        """
        self.content: InformationObject = None
        self.information_objects: list[InformationObject] = []

    def _validate_duplicate_objects(self, title, labels):
        """Validate that the combinatn of title and alternate labels is unique for the related Information Objects.

        Args:
            title (str): The title to validate
            labels (list[str]): The list of alternate labels to validate.

        Raises:
            Exception: Adding an InformationObject with the same title and labels as an existing InformationObject is not allowed.
        """
        for r in self.information_objects:
            if not r.validate_uniqueness(title, labels):
                raise Exception("Adding an InformationObject with the same title and labels as an existing InformationObject is not allowed")

    def set_content(self, title: str, labels=[], field: typing.Union[TFieldInput, None] = utils.generate_default_field_input()):
        """Sets the content for a Information Package. This DOES overwrite any existing content including Fields.

        Args:
            title (str): The desired title.
            labels (list, optional): The list of alternate labels to assign to the content. Defaults to [].
            field (typing.Union[TFieldInput, None], optional): The Field for the conent. Defaults to {{ 'title': "", 'labels': [], 'value': generate_placeholder(), 'is_link': False, 'is_required': True }}}.

        Raises:
            Exception: Adding an InformationObject with the same title and labels as an existing InformationObject is not allowed

        Returns:
            _type_: _description_
        """
        if self.content is not None and self.content.validate_uniqueness(title, labels) is not True:
            raise Exception("Adding an InformationObject with the same title and labels as an existing InformationObject is not allowed")
        
        namespace = utils.get_dynamic_namespace(self.node)
        obj = InformationObject(self.session, self.session.core_ontology.ContentInformationObject, namespace, title, labels)
        if field:
            new_field = obj._add_field(field)
            self.node.hasLiteralField.append(new_field.node)
        self.content = obj
        self.information_objects.append(obj)
        self.node.hasContentInformation.append(obj.node)
        return obj

    def remove_content(self):
        """Destroys the content of the Information Package.
        """
        if self.content:
            self.information_objects.remove(self.content)
            self.content.destroy()
            self.content = None

    def add_packaging(self, title: str, labels=[], field: typing.Union[TFieldInput, None] = utils.generate_default_field_input()):
        """Adds a Packaging type Information Object to the Information Package.

        Args:
            title (str): The Desired title.
            labels (list, optional): A list of alternate labels to assign to the Packaging. Defaults to [].
            field (typing.Union[TFieldInput, None], optional): The Field to be assicated to the Packaging Information Object. Defaults to {{ 'title': "", 'labels': [], 'value': generate_placeholder(), 'is_link': False, 'is_required': True }}}.

        Returns:
            Information Object: The new Packaging Information Object.
        """
        self._validate_duplicate_objects(title, labels)
        
        namespace = utils.get_dynamic_namespace(self.node)
        obj = InformationObject(self.session, self.session.core_ontology.PackagingInformationObject, namespace, title, labels)
        if field:
            new_field = obj._add_field(field)
            self.node.hasLiteralField.append(new_field.node)
        self.information_objects.append(obj)
        self.node.packagedBy.append(obj.node)
        return obj

    def add_fixity(self, title: str, labels=[], field: typing.Union[TFieldInput, None] = utils.generate_default_field_input()):
        """Adds a Fixity type Information Object to the Information Package.

        Args:
            title (str): The Desired title.
            labels (list, optional): A list of alternate labels to assign to the Fixity. Defaults to [].
            field (typing.Union[TFieldInput, None], optional): The Field to be assicated to the Fixity Information Object. Defaults to {{ 'title': "", 'labels': [], 'value': generate_placeholder(), 'is_link': False, 'is_required': True }}}.

        Returns:
            Information Object: The new Fixity Information Object.
        """
        self._validate_duplicate_objects(title, labels)
        
        namespace = utils.get_dynamic_namespace(self.node)
        obj = InformationObject(self.session, self.session.core_ontology.FixityPreservation, namespace, title, labels)
        if field:
            new_field = obj._add_field(field)
            self.node.hasLiteralField.append(new_field.node)
        self.information_objects.append(obj)
        self.node.hasFixity.append(obj.node)
        return obj

    def add_access_rights(self, title: str, labels=[], field: typing.Union[TFieldInput, None] = utils.generate_default_field_input()):
        """Adds a Access Rights type Information Object to the Information Package.

        Args:
            title (str): The Desired title.
            labels (list, optional): A list of alternate labels to assign to the Access Rights. Defaults to [].
            field (typing.Union[TFieldInput, None], optional): The Field to be assicated to the Access Rights Information Object. Defaults to {{ 'title': "", 'labels': [], 'value': generate_placeholder(), 'is_link': False, 'is_required': True }}}.

        Returns:
            Information Object: The new Access Rights Information Object.
        """
        self._validate_duplicate_objects(title, labels)
        
        namespace = utils.get_dynamic_namespace(self.node)
        obj = InformationObject(self.session, self.session.core_ontology.AccessRightsPreservation, namespace, title, labels)
        if field:
            new_field = obj._add_field(field)
            self.node.hasLiteralField.append(new_field.node)
        self.information_objects.append(obj)
        self.node.hasAccessRights.append(obj.node)
        return obj

    def add_context(self, title: str, labels=[], field: typing.Union[TFieldInput, None] = utils.generate_default_field_input()):
        """Adds a Context type Information Object to the Information Package.

        Args:
            title (str): The Desired title.
            labels (list, optional): A list of alternate labels to assign to the Context. Defaults to [].
            field (typing.Union[TFieldInput, None], optional): The Field to be assicated to the Context Information Object. Defaults to {{ 'title': "", 'labels': [], 'value': generate_placeholder(), 'is_link': False, 'is_required': True }}}.

        Returns:
            Information Object: The new Context Information Object.
        """
        self._validate_duplicate_objects(title, labels)
        
        namespace = utils.get_dynamic_namespace(self.node)
        obj = InformationObject(self.session, self.session.core_ontology.ContextPreservation, namespace, title, labels)
        if field:
            new_field = obj._add_field(field)
            self.node.hasLiteralField.append(new_field.node)
        self.information_objects.append(obj)
        self.node.hasContext.append(obj.node)
        return obj

    def add_provenance(self, title: str, labels=[], field: typing.Union[TFieldInput, None] = utils.generate_default_field_input()):
        """Adds a Provenance type Information Object to the Information Package.

        Args:
            title (str): The Desired title.
            labels (list, optional): A list of alternate labels to assign to the Provenance. Defaults to [].
            field (typing.Union[TFieldInput, None], optional): The Field to be assicated to the Provenance Information Object. Defaults to {{ 'title': "", 'labels': [], 'value': generate_placeholder(), 'is_link': False, 'is_required': True }}}.

        Returns:
            Information Object: The new Provenance Information Object.
        """
        self._validate_duplicate_objects(title, labels)
        
        namespace = utils.get_dynamic_namespace(self.node)
        obj = InformationObject(self.session, self.session.core_ontology.ProvenancePreservation, namespace, title, labels)
        if field:
            new_field = obj._add_field(field)
            self.node.hasLiteralField.append(new_field.node)
        self.information_objects.append(obj)
        self.node.hasProvenance.append(obj.node)
        return obj

    def add_reference(self, title: str, labels=[], field: typing.Union[TFieldInput, None] = utils.generate_default_field_input()):
        """Adds a Reference type Information Object to the Information Package.

        Args:
            title (str): The Desired title.
            labels (list, optional): A list of alternate labels to assign to the Reference. Defaults to [].
            field (typing.Union[TFieldInput, None], optional): The Field to be assicated to the Reference Information Object. Defaults to {{ 'title': "", 'labels': [], 'value': generate_placeholder(), 'is_link': False, 'is_required': True }}}.

        Returns:
            Information Object: The new Reference Information Object.
        """
        self._validate_duplicate_objects(title, labels)
        
        namespace = utils.get_dynamic_namespace(self.node)
        obj = InformationObject(self.session, self.session.core_ontology.ReferencePreservation, namespace, title, labels)
        if field:
            new_field = obj._add_field(field)
            self.node.hasLiteralField.append(new_field.node)
        self.information_objects.append(obj)
        self.node.hasReference.append(obj.node)
        return obj

    def remove_packaging(self, packaging):
        """Removes the provided Packaging from the Information Package.

        Args:
            packaging (InformationObject): The Packaging to be removed.
        """
        self.information_objects.remove(packaging)
        packaging.destroy()
    
    def remove_fixity(self, fixity):
        """Removes the provided Fixity from the Information Package.

        Args:
            fixity (InformationObject): The Fixity to be removed.
        """
        self.information_objects.remove(fixity)
        fixity.destroy()

    def remove_access_rights(self, access_rights):
        """Removes the provided Access Rights from the Information Package.

        Args:
            access_rights (InformationObject): The Access Rights to be removed.
        """
        self.information_objects.remove(access_rights)
        access_rights.destroy()

    def remove_context(self, context):
        """Removes the provided Context from the Information Package.

        Args:
            context (InformationObject): The Context to be removed.
        """
        self.information_objects.remove(context)
        context.destroy()

    def remove_provenance(self, provenance):
        """Removes the provided Provenance from the Information Package.

        Args:
            provenance (InformationObject): The Provenance to be removed.
        """
        self.information_objects.remove(provenance)
        provenance.destroy()

    def remove_reference(self, reference):
        """Removes the provided Reference from the Information Package.

        Args:
            reference (InformationObject): The Reference to be removed.
        """
        self.information_objects.remove(reference)
        reference.destroy()

    def deploy(self):
        responses = self.session.deploy(self)
        return responses

class EntityPackage(InformationPackage):
    def __init__(self, session, VaipClass, namespace, title, labels, node_id = None):
        super().__init__(session, VaipClass, namespace, title, labels, node_id)
        
    def _hydrate_from_rdf(self, session, graph, root_iri, root_node_id):
        super()._hydrate_from_rdf(session, graph, root_iri, root_node_id)
        res = graph.query(f"""
            PREFIX vaip: <https://ncei.noaa.gov/vaip/ontologies/vaip-core#>
            SELECT ?o
            WHERE {{
                <{root_iri}> vaip:describedBy ?o .
                ?o rdf:type vaip:UnitDescription
            }}
        """)
        for r in res:
            iri = str(r.o)
            node_id = None if root_node_id is None else iri.rsplit("/", 1)[1]
            io_instance = InformationObject.from_rdf(session, self.ontology, graph, iri, "UnitDescription", node_id)
            io_instance.node.derivedFromInformationPackage.append(self.node)
            self.node.describedBy.append(io_instance.node)
            self.information_objects.append(io_instance)
            for field in io_instance.data_objects:
                self.node.hasLiteralField.append(field.node)
        return self

    def add_description(self, title: str, labels=[], field: typing.Union[TFieldInput, None] = utils.generate_default_field_input()):
        self._validate_duplicate_objects(title, labels)
        
        namespace = utils.get_dynamic_namespace(self.node)
        obj = InformationObject(self.session, self.session.core_ontology.UnitDescription, namespace, title, labels)
        if field:
            new_field = obj._add_field(field)
            self.node.hasLiteralField.append(new_field.node)
        self.information_objects.append(obj)
        self.node.describedBy.append(obj.node)
        obj.node.derivedFromInformationPackage.append(self.node)
        return obj
    
    def remove_description(self, description):
        self.information_objects.remove(description)
        description.destroy()
        
        # possible owlready2 bug: destroy_entity doesn't actually remove this property for some reason
        description.node.derivedFromInformationPackage = []

class IdentityStoragePattern(EntityPackage):
    """Archive Information Units relate to patterning and recording of identity of any type of entity that might be stored in the knowledge graph.
    This includes things like users, roles, orders, granules, collection records, files, cruises, models, code packages, etc.
    ArchivalInformationUnits should be stored as the data object for AIU pattern metadata. Creating an AIU pattern means creating and persisting a new pattern metadata
    record that holds a new central AIU node of an information package. All information objects are related to information packages through relationship to the central node.
    The central node of the ArchivalInformationUnit is considered the IRI of the entire 'pattern' or thing and other things are logically stored in relationship to it.
    """
    def __init__(self, session, title: str, labels: 'list[str]' = [], node_id: str = None):
        super().__init__(session, session.core_ontology.ArchivalInformationUnit, utils.get_aiu_pattern_namespace(), title, labels, node_id)
        self.node.is_a.append(self.session.framework_ontology.IdentityStoragePattern)

class OutputStoragePattern(EntityPackage):
    def __init__(self, session, title: str, labels: 'list[str]' = [], node_id: str = None):
        super().__init__(session, session.core_ontology.DisseminationInformationPackage, utils.get_dip_pattern_namespace(), title, labels, node_id)
        self.node.is_a.append(self.session.framework_ontology.OutputStoragePattern)

class AICPackage(InformationPackage):
    # TODO: Refactor this class, EntityPackage, TransformationStoragePattern/Template, and BaseTemplate to reduce code
    def __init__(self, session, VaipClass, namespace, title, labels, node_id: str = None):
        super().__init__(session, VaipClass, namespace, title, labels, node_id)
        
    def _hydrate_from_rdf(self, session, graph, root_iri, root_node_id):
        super()._hydrate_from_rdf(session, graph, root_iri, root_node_id)
        res = graph.query(f"""
            PREFIX vaip: <https://ncei.noaa.gov/vaip/ontologies/vaip-core#>
            SELECT ?o
            WHERE {{
                <{root_iri}> vaip:describedByOverviewDescription ?o .
                ?o rdf:type vaip:OverviewDescription
            }}
        """)
        for r in res:
            iri = str(r.o)
            node_id = None if root_node_id is None else iri.rsplit("/", 1)[1]
            io_instance = InformationObject.from_rdf(session, self.ontology, graph, iri, "OverviewDescription", node_id)
            self.node.describedByOverviewDescription.append(io_instance.node)
            self.information_objects.append(io_instance)
            for field in io_instance.data_objects:
                self.node.hasLiteralField.append(field.node)
        return self

    def add_overview_description(self, title: str, labels=[], field: typing.Union[TFieldInput, None] = utils.generate_default_field_input()) -> InformationObject:
        self._validate_duplicate_objects(title, labels)
        namespace = utils.get_dynamic_namespace(self.node)
        obj = InformationObject(self.session, self.session.core_ontology.OverviewDescription, namespace, title, labels)
        if field:
            new_field = obj._add_field(field)
            self.node.hasLiteralField.append(new_field.node)
        self.information_objects.append(obj)
        self.node.describedByOverviewDescription.append(obj.node)
        return obj
    
    def remove_overview_description(self, overview_description: InformationObject):
        self.information_objects.remove(overview_description)
        overview_description.destroy()

class BaseMemberDescription(VaipResource):
    # TODO: This needs to inherit from some manner of InformationObject so that users can add semantic/structure/extra representations
    
    def __init__(self, session, namespace, title, labels, node_id: str = None):
        super().__init__(session, node_id)
        self.namespace = namespace
        self.node = session.core_ontology.MemberDescription(self.node_id, namespace=self.namespace)
        self.set_title(title)
        self.set_labels(labels)
        self.fields: set[Field] = set()
        
    def _hydrate_from_rdf(self, session, graph, root_iri, root_node_id):
        fmap = dict([
            ("ObjectField", ObjectField.from_rdf),
            ("LiteralField", LiteralField.from_rdf),
            ("PropertyField", PropertyField.from_rdf),
            ("StatementField", StatementField.from_rdf)
        ])
        res = graph.query(f"""
            PREFIX fmk: <http://ncei.noaa.gov/vaip/ontologies/vaip-framework#>
            SELECT ?o
            WHERE {{
                <{root_iri}> fmk:hasField ?o
            }}
        """)
        for r in res:
            iri = str(r.o)
            field_type = sparql_utils.query_vaip_framework_class(graph, iri)
            node_id = None if root_node_id is None else iri.rsplit("/", 1)[1]
            func = fmap[field_type]
            field = func(self, graph, iri, "DigitalObject", node_id)
            self._add_field(field)
            if field_type != "StatementField":
                field_attr = field.get_title()
                setattr(self, snakecase(field_attr), field)
            elif field_type == "StatementField":
                subj = field.subject
                obj = field.object
                if type(subj) is ObjectField and (type(obj) is ObjectField or LiteralField):
                    setattr(subj, obj.get_title(), obj)
        return self
    
    def destroy(self, cascade = True):
        """Destroy the Member Description Pattern and all related Fields.
        """
        if cascade:
            [field.destroy(cascade) for field in self.fields]
            self.fields.clear()
        super().destroy(cascade)

    def _find_vaip_framework_property_field(self):
        """Finds the "hasProperty" Property Field for the Member Description Pattern.

        Returns:
            PropertyField: The "hasProperty" Property Field for the Member Description Pattern.
        """
        for field in self.fields:
            if (type(field) is not PropertyField): continue
            if field.field_namespace == self.session.framework_ontology.base_iri and field.field_class == "hasProperty":
                return field
        return None

    def _add_field(self, field: Field):
        """Adds a Field to the Member Description.

        Args:
            field (Field)

        Returns:
            Field: Returns the updated Field.
        """
        self.fields.add(field)
        self.node.hasField.append(field.node)
        return field
        
    def deploy(self):
        responses = self.session.deploy(self)
        return responses

class MemberDescriptionPattern(BaseMemberDescription):
    """A member description describes a particular collection member and its contextual purpose within a collection and how it is relevant to a particular user or access aid. Member descriptions are types of associated descriptions.
    """

    def __init__(self,
        session,
        aic_pattern: typing.Union[TransformationStoragePattern, str],
        title: str,
        labels: 'list[str]' = [],
        node_id: str = None
    ):
        """Initialize a new Member Description Pattern.

        Args:
            aic_pattern (typing.Union[TransformationStoragePattern, str]): The TransformationStoragePattern this Member Description Pattern belongs to.
            title (str): The title of the Member Description Pattern
            labels (List[str]): The list of alternate labels to be applied to the Member Description Pattern
            node_id (str, optional): An optional identifier for the Member Description Pattern. This becomes part of the IRI of the underlying owlready2 node. Defaults to None.
        """
        self.aic_id = aic_pattern if isinstance(aic_pattern, str) else aic_pattern.node_id
        self.ontology = session.context.get_ontology(utils.get_aic_member_description_pattern_namespace(self.aic_id))
        self.namespace = self.ontology.get_namespace(f"{utils.get_aic_member_description_pattern_namespace(self.aic_id)}/")
        super().__init__(session, self.namespace, title, labels, node_id)
        self.node.is_a.append(self.session.framework_ontology.MemberDescriptionPattern)

    @classmethod
    def from_rdf(cls, session, graph, root_iri: str, vaip_type: str, root_node_id: str):
        title, labels = sparql_utils.query_title_and_labels(graph, root_iri)
        # https://ncei.noaa.gov/vaip/pattern/storage/aic/<aic_id>/member_descriptions/<mdesc_uuid>/
        aic_pattern_id = root_iri.rsplit("/", 4)[1]
        instance = cls(session, aic_pattern_id, title, labels, root_node_id)
        instance._hydrate_from_rdf(session, graph, root_iri, root_node_id)
        return instance
    
    def connect(self, source_field: Field, target_field: Field, title: str = None, labels: list[str] = [], namespace: str = None, namespace_class: str = None):
        """Connects two Fields together through a Property and Statement Field combination.

        Args:
            source_field (Field): The subject of the connecting Statement Field.
            target_field (Field): The object of the connecting Statement Field.
            title (str, optional): The title of the generated Property Field. Defaults to None. Ex. 'predatorOf'
            labels (list[str], optional): The list of Alternate Labels for the generated Property Field. Defaults to [].
            namespace (str, optional): The traget namespace IRI for the generated Property Field. Defaults to the parent node's namespace IRI.
            namespace_class (str, optional): The namespace class for the generated Property Field. Defaults to the title value used.

        Returns:
            StatementField: The generated Statement Field.
        """
        property = PropertyField(self, title, labels, namespace, namespace_class, is_required=True)
        statement = StatementField(self, subject = source_field, predicate = property, object = target_field)

        self._add_field(property)
        self._add_field(statement)
        return statement
    
    def add_object(self, title: str = None, labels: list[str] = [], namespace: str = None, namespace_class: str = None, is_required: bool = True, auto_generated: bool = False):
        """Create a new Object Field for the Member Description

        Args:
            title (str, optional): The title of the Object Field. Defaults to None. Ex. 'predatorOf'
            labels (list[str], optional): The list of Alternate Labels for the Object Field. Defaults to [].
            namespace (str, optional): The traget namespace IRI for the Object Field. Defaults to the parent node's namespace IRI.
            namespace_class (str, optional): The namespace class for the Object Field. Defaults to the title value used.
            is_required (bool, optional): Is the Object Field required for UBL? Defaults to True.
            auto_generated (bool, optional): Was the Object autogenerated. Defaults to False.

        Returns:
            ObjectField: The new Object Field.
        """
        obj = ObjectField(self, title, labels, namespace, namespace_class, is_required, auto_generated)
        self._add_field(obj)
        return obj
    
    def add_literal(self, title: str = None, labels: list[str] = [], namespace: str = None, namespace_class: str = None, is_required: bool = True):
        """Create a new Literal Field for the Member Description

        Args:
            title (str, optional): The title of the Literal Field. Defaults to None. Ex. 'predatorOf'
            labels (list[str], optional): The list of Alternate Labels for the Literal Field. Defaults to [].
            namespace (str, optional): The traget namespace IRI for the Literal Field. Defaults to the parent node's namespace IRI.
            namespace_class (str, optional): The namespace class for the Literal Field. Defaults to the title value used.
            is_required (bool, optional): Is the Literal Field required for UBL? Defaults to True.

        Returns:
            LiteralField: The new Literal Field.
        """
        lit = LiteralField(self, title, labels, namespace=namespace, namespace_class=namespace_class, is_required=is_required)
        self._add_field(lit)
        return lit

    def add_property(self, title: str = None, labels: list[str] = [], namespace: str = None, namespace_class: str = None, is_required: bool = True):
        """Create a new Property Field for the Member Description

        Args:
            title (str, optional): The title of the Property Field. Defaults to None. Ex. 'predatorOf'
            labels (list[str], optional): The list of Alternate Labels for the Property Field. Defaults to [].
            namespace (str, optional): The traget namespace IRI for the Property Field. Defaults to the parent node's namespace IRI.
            namespace_class (str, optional): The namespace class for the Property Field. Defaults to the title value used.
            is_required (bool, optional): Is the Property Field required for UBL? Defaults to True.

        Returns:
            PropertyField: The new Property Field
        """
        prop = PropertyField(self, title, labels, namespace, namespace_class, is_required)
        self._add_field(prop)
        return prop

    def add_statement(self, title: str = None, labels: list[str] = [], subject: Field = None, predicate: Field = None, object: Field = None):
        """Create a new Statement Field for the Member Description.

        Args:
            title (str, optional): The title of the Statement Field. Defaults to None. Ex. 'predatorOf'
            labels (list[str], optional): The list of Alternate Labels for the Statement Field. Defaults to [].
            subject (Field, optional): The target Subject Field. Subject may be an Object Field, Literal Field, Property Field, or Statement Field. Defaults to None.
            predicate (Field, optional): The target Predicate Field. Predicate may be a Property Field or Object Field. Defaults to None.
            object (Field, optional): The target Object Field. Object may be an Object Field, Literal Field, Property Field, or Statement Field. Defaults to None.

        Returns:
            StatementField: The new Statement Field.
        """
        statement = StatementField(self, title, labels, subject, predicate, object)
        self._add_field(statement)
        return statement

class MemberDescriptionTemplate(BaseMemberDescription):
    def __init__(self,
        session,
        source_pattern: typing.Union[MemberDescriptionPattern, str] = None,
        aic_template: typing.Union[TransformationStorageTemplate, str] = None,
        source_template: typing.Union[MemberDescriptionTemplate, str] = None,
        graph: Graph = None,
        node_id: str = None
    ):
        """Initialize a new Member Description Template.

        Args:
            source_pattern (MemberDescriptionPattern): The pattern this MemberDescriptionTemplate is copied from.
            aic_template (typing.Union[TransformationStorageTemplate, str): Provide either a TransformationStorageTemplate instance of the IRI of a TransformationStorageTemplate.
            node_id (str, optional): An optional identifier for the Member Description Template. This becomes part of the IRI of the underlying owlready2 node. Defaults to None.
        """
        self.aic_template_id = aic_template if isinstance(aic_template, str) else aic_template.node_id
        self.ontology = session.context.get_ontology(utils.get_aic_member_description_template_namespace(self.aic_template_id))
        self.namespace = self.ontology.get_namespace(f"{utils.get_aic_member_description_template_namespace(self.aic_template_id)}/")
        
        if source_pattern is not None:
            super().__init__(session, self.namespace, source_pattern.get_title(), source_pattern.get_labels(), node_id)
            self.copy_from_member_description(source_pattern)
        elif source_template is not None:
            if isinstance(source_template, str):
                if graph is not None:
                    title, labels = sparql_utils.query_title_and_labels(graph, source_template)
                    super().__init__(session, self.namespace, title, labels, node_id)
                    # hydrate_from_rdf will be called after the constructor, so don't need to run `copy_from_member_description`
                else:
                    template = utils.load(session, source_template, as_copy=True)
                    super().__init__(session, self.namespace, source_pattern.get_title(), source_pattern.get_labels(), node_id)
                    self.copy_from_member_description(template)
            else:
                super().__init__(session, self.namespace, source_template.get_title(), source_template.get_labels(), node_id)
                self.copy_from_member_description(source_template)
        
        self.node.is_a.append(self.session.framework_ontology.MemberDescriptionTemplate)
    
    @classmethod
    def from_rdf(cls, session, graph, root_iri: str, vaip_type: str, root_node_id: str):
        # https://ncei.noaa.gov/vaip/template/storage/aic/<aic_id>/member_descriptions/<mdesc_uuid>/
        aic_template_id = root_iri.rsplit("/", 4)[1]
        instance = cls(session, aic_template=aic_template_id, source_template=root_iri, graph=graph, node_id=root_node_id)
        instance._hydrate_from_rdf(session, graph, root_iri, root_node_id)
        return instance
        
    # def _hydrate_from_rdf(self, session, graph, root_iri, root_node_id):
    #     super()._hydrate_from_rdf(session, graph, root_iri, root_node_id)
    
    def copy_from_member_description(self, source: BaseMemberDescription, source_field_values = None):
        """Copies the source Member Description. This includes all related Fields.

        Args:
            source (BaseMemberDescription): The Member Description you wish to copy

        Returns:
            MemberDescriptionTemplate: The copy Member Description as a Template.
        """
        fmap = dict([
            (str(ObjectField), ObjectField.from_field),
            (str(LiteralField), LiteralField.from_field),
            (str(PropertyField), PropertyField.from_field)
        ])
        # There are 2 steps for copying Fields from a Member Description:
        #     1. Copy all terminal/leaf Fields
        #     2. Copy all StatementFields and ensure the s/p/o of the copied Statement references the same Fields as the original Statement
        #          2a. TODO: This new StatementField can potentially be fully valued if all its components are fully valued at template time
        statement_fields: set[StatementField] = set()
        copied_field_map: dict[Field, Field] = {}
        for field in source.fields:
            if type(field) is StatementField:
                statement_fields.add(field)
            else:
                add_func = fmap[str(type(field))]
                copied_field = add_func(field, self)
                self._add_field(copied_field)
                copied_field_map[field] = copied_field
                field_attr = field.get_title()
                setattr(self, snakecase(field_attr), copied_field)
            if source_field_values is not None:
                if field.node.iri in source_field_values:
                    copied_field.set_value(source_field_values[field.node.iri])
        
        for stmnt in statement_fields:
            subj = stmnt.subject
            pred = stmnt.predicate
            obj = stmnt.object
            copied_s = copied_field_map[subj]
            copied_p = copied_field_map[pred]
            copied_o = copied_field_map[obj]
            copied_statement = StatementField(self, None, stmnt.get_labels(), copied_s, copied_p, copied_o)
            self._add_field(copied_statement)
            if type(copied_s) is ObjectField and (type(copied_o) is ObjectField or LiteralField):
                setattr(copied_s, copied_o.get_title(), copied_o)
        return self

class MemberDescriptionRecord(BaseMemberDescription):
    def __init__(self,
        session,
        source_template: typing.Union[MemberDescriptionTemplate, str] = None,
        source_record: typing.Union[MemberDescriptionRecord, str] = None,
        graph: Graph = None,
        template_field_values = {},
        node_id: str = None
    ):
        """Initialize a new Member Description Record.

        Args:
            source_template (MemberDescriptionTemplate): The source MemberDescriptionTemplate to copy from.
            template_field_values (dict): A dictionary of Field IRIs present in the source_template mapped to their actual values.
        """
        if source_template is not None:
            aic_template_id = source_template.aic_template_id
            self.ontology = session.context.get_ontology(utils.get_aic_member_description_record_namespace(aic_template_id))
            self.namespace = self.ontology.get_namespace(f"{utils.get_aic_member_description_record_namespace(aic_template_id)}/")
            super().__init__(session, self.namespace, source_template.get_title(), source_template.get_labels())
            self._copy_from_template(source_template, template_field_values)
        elif source_record is not None:
            if isinstance(source_record, str):
                aic_template_id = source_record.rsplit("/", 4)[1]
                if graph is not None:
                    title, labels = sparql_utils.query_title_and_labels(graph, source_record)
                    self.ontology = session.context.get_ontology(utils.get_aic_member_description_record_namespace(aic_template_id))
                    self.namespace = self.ontology.get_namespace(f"{utils.get_aic_member_description_record_namespace(aic_template_id)}/")
                    super().__init__(session, self.namespace, title, labels)
                    # hydrate_from_rdf will be called after the constructor, so don't need to run `copy_from_member_description`
                else:
                    record = utils.load(session, source_record, as_copy=True)
                    self.ontology = session.context.get_ontology(utils.get_aic_member_description_record_namespace(aic_template_id))
                    self.namespace = self.ontology.get_namespace(f"{utils.get_aic_member_description_record_namespace(aic_template_id)}/")
                    super().__init__(session, self.namespace, record.get_title(), record.get_labels())
                    self._copy_from_template(record, template_field_values)
            else:
                aic_template_id = source_record.node.iri.rsplit("/", 4)[1]
                self.ontology = session.context.get_ontology(utils.get_aic_member_description_record_namespace(aic_template_id))
                self.namespace = self.ontology.get_namespace(f"{utils.get_aic_member_description_record_namespace(aic_template_id)}/")
                super().__init__(session, self.namespace, source_record.get_title(), source_record.get_labels())
                self._copy_from_template(record, template_field_values)
        
        self.node.is_a.append(self.session.framework_ontology.MemberDescriptionRecord)
    
    @classmethod
    def from_rdf(cls, session, graph, root_iri: str, vaip_type: str, root_node_id: str):
        instance = cls(session, source_record=root_iri, graph=graph, node_id=root_node_id)
        instance._hydrate_from_rdf(session, graph, root_iri, root_node_id)
        return instance
    
    def _copy_from_template(self, template: MemberDescriptionTemplate, template_field_values):
        fmap = dict([
            (str(ObjectField), ObjectField.from_field),
            (str(LiteralField), LiteralField.from_field),
            (str(PropertyField), PropertyField.from_field)
        ])
        statement_fields: set[StatementField] = set()
        copied_field_map: dict[Field, Field] = {}
        for field in template.fields:
            if type(field) is StatementField:
                statement_fields.add(field)
            else:
                add_func = fmap[str(type(field))]
                copied_field = add_func(field, self)
                self._add_field(copied_field)
                copied_field_map[field] = copied_field
                field_attr = field.get_title()
                setattr(self, snakecase(field_attr), copied_field)
            if template_field_values is not None:
                if field.node.iri in template_field_values:
                    copied_field.set_value(template_field_values[field.node.iri])
        
        for stmnt in statement_fields:
            subj = stmnt.subject
            pred = stmnt.predicate
            obj = stmnt.object
            copied_s = copied_field_map[subj]
            copied_p = copied_field_map[pred]
            copied_o = copied_field_map[obj]
            
            # At this point, we now have to generate the relationships defined by the PropertyField referenced in the StatementField.
            # To do this, we can access the `copied_p.field_namespace` and `copied_p.field_class` attributes.
            # As long as the ontology referenced by `field_namespace` is loaded in the session, it can be accessed as an owlready2 ObjectProperty
            # As an ObjectProperty, we can add a relation to it by doing `prop[node] = [something]`
            prop = self.session.framework_ontology[copied_p.field_class]
            prop[copied_s.node] = [copied_o.node]
            if type(copied_s) is ObjectField and (type(copied_o) is ObjectField or LiteralField):
                setattr(copied_s, copied_o.get_title(), copied_o)
        return self

class TransformationStoragePattern(AICPackage):
    def __init__(self, session, title: str, labels: 'list[str]' = [], node_id: str = None):
        super().__init__(session, session.core_ontology.ArchivalInformationCollection, utils.get_aic_pattern_namespace(), title, labels, node_id)
        self.node.is_a.append(self.session.framework_ontology.TransformationStoragePattern)
        self.member_descriptions: 'set[MemberDescriptionPattern]' = set()
        
    def _hydrate_from_rdf(self, session, graph, root_iri, root_node_id):
        super()._hydrate_from_rdf(session, graph, root_iri, root_node_id)
        res = graph.query(f"""
            PREFIX vaip: <https://ncei.noaa.gov/vaip/ontologies/vaip-core#>
            PREFIX fmk: <http://ncei.noaa.gov/vaip/ontologies/vaip-framework#>
            SELECT ?o
            WHERE {{
                <{root_iri}> fmk:hasMemberDescriptionPattern ?o
            }}
        """)
        for r in res:
            iri = str(r.o)
            node_id = None if root_node_id is None else iri.rsplit("/", 1)[1]
            as_copy = node_id == None
            member_desc = utils.load(self.session, iri, as_copy=as_copy)
            # member_desc = MemberDescriptionPattern.from_rdf(self.session, graph, iri, "MemberDescription", node_id)
            self.member_descriptions.add(member_desc)
            self.node.describedByMemberDescription.append(member_desc.node)
            self.node.hasMemberDescriptionPattern.append(member_desc.node)
        return self

    def add_member_description(self, title: str, labels: 'list[str]' = []) -> MemberDescriptionPattern:
        member_desc = MemberDescriptionPattern(self.session, self, title, labels)
        self.member_descriptions.add(member_desc)
        self.node.describedByMemberDescription.append(member_desc.node)
        self.node.hasMemberDescriptionPattern.append(member_desc.node)
        return member_desc

    def remove_member_description(self, member_description: MemberDescriptionPattern):
        self.member_descriptions.remove(member_description)
        member_description.destroy()

class TransformationStorageTemplate(AICPackage):
    """Context Transformation Storage Template"""
    def __init__(self,
        session,
        source_pattern: typing.Union[AICPackage, str] = None,
        source_template: typing.Union[TransformationStorageTemplate, str] = None,
        graph: Graph = None,
        namespace: str = utils.get_aic_template_namespace(),
        node_id: str = None
    ):
        self.labeled_fields: typing.Dict[str, typing.Dict[str, Field]]= {}
        """ labeled_fields is a dictionary mapping an InformationObject's title to another dictionary containing all of its Fields' titles.
            Essentially it is an index pointing to Fields using first their containing InformationObject's title and then the Field's title.
        """
        self.id_fields: typing.Dict[str, Field] = {}
        """ id_fields is a counterpart to labeled_fields in that they both point to the same set of Fields.
            id_fields simply uses the node_id of the Field as the index to the Field.
        """
        self.member_descriptions: set[MemberDescriptionTemplate] = set()
        
        if source_pattern is not None:
            pattern = utils.load(session, source_pattern, as_copy=False) if isinstance(source_pattern, str) else source_pattern
            VaipClass = pattern.node.is_a[0]
            super().__init__(session, VaipClass, namespace, pattern.get_title(), pattern.get_labels(), node_id)
            self.node.hasParentPattern = [source_pattern.node]
            self._copy_from_package(pattern)
        elif source_template is not None:
            if isinstance(source_template, str):
                if graph is not None:
                    title, labels = sparql_utils.query_title_and_labels(graph, source_template)
                    vaip_class_str = sparql_utils.query_vaip_core_class(graph, source_template)
                    VaipClass = session.core_ontology[vaip_class_str]
                    super().__init__(session, VaipClass, namespace, title, labels, node_id)
                else:
                    template = utils.load(session, source_template, as_copy=True)
                    VaipClass = template.node.is_a[0]
                    super().__init__(session, VaipClass, namespace, template.get_title(), template.get_labels(), node_id)
                    self._copy_from_package(template)
            else:
                VaipClass = source_template.node.is_a[0]
                super().__init__(session, VaipClass, namespace, source_template.get_title(), source_template.get_labels(), node_id)
                self._copy_from_package(source_template)
        
        self.node.is_a.append(self.session.framework_ontology.TransformationStorageTemplate)

    @classmethod
    def from_rdf(cls, session, graph, root_iri: str, vaip_type: str, root_node_id: str):
        """Creates a Transformation Storage Template from an RDF Graph.

        Args:
            session (_type_): The Ontology Session
            graph (_type_): The graph to generate the Teansformation Storage Template
            root_iri (str): The root iri of the graph
            vaip_type (str): Unused
            root_node_id (str): The node id to append the Transformation Storage Template to in the Session.

        Returns:
            TransformationStorageTemplate: TransformationStorageTemplate
        """
        namespace = root_iri.rsplit("/", 2)[0]
        instance = cls(
            session,
            source_template=root_iri,
            graph=graph,
            namespace=namespace,
            node_id=root_node_id
        )
        instance._hydrate_from_rdf(session, graph, root_iri, root_node_id)
        return instance
    
    def _hydrate_from_rdf(self, session, graph, root_iri: str, root_node_id: str):
        super()._hydrate_from_rdf(session, graph, root_iri, root_node_id)
        res = graph.query(f"""
            PREFIX fmk: <http://ncei.noaa.gov/vaip/ontologies/vaip-framework#>
            SELECT ?o
            WHERE {{
                <{root_iri}> fmk:hasParentPattern ?o 
            }}
        """)
        for r in res:
            source_pattern_iri = str(r.o)
            break
        
        # Create a temporary owlready2 instance of the vaip-framework Pattern class, using the parent pattern IRI obtained from query.
        # This is a workaround to avoid loading the entire Pattern into owlready2.
        # owlready2 throws an error if `self.node.hasParentPattern` is assigned to a string; it must be an owlready2 object
        p_split = source_pattern_iri.rsplit("/", 2)
        temp_node_id = p_split[2]
        temp_namespace = session.context.get_ontology(p_split[0]).get_namespace(source_pattern_iri)
        pattern = session.framework_ontology.Pattern(temp_node_id, namespace=temp_namespace)
        self.node.hasParentPattern = [pattern]
        
        for iobj in self.information_objects:
            iobj_title = iobj.get_title()
            setattr(self, snakecase(iobj_title), iobj)
            self.labeled_fields[iobj_title] = {}
            for dobj in iobj.data_objects:
                dobj_title = dobj.get_title()
                dobj_id = dobj.node_id
                setattr(iobj, snakecase(dobj_title), dobj)
                self.id_fields[dobj_id] = dobj
                self.labeled_fields[iobj_title][dobj.get_title()] = dobj
                self.node.hasLiteralField.append(dobj.node)
                
        res = graph.query(f"""
            PREFIX vaip: <https://ncei.noaa.gov/vaip/ontologies/vaip-core#>
            PREFIX fmk: <http://ncei.noaa.gov/vaip/ontologies/vaip-framework#>
            SELECT ?o
            WHERE {{
                <{root_iri}> fmk:hasMemberDescriptionTemplate ?o
            }}
        """)
        for r in res:
            iri = str(r.o)
            node_id = None if root_node_id is None else iri.rsplit("/", 1)[1]
            as_copy = node_id == None
            member_desc = utils.load(self.session, iri, as_copy=as_copy)
            # member_desc = MemberDescriptionTemplate.from_rdf(self.session, graph, iri, "MemberDescription", node_id)
            self.member_descriptions.add(member_desc)
            self.node.describedByMemberDescription.append(member_desc.node)
            self.node.hasMemberDescriptionTemplate.append(member_desc.node)
        
        return self
    
    def _copy_from_package(self, source_package: AICPackage):
        """Create a new instance of Transformation Storage Template from an existing one.

        Args:
            source_package (AICPackage): An existing Transformation Storage Template
        """
        fmap = dict([
            (str(self.session.core_ontology.ContentInformationObject), self.set_content),
            (str(self.session.core_ontology.OverviewDescription), self.add_overview_description),
            (str(self.session.core_ontology.PackagingInformationObject), self.add_packaging),
            (str(self.session.core_ontology.FixityPreservation), self.add_fixity),
            (str(self.session.core_ontology.AccessRightsPreservation), self.add_access_rights),
            (str(self.session.core_ontology.ContextPreservation), self.add_context),
            (str(self.session.core_ontology.ProvenancePreservation), self.add_provenance),
            (str(self.session.core_ontology.ReferencePreservation), self.add_reference)
        ])
        for iobj in source_package.information_objects:
            iobj_title = iobj.get_title()
            add_func = fmap[str(iobj.node.is_a[0])]
            copied_resource = add_func(iobj_title, iobj.get_labels(), field=None)
            copied_resource.copy_from_information_object(iobj)
            setattr(self, snakecase(iobj_title), copied_resource)
            self.labeled_fields[iobj_title] = {}
            for dobj in copied_resource.data_objects:
                dobj_title = dobj.get_title()
                dobj_id = dobj.node_id
                setattr(copied_resource, snakecase(dobj_title), dobj)
                self.id_fields[dobj_id] = dobj
                self.labeled_fields[iobj_title][dobj.get_title()] = dobj
                self.node.hasLiteralField.append(dobj.node)
        
        for mdesc in source_package.member_descriptions:
            member_desc = MemberDescriptionTemplate(self.session, source_template=mdesc, aic_template=self)
            self.member_descriptions.add(member_desc)
            setattr(self, snakecase(member_desc.get_title()), member_desc)
            self.node.describedByMemberDescription.append(member_desc.node)
            self.node.hasMemberDescriptionTemplate.append(member_desc.node)
        

class TransformationStorageRecord(AICPackage):
    """ Transformation/AIC Storage Record
    
    A Record is a fully valued unit of the system - each Record derives from a runtime execution of a Template. Records are deep-copies of Template parents. As deep-copies of Templates, Records are fully conformant to the implemented Reference Model and are fully denormalized metadata.
    """
    def __init__(self,
        session,
        source_template: TransformationStorageTemplate = None,
        source_record: typing.Union[TransformationStorageRecord, str] = None,
        graph: Graph = None,
        template_field_values = {},
        node_id: str = None
    ):
        self.member_descriptions: set[MemberDescriptionRecord] = set()
        namespace = utils.get_aic_record_namespace()
        
        if source_template is not None:
            self.aic_template_id = source_template.node_id
            super().__init__(session, session.core_ontology.ArchivalInformationCollection, namespace, source_template.get_title(), source_template.get_labels(), self.aic_template_id)
            self.node.hasParentTemplate = [source_template.node]
            self._copy_from_template(source_template, template_field_values)
        elif source_record is not None:
            if isinstance(source_record, str):
                self.aic_template_id = source_record.rsplit("/", 1)[1]
                if graph is not None:
                    title, labels = sparql_utils.query_title_and_labels(graph, source_record)
                    super().__init__(session, session.core_ontology.ArchivalInformationCollection, namespace, title, labels, self.aic_template_id)
                    # hydrate_from_rdf will be called after the constructor, so don't need to run `_copy_from_template`
                else:
                    record = utils.load(session, source_record, as_copy=True)
                    super().__init__(session, session.core_ontology.ArchivalInformationCollection, namespace, record.get_title(), record.get_labels(), self.aic_template_id)
                    self._copy_from_template(record, template_field_values)
            else:
                self.aic_template_id = source_record.node.iri.rsplit("/", 1)[1]
                super().__init__(session, session.core_ontology.ArchivalInformationCollection, namespace, source_record.get_title(), source_record.get_labels(), self.aic_template_id)
                self._copy_from_template(source_record, template_field_values)
        
        self.node.is_a.append(session.framework_ontology.TransformationStorageRecord)
    
    @classmethod
    def from_rdf(cls, session, graph, root_iri: str, vaip_type: str, root_node_id: str):
        """Creates a Transformation Storage Record from an RDF Graph.

        Args:
            session (_type_): The Ontology Session
            graph (_type_): The graph to generate the Teansformation Storage Record
            root_iri (str): The root iri of the graph
            vaip_type (str): Unused
            root_node_id (str): The node id to append the Transformation Storage Record to in the Session.

        Returns:
            TransformationStorageRecord: TransformationStorageRecord
        """
        instance = cls(
            session,
            source_record=root_iri,
            graph=graph,
            node_id=root_node_id
        )
        instance._hydrate_from_rdf(session, graph, root_iri, root_node_id)
        return instance
    
    def _hydrate_from_rdf(self, session, graph, root_iri: str, root_node_id: str):
        super()._hydrate_from_rdf(session, graph, root_iri, root_node_id)
        res = graph.query(f"""
            PREFIX fmk: <http://ncei.noaa.gov/vaip/ontologies/vaip-framework#>
            SELECT ?o
            WHERE {{
                <{root_iri}> fmk:hasParentTemplate ?o 
            }}
        """)
        for r in res:
            source_template_iri = str(r.o)
            break
        
        # Create a temporary owlready2 instance of the vaip-framework Pattern class, using the parent pattern IRI obtained from query.
        # This is a workaround to avoid loading the entire Pattern into owlready2.
        # owlready2 throws an error if `self.node.hasParentPattern` is assigned to a string; it must be an owlready2 object
        p_split = source_template_iri.rsplit("/", 2)
        temp_node_id = p_split[2]
        temp_namespace = session.context.get_ontology(p_split[0]).get_namespace(source_template_iri)
        template = session.framework_ontology.Template(temp_node_id, namespace=temp_namespace)
        self.node.hasParentTemplate = [template]
        
        for iobj in self.information_objects:
            iobj_title = iobj.get_title()
            setattr(self, snakecase(iobj_title), iobj)
            for dobj in iobj.data_objects:
                dobj_title = dobj.get_title()
                setattr(iobj, snakecase(dobj_title), dobj)
                self.node.hasLiteralField.append(dobj.node)
        return self
    
    def _copy_from_template(self, template: AICPackage, template_field_values):
        fmap = dict([
            (str(self.session.core_ontology.ContentInformationObject), self.set_content),
            (str(self.session.core_ontology.OverviewDescription), self.add_overview_description),
            (str(self.session.core_ontology.PackagingInformationObject), self.add_packaging),
            (str(self.session.core_ontology.FixityPreservation), self.add_fixity),
            (str(self.session.core_ontology.AccessRightsPreservation), self.add_access_rights),
            (str(self.session.core_ontology.ContextPreservation), self.add_context),
            (str(self.session.core_ontology.ProvenancePreservation), self.add_provenance),
            (str(self.session.core_ontology.ReferencePreservation), self.add_reference)
        ])
        for iobj in template.information_objects:
            add_func = fmap[str(iobj.node.is_a[0])]
            iobj_title = iobj.get_title()
            copied_resource = add_func(iobj_title, iobj.get_labels(), field=None)
            copied_resource.copy_from_information_object(iobj, template_field_values)
            setattr(self, snakecase(iobj_title), copied_resource)
            for dobj in copied_resource.data_objects:
                setattr(copied_resource, snakecase(dobj.get_title()), dobj)
                self.node.hasLiteralField.append(dobj.node)

class ProcessPattern(EntityPackage):
    """ A Pattern that can be used and reused to create Processes."""
    def __init__(self, session, title: str, labels: 'list[str]' = [], node_id: str = None):
        """Create a Process Pattern.

        Args:
            session (_type_): The Ontology Sesion. 
            title (str): The title of the Process Pattern
            labels (list[str], optional): All additional alternate labels. Defaults to [].
            node_id (str, optional): The node ID to associate the proces pattern to. Defaults to None.
        """
        super().__init__(session, session.core_ontology.ArchivalInformationUnit, utils.get_process_pattern_namespace(), title, labels, node_id)
        self.node.is_a.append(self.session.framework_ontology.ProcessPattern)

class UBLPattern(EntityPackage):
    """User Business Logic (UBL) represents a task-bound configuration container for holding some user provided computationally capable action - an API call, a service call, a lambda or Docker containing code, a step function, etc. UBL takes in a flat set of values and passes out a flat set of values. The UBL should provide either in template or at runtime enough information to successfully trigger and resolve a call to the specified user logic. The UBL as a construct avoids placing burden on the user to leverage hardcoded message adapters or other intrusive mechanisms.
    """
    def __init__(self, session, title: str, labels: 'list[str]' = [], node_id: str = None):
        super().__init__(session, session.core_ontology.ArchivalInformationUnit, utils.get_ubl_pattern_namespace(), title, labels, node_id)
        self.node.is_a.append(self.session.framework_ontology.UBLPattern)

class IdentityTaskPattern(EntityPackage):
    """A pattern used to create Identity Tasks."""
    def __init__(self, session, title: str, labels: 'list[str]' = [], node_id: str = None):
        super().__init__(session, session.core_ontology.ArchivalInformationUnit, utils.get_task_pattern_namespace(), title, labels, node_id)
        self.node.is_a.append(self.session.framework_ontology.IdentityTaskPattern)

class TransformationTaskPattern(EntityPackage):
    """A Pattern used to create Transformation Tasks."""
    def __init__(self, session, title: str, labels: 'list[str]' = [], node_id: str = None):
        super().__init__(session, session.core_ontology.ArchivalInformationUnit, utils.get_task_pattern_namespace(), title, labels, node_id)
        self.node.is_a.append(self.session.framework_ontology.TransformationTaskPattern)

class OutputTaskPattern(EntityPackage):
    """A Pattern used to create Output Tasks."""
    def __init__(self, session, title: str, labels: 'list[str]' = [], node_id: str = None):
        super().__init__(session, session.core_ontology.ArchivalInformationUnit, utils.get_task_pattern_namespace(), title, labels, node_id)
        self.node.is_a.append(self.session.framework_ontology.OutputTaskPattern)

class FieldMapPattern(EntityPackage):
    """A Pattern used to create Field Maps."""
    def __init__(self, session, title: str, labels: 'list[str]' = [], node_id: str = None):
        super().__init__(session, session.core_ontology.ArchivalInformationUnit, utils.get_field_map_pattern_namespace(), title, labels, node_id)
        self.node.is_a.append(self.session.framework_ontology.FieldMapPattern)

class BaseTemplate(EntityPackage):
    """The Base Class inherited by all other Template classes. This class should not be instanced on it own, instead it is better to instantiate the specific kind of Template needed."""
    def __init__(self,
        session,
        source_pattern: typing.Union[EntityPackage, str] = None,
        source_template: typing.Union[BaseTemplate, str] = None,
        graph: Graph = None,
        namespace: str = None,
        node_id: str = None
    ):
        self.labeled_fields: typing.Dict[str, typing.Dict[str, Field]]= {}
        """ labeled_fields is a dictionary mapping an InformationObject's title to another dictionary containing all of its Fields' titles.
            Essentially it is an index pointing to Fields using first their containing InformationObject's title and then the Field's title.
        """
        self.id_fields: typing.Dict[str, Field] = {}
        """ id_fields is a counterpart to labeled_fields in that they both point to the same set of Fields.
            id_fields simply uses the node_id of the Field as the index to the Field.
        """
        
        if source_pattern is not None:
            pattern = utils.load(session, source_pattern, as_copy=False) if isinstance(source_pattern, str) else source_pattern
            VaipClass = pattern.node.is_a[0]
            super().__init__(session, VaipClass, namespace, pattern.get_title(), pattern.get_labels(), node_id)
            self.node.hasParentPattern = [source_pattern.node]
            self._copy_from_package(pattern)
        elif source_template is not None:
            if isinstance(source_template, str):
                if graph is not None:
                    title, labels = sparql_utils.query_title_and_labels(graph, source_template)
                    vaip_class_str = sparql_utils.query_vaip_core_class(graph, source_template)
                    VaipClass = session.core_ontology[vaip_class_str]
                    super().__init__(session, VaipClass, namespace, title, labels, node_id)
                else:
                    template = utils.load(session, source_template, as_copy=False)
                    VaipClass = template.node.is_a[0]
                    super().__init__(session, VaipClass, namespace, template.get_title(), template.get_labels(), node_id)
                    self._copy_from_package(template)
            else:
                VaipClass = source_template.node.is_a[0]
                super().__init__(session, VaipClass, namespace, source_template.get_title(), source_template.get_labels(), node_id)
                self._copy_from_package(source_template)
    
    @classmethod
    def from_rdf(cls, session, graph, root_iri: str, vaip_type: str, root_node_id: str):
        """Create a Template from an RDF graph.

        Args:
            session (_type_): The Ontology Session.
            graph (_type_): The graph to generate the Template from.
            root_iri (str): The root iri of the graph.
            vaip_type (str): Unused
            root_node_id (str): The node id to append the Template to in the Session.

        Returns:
            Template: The Template created from the RDF Graph. 
        """
        namespace = root_iri.rsplit("/", 2)[0]
        instance = cls(
            session,
            source_template=root_iri,
            graph=graph,
            namespace=namespace,
            node_id=root_node_id
        )
        instance._hydrate_from_rdf(session, graph, root_iri, root_node_id)
        return instance
    
    def _hydrate_from_rdf(self, session, graph, root_iri: str, root_node_id: str):
        super()._hydrate_from_rdf(session, graph, root_iri, root_node_id)
        res = graph.query(f"""
            PREFIX fmk: <http://ncei.noaa.gov/vaip/ontologies/vaip-framework#>
            SELECT ?o
            WHERE {{
                <{root_iri}> fmk:hasParentPattern ?o 
            }}
        """)
        for r in res:
            source_pattern_iri = str(r.o)
            break
        
        # Create a temporary owlready2 instance of the vaip-framework Pattern class, using the parent pattern IRI obtained from query.
        # This is a workaround to avoid loading the entire Pattern into owlready2.
        # owlready2 throws an error if `self.node.hasParentPattern` is assigned to a string; it must be an owlready2 object
        p_split = source_pattern_iri.rsplit("/", 2)
        temp_node_id = p_split[2]
        temp_namespace = session.context.get_ontology(p_split[0]).get_namespace(source_pattern_iri)
        pattern = session.framework_ontology.Pattern(temp_node_id, namespace=temp_namespace)
        self.node.hasParentPattern = [pattern]
        
        for iobj in self.information_objects:
            iobj_title = iobj.get_title()
            setattr(self, snakecase(iobj_title), iobj)
            self.labeled_fields[iobj_title] = {}
            for dobj in iobj.data_objects:
                dobj_title = dobj.get_title()
                dobj_id = dobj.node_id
                setattr(iobj, snakecase(dobj_title), dobj)
                self.id_fields[dobj_id] = dobj
                self.labeled_fields[iobj_title][dobj.get_title()] = dobj
                self.node.hasLiteralField.append(dobj.node)
        
        return self

    def _copy_from_package(self, source_package: EntityPackage):
        fmap = dict([
            (str(self.session.core_ontology.ContentInformationObject), self.set_content),
            (str(self.session.core_ontology.UnitDescription), self.add_description),
            (str(self.session.core_ontology.PackagingInformationObject), self.add_packaging),
            (str(self.session.core_ontology.FixityPreservation), self.add_fixity),
            (str(self.session.core_ontology.AccessRightsPreservation), self.add_access_rights),
            (str(self.session.core_ontology.ContextPreservation), self.add_context),
            (str(self.session.core_ontology.ProvenancePreservation), self.add_provenance),
            (str(self.session.core_ontology.ReferencePreservation), self.add_reference)
        ])
        for iobj in source_package.information_objects:
            iobj_title = iobj.get_title()
            add_func = fmap[str(iobj.node.is_a[0])]
            copied_resource = add_func(iobj_title, iobj.get_labels(), field=None)
            copied_resource.copy_from_information_object(iobj)
            setattr(self, snakecase(iobj_title), copied_resource)
            self.labeled_fields[iobj_title] = {}
            for rep in copied_resource.representations:
                setattr(copied_resource, snakecase(rep.get_title()), rep)
                for dobj in rep.data_objects:
                    dobj_title = dobj.get_title()
                    dobj_id = dobj.node_id
                    setattr(rep, snakecase(dobj_title), dobj)
                    # self.id_fields[dobj_id] = dobj
                    # self.labeled_fields[iobj_title][dobj.get_title()] = dobj
                    self.node.hasLiteralField.append(dobj.node)
            for dobj in copied_resource.data_objects:
                dobj_title = dobj.get_title()
                dobj_id = dobj.node_id
                setattr(copied_resource, snakecase(dobj_title), dobj)
                self.id_fields[dobj_id] = dobj
                self.labeled_fields[iobj_title][dobj.get_title()] = dobj
                self.node.hasLiteralField.append(dobj.node)
    
    ### Commenting these out to have an example of how to recursively iterate our vAIP relationships

    # def _copy_from_pattern_old(self):
    #     copied_nodes = dict([(self.pattern.node.name, self.pattern.node)])
    #     self.deep_copy_owlready(self.node, self.pattern.node, copied_nodes)
    #     return self.node
    
    # def deep_copy_owlready(self, copy_to_node, source_node, visited_nodes: dict):
    #     for predicate in source_node.get_properties():
    #         for obj in predicate[source_node]:
    #             if (type(obj) != str):
    #                 VaipClass = type(obj)
    #                 if (obj.name not in visited_nodes.keys()):
    #                     visited_nodes[obj.name] = obj
    #                     copy = VaipClass(utils.generate_node_id(), namespace=self.namespace)
    #                     self.deep_copy_owlready(copy, obj, visited_nodes)
    #                 else:
    #                     copy = visited_nodes[obj.name]
    #             else:
    #                 copy = obj
    #             if (predicate.is_functional_for(source_node)):
    #                 setattr(copy_to_node, predicate.name, copy)
    #             else:
    #                 setattr(copy_to_node, predicate.name, [copy])

    def get_fields(self):
        """Get all Labeled Fields from the Template

        Returns:
            Dict[str,Dict[str,Field]]: A dictionary of all labeled Fields for the template.
        """
        # TODO: this needs to a return a more informative and UX-friendly structure
        return self.labeled_fields

    def get_field(self, field_id: str):
        """Get a specific field from a template based on Title. 

        Args:
            field_id (str): The Title/Primary Label of the desired Field.

        Returns:
            Field: The Field with the matching Title.
        """
        return self.id_fields[field_id]

    def _find_io_field(self, IOClass, io_title: str, field_title: str):
        for iobj in self.information_objects:
            if iobj.node.is_a[0] is IOClass and iobj.get_title() == io_title:
                fields = self.labeled_fields[io_title]
                for f in fields.keys():
                    if f == field_title:
                        return fields[f]
        return None

    def find_description_field(self, description: str = None, field: str = None):
        """Find a Labeled field of a Description Information Object

        Args:
            description (str, optional): Title of the Decription Information Oject. Defaults to None.
            field (str, optional): Title of the labeled field. Defaults to None.

        Returns:
            Field: The desired Field object
        """
        return self._find_io_field(self.session.core_ontology.UnitDescription, description, field)
    
    def find_content_field(self, content: str = None, field: str = None):
        """Find a Labeled field of a Content Information Object

        Args:
            description (str, optional): Title of the Content Information Oject. Defaults to None.
            field (str, optional): Title of the labeled field. Defaults to None.

        Returns:
            Field: The desired Field object
        """
        return self._find_io_field(self.session.core_ontology.ContentInformationObject, content, field)

    def find_packaging_field(self, packaging: str = None, field: str = None):
        """Find a Labeled field of a Packaging Information Object

        Args:
            description (str, optional): Title of the Packaging Information Oject. Defaults to None.
            field (str, optional): Title of the labeled field. Defaults to None.

        Returns:
            Field: The desired Field object
        """
        return self._find_io_field(self.session.core_ontology.PackagingInformationObject, packaging, field)

    def find_fixity_field(self, fixity: str = None, field: str = None):
        """Find a Labeled field of a Packaging Information Object

        Args:
            description (str, optional): Title of the Packaging Information Oject. Defaults to None.
            field (str, optional): Title of the labeled field. Defaults to None.

        Returns:
            Field: The desired Field object
        """
        return self._find_io_field(self.session.core_ontology.FixityPreservation, fixity, field)

    def find_access_rights_field(self, access_rights: str = None, field: str = None):
        """Find a Labeled field of a Access Rights Information Object

        Args:
            description (str, optional): Title of the Access Rights Information Oject. Defaults to None.
            field (str, optional): Title of the labeled field. Defaults to None.

        Returns:
            Field: The desired Field object
        """
        return self._find_io_field(self.session.core_ontology.AccessRightsPreservation, access_rights, field)

    def find_context_field(self, context: str = None, field: str = None):
        """Find a Labeled field of a Context Information Object

        Args:
            description (str, optional): Title of the Context Information Oject. Defaults to None.
            field (str, optional): Title of the labeled field. Defaults to None.

        Returns:
            Field: The desired Field object
        """
        return self._find_io_field(self.session.core_ontology.ContextPreservation, context, field)

    def find_provenance_field(self, provenance: str = None, field: str = None):
        """Find a Labeled field of a Provenance Information Object

        Args:
            description (str, optional): Title of the Provenance Information Oject. Defaults to None.
            field (str, optional): Title of the labeled field. Defaults to None.

        Returns:
            Field: The desired Field object
        """
        return self._find_io_field(self.session.core_ontology.ProvenancePreservation, provenance, field)

    def find_reference_field(self, reference: str = None, field: str = None):
        """Find a Labeled field of a Reference Information Object

        Args:
            description (str, optional): Title of the Reference Information Oject. Defaults to None.
            field (str, optional): Title of the labeled field. Defaults to None.

        Returns:
            Field: The desired Field object
        """
        return self._find_io_field(self.session.core_ontology.ReferencePreservation, reference, field)

    def set_field(self, field_id: str = None, value: str = None):
        """Set the value of a Field

        Args:
            field_id (str, optional): Title of the target Field. Defaults to None.
            value (str, optional): The Value to set the field's value to. Defaults to None.
        """
        data_field = self.get_field(field_id)
        data_field.set_value(value)
    
    def set_description_field(self, description: str = None, field: str = None, value: str = None):
        """Set the value of a Description Information Object

        Args:
            description (str, optional): The title of the Description Information Object. Defaults to None.
            field (str, optional): Title of the Field to set the value for. Defaults to None.
            value (str, optional): The value to set the Field value to. Defaults to None.
        """
        data_field = self.find_description_field(description, field)
        data_field.set_value(value)
    
    def set_content_field(self, content: str = None, field: str = None, value: str = None):
        """Set the value of a Content Information Object

        Args:
            description (str, optional): The title of the Content Information Object. Defaults to None.
            field (str, optional): Title of the Field to set the value for. Defaults to None.
            value (str, optional): The value to set the Field value to. Defaults to None.
        """
        data_field = self.find_content_field(content, field)
        data_field.set_value(value)

    def set_packaging_field(self, packaging: str = None, field: str = None, value: str = None):
        """Set the value of a Packaging Information Object

        Args:
            description (str, optional): The title of the Packaging Information Object. Defaults to None.
            field (str, optional): Title of the Field to set the value for. Defaults to None.
            value (str, optional): The value to set the Field value to. Defaults to None.
        """
        data_field = self.find_packaging_field(packaging, field)
        data_field.set_value(value)
    
    def set_fixity_field(self, fixity: str = None, field: str = None, value: str = None):
        """Set the value of a Fixity Information Object

        Args:
            description (str, optional): The title of the Fixity Information Object. Defaults to None.
            field (str, optional): Title of the Field to set the value for. Defaults to None.
            value (str, optional): The value to set the Field value to. Defaults to None.
        """
        data_field = self.find_fixity_field(fixity, field)
        data_field.set_value(value)

    def set_access_rights_field(self, access_rights: str = None, field: str = None, value: str = None):
        """Set the value of a Access Rights Information Object

        Args:
            description (str, optional): The title of the Access Rights Information Object. Defaults to None.
            field (str, optional): Title of the Field to set the value for. Defaults to None.
            value (str, optional): The value to set the Field value to. Defaults to None.
        """
        data_field = self.find_access_rights_field(access_rights, field)
        data_field.set_value(value)

    def set_context_field(self, context: str = None, field: str = None, value: str = None):
        """Set the value of a Content Information Object

        Args:
            description (str, optional): The title of the Content Information Object. Defaults to None.
            field (str, optional): Title of the Field to set the value for. Defaults to None.
            value (str, optional): The value to set the Field value to. Defaults to None.
        """
        data_field = self.find_context_field(context, field)
        data_field.set_value(value)

    def set_provenance_field(self, provenance: str = None, field: str = None, value: str = None):
        """Set the value of a Provenance Information Object

        Args:
            description (str, optional): The title of the Provenance Information Object. Defaults to None.
            field (str, optional): Title of the Field to set the value for. Defaults to None.
            value (str, optional): The value to set the Field value to. Defaults to None.
        """
        data_field = self.find_provenance_field(provenance, field)
        data_field.set_value(value)

    def set_reference_field(self, reference: str = None, field: str = None, value: str = None):
        """Set the value of a Reference Information Object

        Args:
            description (str, optional): The title of the Reference Information Object. Defaults to None.
            field (str, optional): Title of the Field to set the value for. Defaults to None.
            value (str, optional): The value to set the Field value to. Defaults to None.
        """
        data_field = self.find_reference_field(reference, field)
        data_field.set_value(value)

class IdentityStorageTemplate(BaseTemplate):
    """Identity Storage Template\n
    An Identity Storage unit represents the target for a given Identity Task. Identity Storage is meant to hold output from Tasks that perform identification of computational requests.
    """
    def __init__(self,
        session,
        source_pattern: typing.Union[IdentityStoragePattern, str] = None,
        source_template: typing.Union[IdentityStorageTemplate, str] = None,
        graph: Graph = None,
        namespace: str = utils.get_aiu_template_namespace(),
        node_id: str = None
    ):
        super().__init__(
            session,
            source_pattern=source_pattern,
            source_template=source_template,
            graph=graph,
            namespace=namespace,
            node_id=node_id
        )
        self.node.is_a.append(self.session.framework_ontology.IdentityStorageTemplate)

class OutputStorageTemplate(BaseTemplate):
    """ Output Storage Template\n
    Output Storage represents the target container for Output Tasks. Output Storage contextualizes outbound (unidirectional) resolutions of a request - sending data to an Endpoint via a specific Connection. This might be as simple as output from a &apos;pass&apos; output task that aggregates and resolves a user request, or might represent some delivery of data or information to an external interface like an email address via specific connection configuration.

    """
    def __init__(self,
        session,
        source_pattern: typing.Union[OutputStoragePattern, str] = None,
        source_template: typing.Union[OutputStorageTemplate, str] = None,
        graph: Graph = None,
        namespace: str = utils.get_dip_template_namespace(),
        node_id: str = None
    ):
        super().__init__(
            session,
            source_pattern=source_pattern,
            source_template=source_template,
            graph=graph,
            namespace=namespace,
            node_id=node_id
        )
        self.node.is_a.append(self.session.framework_ontology.OutputStorageTemplate)

class UBLTemplate(BaseTemplate):
    """User Business Logic Template\n
    User Business Logic (UBL) represents a task-bound configuration container for holding some user provided computationally capable action - an API call, a service call, a lambda or Docker  containing code, a step function, etc. UBL takes in a flat set of values and passes out a flat set of values. The UBL should provide either in template or at runtime enough information to successfully trigger and resolve a call to the specified user logic. The UBL as a construct avoids placing burden on the user to leverage hardcoded message adapters or other intrusive mechanisms.
    """
    def __init__(self,
        session,
        source_pattern: typing.Union[UBLPattern, str] = None,
        source_template: typing.Union[UBLTemplate, str] = None,
        graph: Graph = None,
        namespace: str = utils.get_ubl_template_namespace(),
        node_id: str = None
    ):
        if source_pattern is None and source_template is None:
            source_pattern = session.get_system_pattern("ubl")
        super().__init__(
            session,
            source_pattern=source_pattern,
            source_template=source_template,
            graph=graph,
            namespace=namespace,
            node_id=node_id
        )
        self.node.is_a.append(self.session.framework_ontology.UBLTemplate)
        self.field_set = self.content # somewhat redundant but this accomodates any UBL pattern changes that might impact the fields
        self.input_field_pattern = None # TODO
        self.output_field_pattern = None # TODO
        self.inputs = types.SimpleNamespace()
        self.outputs = types.SimpleNamespace()
        
    def _hydrate_from_rdf(self, session, graph, root_iri, root_node_id):
        super()._hydrate_from_rdf(session, graph, root_iri, root_node_id)
        # TODO: populate self.inputs and self.outputs
        return self

    def add_input(self, title: str = None, type: str = "string", is_required: bool = True, value: str = utils.generate_placeholder()):
        """Add an input literal field to the UBL Template

        Args:
            title (str, optional): Title. Defaults to None.
            type (str, optional): The namespace class type.. Defaults to "string".
            is_required (bool, optional): Is the value Required?. Defaults to True.
            value (str, optional): The default value for the input field. Defaults to utils.generate_placeholder().

        Returns:
            LiteralField: The new input field.
        """
        namespace = "http://www.w3.org/2001/XMLSchema#"
        namespace_class = type
        field = LiteralField(self.field_set, title, ['input field'], value, namespace, namespace_class, is_required)
        # TODO: Refactor adding this explicitly to self.field_set
        self.field_set.data_objects.append(field)
        self.field_set.node.hasDataObject.append(field.node)
        self.node.hasInputField.append(field.node)
        setattr(self.inputs, snakecase(field.get_title()), field)
        return field

    def add_output(self, title: str = None, type: str = "string", is_required: bool = True, value: str = utils.generate_placeholder()):
        """Add an output literal field to the UBL Template.

        Args:
            title (str, optional): Title of the output field. Defaults to None.
            type (str, optional): Namespace class of the output field. Defaults to "string".
            is_required (bool, optional): Is the value required? Defaults to True.
            value (str, optional): The default value for the field. Defaults to utils.generate_placeholder().

        Returns:
            LiterlField: The new output field
        """
        namespace = "http://www.w3.org/2001/XMLSchema#"
        namespace_class = type
        field = LiteralField(self.field_set, title, ['output field'], value, namespace, namespace_class, is_required)
        # TODO: Refactor adding this explicitly to self.field_set
        self.field_set.data_objects.append(field)
        self.field_set.node.hasDataObject.append(field.node)
        self.node.hasOutputField.append(field.node)
        setattr(self.outputs, snakecase(field.get_title()), field)
        return field

class FieldMapTemplate(BaseTemplate):
    """Field Map Template\n
    A Field Map connects a UBL output to a Storage (Target). Field maps contain flat key to key pairs (UBL output key to Storage input key). As a UBL completes within an executing task, it should produce and pass out a map of valued keys, that will be used in conjunction with the key to key Field Map to populate the Storage Target placeholder values.
    """
    def __init__(self,
        session,
        source_pattern: typing.Union[FieldMapPattern, str] = None,
        source_template: typing.Union[FieldMapTemplate, str] = None,
        graph: Graph = None,
        namespace: str = utils.get_field_map_template_namespace(),
        node_id: str = None
    ):
        if source_pattern is None and source_template is None:
            source_pattern = session.get_system_pattern("field_map")
        super().__init__(
            session,
            source_pattern=source_pattern,
            source_template=source_template,
            graph=graph,
            namespace=namespace,
            node_id=node_id
        )
        self.node.is_a.append(self.session.framework_ontology.FieldMapTemplate)
        self.entries = set()
    
    def _hydrate_from_rdf(self, session, graph, root_iri, root_node_id):
        super()._hydrate_from_rdf(session, graph, root_iri, root_node_id)
        # TODO: populate self.entries
        return self

    def add_entry(self, source_field: Field, target_field: Field):
        """Adds a Field Map Entry to the Field Map\n
        A Field Map Entry is a key to key mapping between a source (upstream) key and a target (downstream) key. Field Map Entries belong to Field Maps.
        Args:
            source_field (Field): The upstream field.
            target_field (Field): The downstream field.
        """
        entry = FieldMapEntry(self.session, self.namespace, source_field=source_field.node, target_field=target_field.node)
        self.node.hasFieldMapEntry.append(entry.node)
        self.entries.add(entry)
       
        # TODO: Flesh out the FieldMapEntry representation in the vaip-core ontology
        # This should be mae its own class as well whe fleshed out.
        self.content.add_link_field(utils.generate_placeholder(), labels=["source field"], value=source_field.node.iri)
        self.content.add_link_field(utils.generate_placeholder(), labels=["target field"], value=target_field.node.iri)
    
    def find_entry(self, **kwargs):
        return next(self.__iter_entry(**kwargs))
    def find_all_entries(self, **kwargs):
        return list(self.__iter_entry(**kwargs))
    def __iter_entry(self, **kwargs):
        return (entry for entry in self.entries if entry.match(**kwargs))


    
    def get_source_fields(self):
        sourceFields=[]
        for entry in self.entries:
            #print(f"Entry: Source:{entry.node.hasSourceField} Target:{entry.node.hasTargetField}\n")
            for sourceField in entry.node.hasSourceField:
                sourceFields.append(sourceField)
        return sourceFields
    def get_target_fields(self):
        targetFields=[]
        for entry in self.entries:
            #print(f"Entry: Source:{entry.node.hasSourceField} Target:{entry.node.hasTargetField}\n")
            for targetField in entry.node.hasTargetField:
                targetFields.append(targetField)
        return targetFields

class FieldMapEntry(VaipResource):
    def __init__(self, session, namespace, source_field, target_field):
        super().__init__(session=session)
        self.namespace = namespace
        self.node = session.framework_ontology.FieldMapEntry(self.node_id, namespace=self.namespace)
        self.set_title("Field Map Entry")
        
        self.node.hasSourceField.append(source_field)
        self.node.hasTargetField.append(target_field)

    def __repr__(self):
        return self
    def match(self, **kwargs):
        return all(getattr(self.node, key) == val for (key, val) in kwargs.items())

class BaseTask(BaseTemplate):
    """The base Task Class that all other Task classes inherit.\n
    A Task represents a computational container and component of a Process. Tasks contain an interface to arbitrary user provided logic (UBL), a storage target for the information returned by the UBL, and a key to key map that links UBL to the storage target. Tasks are further classified as Input, Identity,Transformation, and Output, allowing conditional flow rules and fine-grained composition of Processes.
    """
    def __init__(self,
        session,
        source_pattern: typing.Union[EntityPackage, str] = None,
        source_template: typing.Union[BaseTemplate, str] = None,
        graph: Graph = None,
        field_map: FieldMapTemplate = None,
        target: BaseTemplate = None,
        purpose: str = None,
        utility: str = None,
        long_running_mode: bool = False,
        direct_trigger_mode: bool = False,
        persistence_mode: str = "s3",
        namespace: str = None,
        node_id: str = None
    ):
        if source_pattern is None and source_template is None:
            raise Exception("BaseTask was not given a source pattern or source template")
        super().__init__(
            session,
            source_pattern=source_pattern,
            source_template=source_template,
            graph=graph,
            namespace=namespace,
            node_id=node_id
        )
        if field_map is not None:
            self.set_field_map(field_map)
            
        if graph is None:
            if field_map is None: self.set_field_map(FieldMapTemplate(session, namespace=namespace))
            if target: self.set_target(target)
            if purpose: self.set_purpose(purpose)
            if utility: self.set_utility(utility)
            if persistence_mode: self.set_persistence_mode(persistence_mode)
            if direct_trigger_mode is not None: self.set_direct_trigger_mode(direct_trigger_mode)
            if long_running_mode is not None: self.set_long_running_mode(long_running_mode)
        
        # TODO: Fill out the system Task pattern with default values for things like semantic and structure representation
        # ie. the "format" and "semantics" of persistence mode, operating mode, purpose, general utility

    def _hydrate_from_rdf(self, session, graph, root_iri: str, root_node_id: str):
        """Populate a BaseTask from an RDF graph.

        Args:
            session (_type_): The Ontology Session.
            graph (_type_): The graph to generate the Task from.
            root_iri (str): The root iri of the graph.
            root_node_id (str): The node id to append the Task to in the Session.

        Returns:
            Task: The Task updated from the RDF Graph. 
        """
        super()._hydrate_from_rdf(session, graph, root_iri, root_node_id)
        namespace = root_iri.rsplit("/", 2)[0]
        res = graph.query(f"""
            PREFIX vaip: <https://ncei.noaa.gov/vaip/ontologies/vaip-core#>
            PREFIX fmk: <http://ncei.noaa.gov/vaip/ontologies/vaip-framework#>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            SELECT ?field_map_iri ?purpose ?utility ?persistence ?operation ?trigger
            WHERE {{
                <{root_iri}> fmk:hasFieldMap ?field_map_iri .
                
                <{root_iri}> vaip:describedBy ?desc .
                ?desc skos:prefLabel "Purpose" .
                ?desc vaip:hasDataObject/fmk:hasValue ?purpose .
                
                <{root_iri}> vaip:describedBy ?desc2 .
                ?desc2 skos:prefLabel "General Utility" .
                ?desc2 vaip:hasDataObject/fmk:hasValue ?utility .
                
                <{root_iri}> vaip:hasContext ?ctx .
                ?ctx skos:prefLabel "Persistence Mode" .
                ?ctx vaip:hasDataObject/fmk:hasValue ?persistence .
                
                <{root_iri}> vaip:hasContext ?ctx2 .
                ?ctx2 skos:prefLabel "Operating Mode" .
                ?ctx2 vaip:hasDataObject/fmk:hasValue ?operation .
                
                OPTIONAL {{
                    <{root_iri}> vaip:hasContext ?ctx3 .
                    ?ctx3 skos:prefLabel "Downstream Trigger Mode" .
                    ?ctx3 vaip:hasDataObject/fmk:hasValue ?trigger .
                }}
            }}
        """)
            
        for r in res:
            purpose = str(r.purpose)
            utility = str(r.utility)
            persistence_mode = str(r.persistence)
            long_running_mode = False if str(r.operation) == "EXPRESS" else True
            direct_trigger_mode = False if str(r.trigger) == "INDIRECT" else True
            iri = str(r.field_map_iri)
            node_id = None if root_node_id is None else iri.rsplit("/", 1)[1]
            field_map = FieldMapTemplate.from_rdf(session, graph, iri, "ArchivalInformationUnit", node_id)
            break
        
        self.set_field_map(field_map)
        self.set_purpose(purpose)
        self.set_utility(utility)
        self.set_persistence_mode(persistence_mode)
        self.set_direct_trigger_mode(direct_trigger_mode)
        self.set_long_running_mode(long_running_mode)
        return self
    
    def deploy(self):
        target_response = self.session.deploy(self.target)
        return {
            self.target.node.iri: target_response
        }
        
    def set_field_map(self, field_map):
        """Set the FieldMap of the task.

        Args:
            field_map (FieldMapTemplate): The FieldMapTemplate to use for mapping fields.

        Returns:
             Task: Returns the updated Task.
        """
        self.field_mapper = field_map
        self.node.hasFieldMap = [self.field_mapper.node]
        self.set_content_field(content="Content", field="Field Map", value=self.field_mapper.node.iri)
        return self
        
    def match_field(self, ubl_field: Field, target_field: Field):
        """Map a upstream Field to a Downsteam Field

        Args:
            ubl_field (Field): The upstream/source field
            target_field (Field): The downstream/target field.

        Returns:
            Task: Returns the updated Task.
        """
        self.field_mapper.add_entry(ubl_field, target_field)
        return self
    
    def set_target(self, target: BaseTemplate):
        """Set the target of the task. This us usually a Storage Template.

        Args:
            target (BaseTemplate): The Template to target.

        Returns:
             Task: Returns the updated Task.
        """
        self.target = target
        self.set_content_field(content="Content", field="Storage Template", value=target.node.iri)
        return self

    def set_purpose(self, purpose: str):
        """Set the description of the purpose of the Task. This is metadata to help describe the task.

        Args:
            purpose (str): A description of the purpose of the Task.

        Returns:
            BaseTask: The updated Task.
        """
        self.purpose_description = purpose
        self.set_description_field(description="Purpose", field="Description", value=purpose)
        return self

    def set_utility(self, utility: str):
        """Set the description of the utility of the Task. This is metadata to help describe the task.

        Args:
            utility (str): A description of the utility of the Task.

        Returns:
            BaseTask: The updated Task.
        """
        self.utility_description = utility
        self.set_description_field(description="General Utility", field="Description", value=utility)
        return self

    def set_persistence_mode(self, persistence: str):
        """Set the description of the data persistance mode of the task in the Cloud.

        Args:
            persistence (str): Ex.:'Hot', 'UltraWarm'

        Returns:
            BaseTask: The updated Task.
        """
        self.persistence = persistence
        self.set_context_field(context="Persistence Mode", field="Value", value=persistence)
        return self

    def set_long_running_mode(self, long_running_mode: bool):
        """Set this Task to execute as a long running task or not. Default is False.
        Tasks can be defined either as long or short running. The difference is only in their maximum allowed duration of execution.
        
        Args:
            long_running_mode (bool): True or False

        Returns:
            BaseTask: The updated Task
        """
        self.long_running = long_running_mode
        value = "STANDARD" if long_running_mode else "EXPRESS"
        self.set_context_field(context="Operating Mode", field="Value", value=value)
        return self
        
    def set_direct_trigger_mode(self, direct_trigger_mode: bool):
        """Set this Task's downstream Task triggering mode as direct or not. Default is False.
        When a Process triggers the downstream Tasks of a currently running Task, it will use
        either a direct trigger or an indrect trigger mechanism. The main difference is the
        latency between the trigger event and the start of the next downstream Task execution.
        
        Args:
            direct_trigger_mode (bool): True or False

        Returns:
            BaseTask: The updated Task
        """
        self.direct_trigger = direct_trigger_mode
        value = "DIRECT" if direct_trigger_mode else "INDIRECT"
        self.set_context_field(context="Downstream Trigger Mode", field="Value", value=value)
        return self
    
    def get_output_fields(self):
        return self.ubl.outputs.__dict__
    def get_input_fields(self):
        return self.ubl.inputs.__dict__
    
    #UBL doesnt exist in this context, but exists in AIU and AIC Task children
    def validate_output_fields(self):
        #print("Validating Outputs")
        sourceFields = self.field_mapper.get_source_fields()
        for fieldOutputKey in self.ubl.outputs.__dict__:
            fieldOutputValue = self.ubl.outputs.__getattribute__(fieldOutputKey)
            #print(f"Output Label {fieldOutputKey} isRequired:{fieldOutputValue.required} Node:{fieldOutputValue.node}")
            if( fieldOutputValue.required != fieldOutputValue.node.isRequired[0]):
                raise Exception(f"Task titled {self.get_title()}: Task output field {fieldOutputKey} required value is not in sync. {fieldOutputValue.required} {fieldOutputValue.node.isRequired}")
            if(fieldOutputValue.required ): #we need to check both so as to prevent a bad state. This could be worth validation functions
                if(sourceFields.__contains__(fieldOutputValue.node)):
                    pass
                    #print(f"Task {self.get_title()}: Output field {fieldOutputKey} mapped")
                else:
                    raise Exception(f"Task titled {self.get_title()}: Required Task output field {fieldOutputKey} NOT mapped")
    #UBL doesnt exist in this context, but exists in all children
    def validate_input_fields(self):
        #print("Validating Inputs")
        for fieldInputKey in self.ubl.inputs.__dict__:
            fieldInputValue = self.ubl.inputs.__getattribute__(fieldInputKey)
            #print(f"Input Label {fieldInputKey} isRequired:{fieldInputValue.required} Node:{fieldInputValue.node}")
            if( fieldInputValue.required != fieldInputValue.node.isRequired[0]):
                raise Exception(f"Task {self.get_title()}: Task input field {fieldInputKey} required value is not in sync.")
           
            if(fieldInputValue.required): #we need to check both so as to prevent a bad state. This could be worth validation functions
                found_entries:list[FieldMapEntry]= self.field_mapper.find_all_entries(hasSourceField=[fieldInputValue.node])
                if(found_entries.__len__()==0):
                    raise Exception(f"Task {self.get_title()}: Required Task input field {fieldInputKey} NOT mapped")
                #Not sure if this could happen unless intentionally, but its covered
                for entry in found_entries:
                   if(len(entry.node.hasTargetField) ==0):
                        raise Exception(f"Task {self.get_title()}: Required Task input field {fieldInputKey} is mapped, but has no Target Field")
                


class IdentityTaskTemplate(BaseTask):
    """Identity Task Template\n
    A Task represents a computational container and component of a Process. Tasks contain an interface to arbitrary user provided logic (UBL), a storage target for the information returned by the UBL, and a key to key map that links UBL to the storage target. Tasks are further classified as Input, Identity,Transformation, and Output, allowing conditional flow rules and fine-grained composition of Processes.\n
    A Template represents the configuration layer of the system. Templates derive from Patterns, and may be partially-valued structures that are deep-copies of their Pattern parents. As deep-copies of Patterns, Templates conform to the implemented Reference Model, and may have a relationship to their parent Pattern. Templates generally live within configurations that consist of other Templates. Templates are used at runtime to produce fully-valued Records.
    """
    def __init__(self,
        session,
        source_pattern: typing.Union[IdentityTaskPattern, str] = None,
        source_template: typing.Union[IdentityTaskTemplate, str] = None,
        graph: Graph = None,
        field_map: FieldMapTemplate = None,
        target: IdentityStorageTemplate = None,
        ubl: typing.Union[UBLTemplate, str] = None,
        purpose: str = None,
        utility: str = None,
        long_running_mode: bool = False,
        direct_trigger_mode: bool = False,
        persistence_mode: str = "s3", 
        namespace: str = None,
        node_id: str = None
    ):
        if source_pattern is None and source_template is None:
            source_pattern = session.get_system_pattern("aiu_task")
        super().__init__(session,
            source_pattern=source_pattern,
            source_template=source_template,
            graph=graph,
            field_map=field_map,
            target=target,
            purpose=purpose,
            utility=utility,
            long_running_mode=long_running_mode,
            direct_trigger_mode=direct_trigger_mode,
            persistence_mode=persistence_mode,
            namespace=namespace,
            node_id=node_id
        )
        self.node.is_a.append(self.session.framework_ontology.IdentityTaskTemplate)
        if ubl: self.set_ubl(ubl)
        
    def _hydrate_from_rdf(self, session, graph, root_iri, root_node_id):
        super()._hydrate_from_rdf(session, graph, root_iri, root_node_id)
        res = graph.query(f"""
            PREFIX vaip: <https://ncei.noaa.gov/vaip/ontologies/vaip-core#>
            PREFIX fmk: <http://ncei.noaa.gov/vaip/ontologies/vaip-framework#>
            SELECT ?target ?ubl
            WHERE {{
                <{root_iri}> vaip:hasContentInformation ?content .
                ?content skos:prefLabel "Content" .
                ?content vaip:hasDataObject ?data .
                ?data skos:prefLabel "Storage Template" .
                ?data fmk:hasValue ?target .
                
                <{root_iri}> fmk:hasUBLTemplate ?ubl
            }}
        """)
        for r in res:
            iri = str(r.ubl)
            node_id = None if root_node_id is None else iri.rsplit("/", 1)[1]
            ubl = UBLTemplate.from_rdf(session, graph, iri, "ArchivalInformationUnit", node_id)
            self.set_ubl(ubl)
            
            target_iri = str(r.target)
            target = utils.load(session, iri=target_iri, as_copy=False)
            self.set_target(target)
            break
        
        return self

    def set_target(self, target: IdentityStorageTemplate):
        """Set the target Identity Storage Template

        Args:
            target (IdentityStorageTemplate): The desired Identity Storage Template 

        Returns:
            IdentityTaskTemplate: The updated Task Template
        """
        super().set_target(target)
        self.node.hasIdentityStorageTemplate.append(target.node)
        return self
    
    def set_ubl(self, ubl: typing.Union[UBLTemplate, str]):
        """Sets the User Business Logic Template for the Identity Task Template.

        Args:
            ubl (typing.Union[UBLTemplate, str]): The desired UBLTemplate or IRI of a UBL Template

        Returns:
            IdentityTaskTemplate: The updated Task Template
        """
        self.ubl = ubl
        if isinstance(ubl, str):
            self.set_content_field(content="Content", field="UBL", value=ubl)
            self.node.hasUBLTemplate.append(ubl)
        else:
            self.set_content_field(content="Content", field="UBL", value=ubl.node.iri)
            self.node.hasUBLTemplate.append(ubl.node)
        return self
    
   

class TransformationTaskTemplate(BaseTask):
    """Transformation Task Template\n
    A Task represents a computational container and component of a Process. Tasks contain an interface to arbitrary user provided logic (UBL), a storage target for the information returned by the UBL, and a key to key map that links UBL to the storage target. Tasks are further classified as Input, Identity,Transformation, and Output, allowing conditional flow rules and fine-grained composition of Processes.\n
    A Template represents the configuration layer of the system. Templates derive from Patterns, and may be partially-valued structures that are deep-copies of their Pattern parents. As deep-copies of Patterns, Templates conform to the implemented Reference Model, and may have a relationship to their parent Pattern. Templates generally live within configurations that consist of other Templates. Templates are used at runtime to produce fully-valued Records.
    """
    def __init__(self,
        session,
        source_pattern: typing.Union[TransformationTaskPattern, str] = None,
        source_template: typing.Union[TransformationTaskTemplate, str] = None,
        graph: Graph = None,
        field_map: FieldMapTemplate = None,
        target: MemberDescriptionTemplate = None,
        aic_template: TransformationStorageTemplate = None,
        ubl: typing.Union[UBLTemplate, str] = None,
        purpose: str = None,
        utility: str = None,
        long_running_mode: bool = False,
        direct_trigger_mode: bool = False,
        persistence_mode: str = "s3", 
        namespace: str = None,
        node_id: str = None
    ):
        if source_pattern is None and source_template is None:
            source_pattern = session.get_system_pattern("aic_task")
        super().__init__(session,
            source_pattern=source_pattern,
            source_template=source_template,
            graph=graph,
            field_map=field_map,
            target=target,
            purpose=purpose,
            utility=utility,
            persistence_mode=persistence_mode,
            long_running_mode=long_running_mode,
            direct_trigger_mode=direct_trigger_mode,
            namespace=namespace,
            node_id=node_id
        )
        self.node.is_a.append(self.session.framework_ontology.TransformationTaskTemplate)
        
        if ubl: self.set_ubl(ubl)
        if aic_template: self.set_aic_template(aic_template)
        
        self.aic_record = None

    def _hydrate_from_rdf(self, session, graph, root_iri, root_node_id):
        super()._hydrate_from_rdf(session, graph, root_iri, root_node_id)
        res = graph.query(f"""
            PREFIX vaip: <https://ncei.noaa.gov/vaip/ontologies/vaip-core#>
            PREFIX fmk: <http://ncei.noaa.gov/vaip/ontologies/vaip-framework#>
            SELECT ?target ?ubl
            WHERE {{
                <{root_iri}> vaip:hasContentInformation ?content .
                ?content skos:prefLabel "Content" .
                ?content vaip:hasDataObject ?data .
                ?data skos:prefLabel "Storage Template" .
                ?data fmk:hasValue ?target .
                
                <{root_iri}> fmk:hasUBLTemplate ?ubl
            }}
        """)
        for r in res:
            iri = str(r.ubl)
            node_id = None if root_node_id is None else iri.rsplit("/", 1)[1]
            ubl = UBLTemplate.from_rdf(session, graph, iri, "ArchivalInformationUnit", node_id)
            self.set_ubl(ubl)
            
            target_iri = str(r.target)
            target = utils.load(session, iri=target_iri, as_copy=False)
            self.set_target(target)
            break
        
        return self
    
    def set_target(self, target: MemberDescriptionTemplate):
        """Set the target Member Description Storage Template

        Args:
            target (MemberDescriptionTemplate): The desired Member Description Storage Template 

        Returns:
            TransformationTaskTemplate: The updated Task Template
        """
        super().set_target(target)
        self.node.hasMemberDescriptionTemplate.append(target.node)
        return self
    
    def set_ubl(self, ubl: typing.Union[UBLTemplate, str]):
        """Sets the User Business Logic Template for the Transformation Task Template.

        Args:
            ubl (typing.Union[UBLTemplate, str]): The desired Transformation UBLTemplate or IRI of a UBL Template

        Returns:
            TransformationTaskTemplate: The updated Task Template
        """
        self.ubl = ubl
        if isinstance(ubl, str):
            self.set_content_field(content="Content", field="UBL", value=ubl)
            self.node.hasUBLTemplate.append(ubl)
        else:
            self.set_content_field(content="Content", field="UBL", value=ubl.node.iri)
            self.node.hasUBLTemplate.append(ubl.node)
        return self
    
    def set_aic_template(self, aic_template: TransformationStorageTemplate):
        self.aic_template = aic_template
        self.node.hasTransformationStorageTemplate = [aic_template.node]
        return self
    
    def set_aic_record(self, aic_record: TransformationStorageRecord):
        self.aic_record = aic_record
        self.node.hasTransformationStorageRecord = [aic_record.node]
        return self
        
    def deploy(self):
        target_response = self.target.deploy()
        # TODO: This logic is only temporary. The creation of the TransformationStorageRecord
        # should be contained as UBL of a ProcessTemplate that deploys this TransformationTaskTemplate
        aic_record = TransformationStorageRecord(self.session, self.aic_template)
        self.set_aic_record(aic_record)
        aic_record_response = self.aic_record.deploy()
        return {
            self.target.node.iri: target_response,
            self.aic_record.node.iri: aic_record_response
        }

class OutputTaskTemplate(BaseTask):
    """Output Task Template\n
    A Task represents a computational container and component of a Process. Tasks contain an interface to arbitrary user provided logic (UBL), a storage target for the information returned by the UBL, and a key to key map that links UBL to the storage target. Tasks are further classified as Input, Identity,Transformation, and Output, allowing conditional flow rules and fine-grained composition of Processes.\n
    A Template represents the configuration layer of the system. Templates derive from Patterns, and may be partially-valued structures that are deep-copies of their Pattern parents. As deep-copies of Patterns, Templates conform to the implemented Reference Model, and may have a relationship to their parent Pattern. Templates generally live within configurations that consist of other Templates. Templates are used at runtime to produce fully-valued Records.
    """
    def __init__(self,
        session,
        source_pattern: typing.Union[OutputTaskPattern, str] = None,
        source_template: typing.Union[OutputTaskTemplate, str] = None,
        graph: Graph = None,
        field_map: FieldMapTemplate = None,
        target: OutputStorageTemplate = None,
        transform_data_ubl: typing.Union[UBLTemplate, str] = None,
        deliver_data_ubl: typing.Union[UBLTemplate, str] = None,
        purpose: str = None,
        utility: str = None,
        long_running_mode: bool = False,
        direct_trigger_mode: bool = False,
        persistence_mode: str = "s3", 
        namespace: str = None,
        node_id: str = None
    ):
        if source_pattern is None and source_template is None:
            source_pattern = session.get_system_pattern("dip_task")
        super().__init__(session,
            source_pattern=source_pattern,
            source_template=source_template,
            graph=graph,
            field_map=field_map,
            target=target,
            purpose=purpose,
            utility=utility,
            persistence_mode=persistence_mode,
            long_running_mode=long_running_mode,
            direct_trigger_mode=direct_trigger_mode,
            namespace=namespace,
            node_id=node_id
        )
        self.node.is_a.append(self.session.framework_ontology.OutputTaskTemplate)

        if transform_data_ubl: self.set_transform_data_ubl(transform_data_ubl)
        if deliver_data_ubl: self.set_deliver_data_ubl(deliver_data_ubl)

    def _hydrate_from_rdf(self, session, graph, root_iri, root_node_id):
        super()._hydrate_from_rdf(session, graph, root_iri, root_node_id)
        res = graph.query(f"""
            PREFIX vaip: <https://ncei.noaa.gov/vaip/ontologies/vaip-core#>
            PREFIX fmk: <http://ncei.noaa.gov/vaip/ontologies/vaip-framework#>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            SELECT ?target ?transform_ubl ?deliver_ubl
            WHERE {{
                <{root_iri}> vaip:hasContentInformation ?content .
                ?content skos:prefLabel "Content" .
                ?content vaip:hasDataObject ?data .
                ?data skos:prefLabel "Storage Template" .
                ?data fmk:hasValue ?target .
                
                <{root_iri}> vaip:hasContentInformation ?content .
                ?content skos:prefLabel "Content" .
                ?content vaip:hasDataObject ?data .
                ?data skos:prefLabel "Transform Data UBL" .
                ?data fmk:hasValue ?transform_ubl.
                
                ?content vaip:hasDataObject ?data2 .
                ?data2 skos:prefLabel "Deliver Data UBL" .
                ?data2 fmk:hasValue ?deliver_ubl
            }}
        """)
        for r in res:
            transform_iri = str(r.transform_ubl)
            transform_node_id = None if root_node_id is None else transform_iri.rsplit("/", 1)[1]
            transform_ubl = UBLTemplate.from_rdf(session, graph, transform_iri, "ArchivalInformationUnit", transform_node_id)
            self.set_transform_data_ubl(transform_ubl)
            
            deliver_iri = str(r.deliver_ubl)
            deliver_node_id = None if root_node_id is None else deliver_iri.rsplit("/", 1)[1]
            deliver_ubl = UBLTemplate.from_rdf(session, graph, deliver_iri, "ArchivalInformationUnit", deliver_node_id)
            self.set_deliver_data_ubl(deliver_ubl)
            
            target_iri = str(r.target)
            target = utils.load(session, iri=target_iri, as_copy=False)
            self.set_target(target)
            break
        
        return self
    
    def set_target(self, target: OutputStorageTemplate):
        """Set the target Output Storage Template

        Args:
            target (OutputStorageTemplate): The desired Output Storage Template 

        Returns:
            OutputStorageTemplate: The updated Task Template
        """
        super().set_target(target)
        self.node.hasOutputStorageTemplate.append(target.node)
        return self

    def set_transform_data_ubl(self, ubl: typing.Union[UBLTemplate, str]):
        """Sets the Transformation User Business Logic Template for the Output Task Template.

        Args:
            ubl (typing.Union[UBLTemplate, str]): The desired Transformation UBLTemplate or IRI of a UBL Template

        Returns:
            OutputTaskTemplate: The updated Task Template
        """
        self.transform_data_ubl = ubl
        if isinstance(ubl, str):
            self.set_content_field(content="Content", field="Transform Data UBL", value=ubl)
            self.node.hasUBLTemplate.append(ubl)
        else:
            self.set_content_field(content="Content", field="Transform Data UBL", value=ubl.node.iri)
            self.node.hasUBLTemplate.append(ubl.node)
        return self
    
    def set_deliver_data_ubl(self, ubl: typing.Union[UBLTemplate, str]):
        """Sets the Delivery User Business Logic Template for the Output Task Template.

        Args:
            ubl (typing.Union[UBLTemplate, str]): The desired Delivery UBLTemplate or IRI of a UBL Template

        Returns:
            OutputTaskTemplate: The updated Task Template
        """
        self.deliver_data_ubl = ubl
        if isinstance(ubl, str):
            self.set_content_field(content="Content", field="Deliver Data UBL", value=ubl)
            self.node.hasUBLTemplate.append(ubl)
        else:
            self.set_content_field(content="Content", field="Deliver Data UBL", value=ubl.node.iri)
            self.node.hasUBLTemplate.append(ubl.node)
        return self
    def __merge_ubl_outputs_dicts(self):
        res = {**self.transform_data_ubl.outputs.__dict__, **self.deliver_data_ubl.outputs.__dict__}
        return res
    def __merge_ubl_input_dicts(self):
        res = {**self.transform_data_ubl.inputs.__dict__, **self.deliver_data_ubl.inputs.__dict__}
        return res
    def get_output_fields(self):
        return self.__merge_ubl_outputs_dicts()
    def get_input_fields(self):
        return self.__merge_ubl_input_dicts()
    #These are here because dip has two UBLs and they map to one fieldMap.
    def validate_output_fields(self):
        #print("Validating DIP Outputs")
        sourceFields = self.field_mapper.get_source_fields()
        combined_ubl_fields = self.__merge_ubl_outputs_dicts()
        #print(f"Combined Dict{combined_ubl_fields}")
        for fieldOutputKey in combined_ubl_fields:
            fieldOutputValue = combined_ubl_fields.get(fieldOutputKey)
            #print(f"Output Label {fieldOutputKey} isRequired:{fieldOutputValue.required} Node:{fieldOutputValue.node}")
            if( fieldOutputValue.required != fieldOutputValue.node.isRequired[0]):
                raise Exception(f"Task titled {self.get_title()}: Task output field {fieldOutputKey} required value is not in sync. {fieldOutputValue.required} {fieldOutputValue.node.isRequired}")
            if(fieldOutputValue.required ): 
                if(sourceFields.__contains__(fieldOutputValue.node)):
                    pass
                    #print(f"Required Task output field {fieldOutputKey} mapped")
                else:
                    raise Exception(f"Task titled {self.get_title()}: Required Task output field {fieldOutputKey} NOT mapped")
    #These are here because dip has two UBLs and they map to one fieldMap.
    def validate_input_fields(self):
        #print("Validating DIP Inputs")
        combined_ubl_fields = self.__merge_ubl_input_dicts()
        for fieldInputKey in combined_ubl_fields:
            fieldInputValue = combined_ubl_fields.get(fieldInputKey)
            #print(f"Input Label {fieldInputKey} isRequired:{fieldInputValue.required} Node:{fieldInputValue.node}")
            if( fieldInputValue.required != fieldInputValue.node.isRequired[0]):
                raise Exception(f"Task {self.get_title()}: Task input field {fieldInputKey} required value is not in sync.")
           
            if(fieldInputValue.required): 
                found_entries:list[FieldMapEntry]= self.field_mapper.find_all_entries(hasSourceField=[fieldInputValue.node])
                if(found_entries.__len__()==0):
                    raise Exception(f"Task titled {self.get_title()}: Required Task input field {fieldInputKey} NOT mapped")
               
                #Not sure if this could happen unless intentionally, but its covered
                for entry in found_entries:
                   if(len(entry.node.hasTargetField) ==0):
                        raise Exception(f"Task titled {self.get_title()}: Required Task input field {fieldInputKey} is mapped, but has no Target Field")
                   #print(f"source: {entry.node.hasSourceField} target: {entry.node.hasTargetField}")
                

class ProcessTemplate(BaseTemplate):
    """A Process represents an API exposed unit of computational capability. A typical framework implementation might expose an API for users to retrieve a Process Template, which allows them to add and link Tasks, provide information about the Process itself such as Access Rights or Description, and then deploy the process as a record.
    """
    def __init__(self,
        session,
        source_pattern: typing.Union[ProcessPattern, str] = None,
        source_template: typing.Union[ProcessTemplate, str] = None,
        graph: Graph = None,
        purpose: str = None,
        utility: str = None,
        namespace: str = utils.get_process_template_namespace(),
        node_id: str = None
    ):
        if source_template is None and source_pattern is None:
            source_pattern = session.get_system_pattern("process")
        
        super().__init__(
            session,
            source_pattern=source_pattern,
            source_template=source_template,
            graph=graph,
            namespace=namespace,
            node_id=node_id
        )
        
        self.node.is_a.append(self.session.framework_ontology.ProcessTemplate)
        self.task_links: typing.Dict[str, typing.Set[BaseTask]] = {}
        self.aic_task_counter = 0
        self.dip_task_counter = 0

        if purpose: self.set_purpose(purpose)
        if utility: self.set_utility(utility)
    
    def _hydrate_from_rdf(self, session, graph, root_iri, root_node_id):
        super()._hydrate_from_rdf(session, graph, root_iri, root_node_id)
        res = graph.query(f"""
            PREFIX vaip: <https://ncei.noaa.gov/vaip/ontologies/vaip-core#>
            PREFIX fmk: <http://ncei.noaa.gov/vaip/ontologies/vaip-framework#>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            SELECT ?purpose ?utility
            WHERE {{
                <{root_iri}> vaip:describedBy ?desc .
                ?desc skos:prefLabel "Purpose" .
                ?desc vaip:hasDataObject/fmk:hasValue ?purpose .
                
                <{root_iri}> vaip:describedBy ?desc2 .
                ?desc2 skos:prefLabel "General Utility" .
                ?desc2 vaip:hasDataObject/fmk:hasValue ?utility .
            }}
        """)
        purpose: str = None
        utility: str = None
        for r in res:
            purpose = str(r.purpose)
            utility = str(r.utility)
            break
        if purpose: self.set_purpose(purpose)
        if utility: self.set_utility(utility)
        
        res = graph.query(f"""
            PREFIX fmk: <http://ncei.noaa.gov/vaip/ontologies/vaip-framework#>
            SELECT ?task
            WHERE {{
                <{root_iri}> fmk:hasIdentityTaskTemplate ?task .
            }}
        """)
        for r in res:
            iri = str(r.task)
            node_id = None if root_node_id is None else iri.rsplit("/", 1)[1]
            task = IdentityTaskTemplate.from_rdf(session, graph, iri, "ArchivalInformationUnit", node_id)
            self.aiu_task = task
            self.node.hasIdentityTaskTemplate.append(task.node)
        
        res = graph.query(f"""
            PREFIX fmk: <http://ncei.noaa.gov/vaip/ontologies/vaip-framework#>
            SELECT ?task
            WHERE {{
                <{root_iri}> fmk:hasTransformationTaskTemplate ?task .
            }}
        """)
        for r in res:
            iri = str(r.task)
            node_id = None if root_node_id is None else iri.rsplit("/", 1)[1]
            task = TransformationTaskTemplate.from_rdf(session, graph, iri, "ArchivalInformationUnit", node_id)
            self.aic_task_counter += 1
            self.node.hasTransformationTaskTemplate.append(task.node)
        
        res = graph.query(f"""
            PREFIX fmk: <http://ncei.noaa.gov/vaip/ontologies/vaip-framework#>
            SELECT ?task
            WHERE {{
                <{root_iri}> fmk:hasOutputTaskTemplate ?task .
            }}
        """)
        for r in res:
            iri = str(r.task)
            node_id = None if root_node_id is None else iri.rsplit("/", 1)[1]
            task = OutputTaskTemplate.from_rdf(session, graph, iri, "ArchivalInformationUnit", node_id)
            self.dip_task_counter += 1
            self.node.hasOutputTaskTemplate.append(task.node)
        
        return self

    def set_purpose(self, purpose: str):
        """Set the description of the purpose of the Process. This is metadata to help describe the Process.

         Args:
             purpose (str): A description of the purpose of the Process.

         Returns:
             ProcesTemplate: The updated ProcessTemplate.
         """
        self.purpose_description = purpose
        self.set_description_field(description="Purpose", field="Description", value=purpose)
        return self

    def set_utility(self, utility: str):
        """Set the description of the utility of the Proces. This is metadata to help describe the Process.

         Args:
             utility (str): A description of the utility of the Process.

         Returns:
             Processtemplate: The updated ProcessTemplate.
         """
        self.utility_description = utility
        self.set_description_field(description="General Utility", field="Description", value=utility)
        return self
    
    def set_aiu_task(self, task: IdentityTaskTemplate):
        """Sets the AIU task for the Process.\n
        An Archival Information Unit (AIU) is an Archival Information Package where the Archive chooses not to break down the Content Information into other Archival Information Packages. An AIU can consist of multiple digital objects (e.g., multiple files). An AIU is pattern-defined by the user to specify the shape of some type of entity that the user cares about.

        Args:
            task (IdentityTaskTemplate): The desired AIU Task Template 

        Returns:
            ProcessTemplate: Returns the updated Process
        """
        # TODO: check for existing aiu_task and iterate through task links to unlink it
        self.aiu_task = task
        self.content.add_link_field("AIU Task", value=task.node.iri)
        self.node.hasIdentityTaskTemplate.append(task.node)
        return self

    def _search_linked_task(self, task_node, search_iri):
        for downstream_task in task_node.hasFlowTo:
            next_iri = downstream_task
            if (search_iri == next_iri):
                return True
            else:
                next_node = self.session.context[next_iri]
                return self._search_linked_task(next_node, search_iri)
        return False
    
    def link_aic_task(self, source_task: BaseTask, aic_task: TransformationTaskTemplate):
        """Link an Archival Information Collection to Either an Archival Information Unit Task or another Archival Information Collection Task.\n
        Linked Tasks cannot form processing loops. If you need to do a task additional times, please create a copy of that task.\n
        You cannot link DIP tasks as the Source Task.

        Args:
            source_task (BaseTask): The upstream task. Either an AIU or AIC Task.
            aic_task (TransformationTaskTemplate): The downstream AIC Task.

        Raises:
            Exception: If inifinite task loop is detected, throws "Infinite Task loop error"

        Returns:
            ProcessTemplate: The updated Process.
        """
        if self._search_linked_task(aic_task.node, source_task.node.iri):
            raise Exception("Infinite Task loop error")

        tasks = self.task_links.get(source_task.node_id)
        if (tasks):
            self.task_links[source_task.node_id].add(aic_task)
        else:
            self.task_links[source_task.node_id] = set([aic_task])
        self.aic_task_counter += 1
        linked_field = self.content.add_link_field(f"AIC Task {str(self.aic_task_counter)}", value=aic_task.node.iri)

        link_count = len(self.task_links[source_task.node_id])
        # TODO: add semantic/structure representation to context, Added Temp Values for testing
        ctx = source_task.add_context(f"AIC Task {str(link_count)}", field={ 'title': "IRI", 'value': aic_task.node.iri, 'is_link': True })
        ctx.add_structure_representation("Autogenerated Structural Representation for linked AIC")
        ctx.add_semantic_representation("Autogenerated Semantic Rep for linked AIC")
        self.node.hasTransformationTaskTemplate.append(aic_task.node)
        source_task.node.hasFlowTo.append(aic_task.node)
        aic_task.node.hasFlowFrom.append(source_task.node)
        return self

    def link_dip_task(self, source_task: BaseTask, dip_task: OutputTaskTemplate):
        """Link an Dissemination Information Package to Either an Archival Information Unit Task or another Archival Information Collection Task.\n
        Linked Tasks cannot form processing loops. If you need to do a task additional times, please create a copy of that task.\n
        You cannot link DIP tasks as the Source Task. DIP tasks cannot link to other DIP Tasks.


        Args:
            source_task (BaseTask): The upstream task. Either an AIU or AIC Task.
            aic_task (TransformationTaskTemplate): The downstream DIP Task.

        Raises:
            Exception: If inifinite task loop is detected, throws "Infinite Task loop error"

        Returns:
            ProcessTemplate: The updated Process.
        """
        if self._search_linked_task(dip_task.node, source_task.node.iri):
            raise Exception("Infinite Task loop error")
        
        tasks = self.task_links.get(source_task.node_id)
        if (tasks):
            self.task_links[source_task.node_id].add(dip_task)
        else:
            self.task_links[source_task.node_id] = set([dip_task])
        self.dip_task_counter += 1
        self.content.add_link_field(f"DIP Task {str(self.dip_task_counter)}", value=dip_task.node.iri)

        link_count = len(self.task_links[source_task.node_id])
        # TODO: add semantic/structure representation to context
        ctx = source_task.add_context(f"DIP Task {str(link_count)}", field={ 'title': "IRI", 'value': dip_task.node.iri, 'is_link': True })
        ctx.add_structure_representation("Autogenerated Structural Representation for linked DIP")
        ctx.add_semantic_representation("Autogenerated Semantic Rep for linked DIP")

        self.node.hasOutputTaskTemplate.append(dip_task.node)
        source_task.node.hasFlowTo.append(dip_task.node)
        dip_task.node.hasFlowFrom.append(source_task.node)
        return self

    def unlink_aic_task(self, source_task: BaseTask, aic_task: TransformationTaskTemplate):
        """Unlink an Archival Information Collection from either an Archival Information Unit Task or another Archival Information Collection Task.\n
        Args:
            source_task (BaseTask): The upstream task. Either an AIU or AIC Task.
            aic_task (TransformationTaskTemplate): The downstream AIC Task.

        Returns:
            ProcessTemplate: The updated Process.
        """
        self.task_links[source_task.node_id].remove(aic_task)
        self.node.hasTransformationTaskTemplate.remove(aic_task.node)
        source_task.node.hasFlowTo.remove(aic_task.node)
        aic_task.node.hasFlowFrom.remove(source_task.node)
        self.aic_task_counter -= 1
        return self

    def unlink_dip_task(self, source_task: BaseTask, dip_task: OutputTaskTemplate):
        """Unlink an Dissemination Information Package from either an Archival Information Unit Task or another Archival Information Collection Task.\n
        Args:
            source_task (BaseTask): The upstream task. Either an AIU or AIC Task.
            aic_task (TransformationTaskTemplate): The downstream DIP Task.

        Returns:
            ProcessTemplate: The updated Process.
        """
        self.task_links[source_task.node_id].remove(dip_task)
        self.node.hasOutputTaskTemplate.remove(dip_task.node)
        source_task.node.hasFlowTo.remove(dip_task.node)
        dip_task.node.hasFlowFrom.remove(source_task.node)
        self.dip_task_counter -= 1
        return self
    
    def _build_task_set(self):
        tasks: typing.Set[BaseTask] = set()
        if self.aiu_task:
            tasks.add(self.aiu_task)
        for linked_tasks in self.task_links.values():
            for task in linked_tasks:
                tasks.add(task)
        return tasks
    
    def get_unmatched_fields(self):
        tasks = self._build_task_set()
        unmapped_inputs = set()
        for task in tasks:
            task_inputs = set()
            for field in task.get_input_fields().values():
                # TODO: revisit this check once is_required gets fleshed out for Fields
                if utils.is_placeholder(field.value):
                    task_inputs.add(field.node.iri)
            mapped_inputs = set([field.iri for field in task.field_mapper.get_target_fields()])
            unmapped_inputs.update(task_inputs.difference(mapped_inputs))
        return unmapped_inputs

        #Process specific task validation
    def validate(self):
        #If the SHACL isn't valid, there is no way the non-SHACL will be.
        validation_report = super().validate()
        if(validation_report.conforms == False):
            return validation_report
        self.aiu_task.validate_output_fields()
        
        uniqueTasks =[]
        unduped_tasks = set()
        #unduped_tasks.add(self.aiu_task)
        for tasks in self.task_links.values():
            for task in tasks:
                if task not in unduped_tasks:
                    unduped_tasks.add(task)
                    task.validate_output_fields()
                    task.validate_input_fields()
        return validation_report


    def deploy(self):
        """Deploy the Process and all of its Tasks into the Cloud.

        Returns:
            object: {
            self.node.iri: process_responses,
            self.aiu_task.target.node.iri: aiu_task_responses,
            **other_task_responses
        }
        """

        if self.aiu_task is not None:
            aiu_task_responses = self.aiu_task.deploy()
        other_task_responses = {}
        unduped_tasks = set()
        for tasks in self.task_links.values():
            for task in tasks:
                if task not in unduped_tasks:
                    unduped_tasks.add(task)
                    other_task_responses[task.node.iri] = task.deploy()
        process_responses = self.session.deploy(self)
        return {
            self.node.iri: process_responses,
            self.aiu_task.node.iri: aiu_task_responses,
            **other_task_responses
        }


    def visualize(self, notebook=True, filter_menu=True, hierarchical:bool=True, isCDNRemote:bool=True, height:str="750px"):
        """Creates the NetworkX network and styles it.

        Args:
            notebook (bool): Are you running in a Juypter Notebook? Yes if True.
            filter_menu (bool): Do you want the filter menu? Yes if True.
            hierarchical (bool): Display the graph in hierarchical mode? Yes if True.
            isCDNRemote (bool): Do you want the JS resources for pyVis to be remote? Yes if True. If notebook is True, isCDNRemote is also True. If False, JS files required by the visualization will be written locally.
            height (string): Height of the graph area. Can be a height in px, em, or percentage. Do not set to 100% if filter_menu is True as the menu may be unaccessable.
        """

        if notebook:
            vis_network = vis.Network(notebook=True, cdn_resources=True, filter_menu=filter_menu)
        else:
            isRemote="local"
            if(isCDNRemote):
                isRemote="remote"
            vis_network = vis.Network(height=height, filter_menu=filter_menu, cdn_resources=isRemote)
        if hierarchical:
            vis_network.set_options("""
            const options = {
                "layout": {
                    "hierarchical": {
                        "enabled": true,
                        "direction": "LR",
                        "sortMethod": "directed"
                        }
                    }
                }""")
        else:
            #vis_network.show_buttons() # do not turn this on without comment out below.
            vis_network.set_options("""
            const options = {
                "physics": {
                    "forceAtlas2Based": {
                    "springLength": 100
                    },
                    "minVelocity": 0.75,
                    "solver": "forceAtlas2Based"
                }
            }""")
        visited_nodes = set()
        process_root = utils.node_tree(self.node, ontologies=[self.session.core_ontology, self.session.framework_ontology, self.ontology], visited_nodes=visited_nodes)
        utils.parse_vis_tree(process_root, vis_network)
        
        tasks: typing.Set[BaseTask] = set()
        if self.aiu_task:
            tasks.add(self.aiu_task)
        
        for linked_tasks in self.task_links.values():
            for task in linked_tasks:
                tasks.add(task)
        
        for task in tasks:
            task_root = utils.node_tree(task.node, ontologies=[self.session.core_ontology, self.session.framework_ontology, task.ontology], visited_nodes = set())
            utils.parse_vis_tree(task_root, vis_network)
        return vis_network

class BaseRecord(EntityPackage):
    """The Base Class that all other Record Classes inherit.
    """
    def __init__(self, source_template: BaseTemplate, namespace = None, template_field_values = {}):
        self.template = source_template
        VaipClass = self.template.node.is_a[0]
        super().__init__(source_template.session, VaipClass, namespace, self.template.get_title(), self.template.get_labels())
        self.node.hasParentTemplate = [source_template.node]

        self._copy_from_template(template_field_values)

    def _copy_from_template(self, template_field_values):
        fmap = dict([
            (str(self.session.core_ontology.ContentInformationObject), self.set_content),
            (str(self.session.core_ontology.UnitDescription), self.add_description),
            (str(self.session.core_ontology.PackagingInformationObject), self.add_packaging),
            (str(self.session.core_ontology.FixityPreservation), self.add_fixity),
            (str(self.session.core_ontology.AccessRightsPreservation), self.add_access_rights),
            (str(self.session.core_ontology.ContextPreservation), self.add_context),
            (str(self.session.core_ontology.ProvenancePreservation), self.add_provenance),
            (str(self.session.core_ontology.ReferencePreservation), self.add_reference)
        ])
        for iobj in self.template.information_objects:
            add_func = fmap[str(iobj.node.is_a[0])]
            iobj_title = iobj.get_title()
            copied_resource = add_func(iobj_title, iobj.get_labels(), field=None)
            copied_resource.copy_from_information_object(iobj, template_field_values)
            setattr(self, snakecase(iobj_title), copied_resource)
            for dobj in copied_resource.data_objects:
                setattr(copied_resource, snakecase(dobj.get_title()), dobj)
                self.node.hasLiteralField.append(dobj.node)
            for rep in copied_resource.representations:
                setattr(copied_resource, snakecase(rep.get_title()), rep)
                for dobj in rep.data_objects:
                    dobj_title = dobj.get_title()
                    dobj_id = dobj.node_id
                    setattr(rep, snakecase(dobj_title), dobj)
                    self.node.hasLiteralField.append(dobj.node)

class IdentityStorageRecord(BaseRecord):
    """Identity/AIU Storage Record

    A Record is a fully valued unit of the system - each Record derives from a runtime execution of a Template. Records are deep-copies of Template parents. As deep-copies of Templates, Records are fully conformant to the implemented Reference Model and are fully denormalized metadata.
    """
    def __init__(self, source_template: IdentityStorageTemplate, template_field_values = {}):
        super().__init__(source_template, utils.get_aiu_record_namespace(), template_field_values)
        self.node.is_a.append(self.session.framework_ontology.IdentityStorageRecord)

# class MemberRecord(LiteralField):
#     def __init__(self, target_aic: typing.Union[TransformationStorageTemplate, str]):
#         super().__init__(parent, title = None, labels = [], value = utils.generate_placeholder(), namespace = None, namespace_class = None, is_required = False, node_id = None)

class OutputStorageRecord(BaseRecord):
    """ Output/DIP Storage Record
    
    A Record is a fully valued unit of the system - each Record derives from a runtime execution of a Template. Records are deep-copies of Template parents. As deep-copies of Templates, Records are fully conformant to the implemented Reference Model and are fully denormalized metadata.
    """
    def __init__(self, source_template: OutputStorageTemplate, template_field_values = {}):
        super().__init__(source_template, utils.get_dip_record_namespace(), template_field_values)
        self.node.is_a.append(self.session.framework_ontology.OutputStorageRecord)

class SessionPattern(EntityPackage):
    def __init__(self, session, title: str, labels: 'list[str]' = [], node_id: str = None):
        super().__init__(session, session.core_ontology.ArchivalInformationUnit, utils.get_session_pattern_namespace(), title, labels, node_id)
        self.node.is_a.append(self.session.framework_ontology.SessionPattern)
        
class RequestPattern(EntityPackage):
    def __init__(self, session, title: str, labels: 'list[str]' = [], node_id: str = None):
        super().__init__(session, session.core_ontology.ArchivalInformationUnit, utils.get_request_pattern_namespace(), title, labels, node_id)
        self.node.is_a.append(self.session.framework_ontology.RequestPattern)
        
class ResponsePattern(EntityPackage):
    def __init__(self, session, title: str, labels: 'list[str]' = [], node_id: str = None):
        super().__init__(session, session.core_ontology.ArchivalInformationUnit, utils.get_response_pattern_namespace(), title, labels, node_id)
        self.node.is_a.append(self.session.framework_ontology.ResponsePattern)

class SessionTemplate(BaseTemplate):
    def __init__(self,
        session,
        source_pattern: typing.Union[SessionPattern, str] = None,
        source_template: typing.Union[SessionTemplate, str] = None,
        graph: Graph = None,
        namespace: str = utils.get_session_template_namespace(),
        node_id: str = None
    ):
        if source_pattern is None and source_template is None:
            source_pattern = session.get_system_pattern("session")
        super().__init__(
            session,
            source_pattern=source_pattern,
            source_template=source_template,
            graph=graph,
            namespace=namespace,
            node_id=node_id
        )
        self.node.is_a.append(self.session.framework_ontology.SessionTemplate)
        
class RequestTemplate(BaseTemplate):
    def __init__(self,
        session,
        source_pattern: typing.Union[RequestPattern, str] = None,
        source_template: typing.Union[RequestTemplate, str] = None,
        graph: Graph = None,
        namespace: str = utils.get_request_template_namespace(),
        node_id: str = None
    ):
        if source_pattern is None and source_template is None:
            source_pattern = session.get_system_pattern("request")
        super().__init__(
            session,
            source_pattern=source_pattern,
            source_template=source_template,
            graph=graph,
            namespace=namespace,
            node_id=node_id
        )
        self.node.is_a.append(self.session.framework_ontology.RequestTemplate)
        
class ResponseTemplate(BaseTemplate):
    def __init__(self,
        session,
        source_pattern: typing.Union[ResponsePattern, str] = None,
        source_template: typing.Union[ResponseTemplate, str] = None,
        graph: Graph = None,
        namespace: str = utils.get_response_template_namespace(),
        node_id: str = None
    ):
        if source_pattern is None and source_template is None:
            source_pattern = session.get_system_pattern("response")
        super().__init__(
            session,
            source_pattern=source_pattern,
            source_template=source_template,
            graph=graph,
            namespace=namespace,
            node_id=node_id
        )
        self.node.is_a.append(self.session.framework_ontology.ResponseTemplate)

class SessionRecord(BaseRecord):
    """Session Record\n
    A Record is a fully valued unit of the system - each Record derives from a runtime execution of a Template. Records are deep-copies of Template parents. As deep-copies of Templates, Records are fully conformant to the implemented Reference Model and are fully denormalized metadata.
    """
    def __init__(self, source_template: SessionTemplate, template_field_values = {}):
        super().__init__(source_template, utils.get_session_record_namespace(), template_field_values)
        self.node.is_a.append(self.session.framework_ontology.SessionRecord)
        
    def set_request_record(self, request: typing.Union[str, RequestRecord]):
        iri = request if isinstance(request, str) else request.node.iri
        # Set the Request ID Field from the SessionTemplate
        self.request_record.id.set_value(iri)
        if isinstance(request, str):
            split = request.rsplit("/", 2)
            temp_node_id = split[2]
            temp_namespace = self.session.context.get_ontology(split[0]).get_namespace(request)
            temp = self.session.framework_ontology.RequestRecord(temp_node_id, namespace=temp_namespace)
            self.node.hasRequestRecord = [temp]
        else:
            self.node.hasRequestRecord = [request.node]
    
    def add_response_record(self, response: typing.Union[str, ResponseRecord]):
        iri = response if isinstance(response, str) else response.node.iri
        # Set the Request ID Field from the SessionTemplate
        self.response_records.add_link_field(title=f"Record {len(self.response_records.data_objects) + 1}", value=iri)
        if isinstance(response, str):
            split = iri.rsplit("/", 2)
            temp_node_id = split[2]
            temp_namespace = self.session.context.get_ontology(split[0]).get_namespace(iri)
            temp = self.session.framework_ontology.RequestRecord(temp_node_id, namespace=temp_namespace)
            self.node.hasResponseRecord.append(temp)
        else:
            self.node.hasResponseRecord.append(response.node)

class RequestRecord(BaseRecord):
    """Request Record\n
    A Record is a fully valued unit of the system - each Record derives from a runtime execution of a Template. Records are deep-copies of Template parents. As deep-copies of Templates, Records are fully conformant to the implemented Reference Model and are fully denormalized metadata.
    """
    def __init__(self, source_template: RequestTemplate, session_record: SessionRecord, field_map = None, template_field_values = {}):
        super().__init__(source_template, utils.get_request_record_namespace(), template_field_values)
        self.node.is_a.append(self.session.framework_ontology.RequestRecord)
        self.set_field_map(field_map)
        
    def set_session_record(self, session: SessionRecord):
        # Set the Session ID Field from the RequestTemplate
        self.session_record.id.set_value(session.node.iri)
        
    def set_response_record(self, record: str):
        self.response_record.id.set_value(record)
        split = record.rsplit("/", 2)
        temp_node_id = split[2]
        temp_namespace = self.session.context.get_ontology(split[0]).get_namespace(record)
        temp = self.session.framework_ontology.ResponseRecord(temp_node_id, namespace=temp_namespace)
        self.node.hasResponseRecord = [temp]
    
    def set_field_map(self, field_map):
        if field_map is not None:
            self._field_map = field_map
            # Set the FieldMap Link Field from the Request Template
            self.field_map.link.set_value(field_map.node.iri)
            self.node.hasFieldMap = [field_map.node]
        return self
        
class ResponseRecord(BaseRecord):
    """Reponse Record\n
    A Record is a fully valued unit of the system - each Record derives from a runtime execution of a Template. Records are deep-copies of Template parents. As deep-copies of Templates, Records are fully conformant to the implemented Reference Model and are fully denormalized metadata.
    """
    def __init__(self, source_template: ResponseTemplate, session_record: SessionRecord, template_field_values = {}):
        super().__init__(source_template, utils.get_response_record_namespace(), template_field_values)
        self.node.is_a.append(self.session.framework_ontology.ResponseRecord)
        self.set_session_record(session_record)
        
    def add_aip_record(self, record: str):
        # Set the Request ID Field from the SessionTemplate
        self.aip_records.add_link_field(title=f"Record {len(self.aip_records.data_objects) + 1}", value=record)
    
    def set_task_record(self, record: str):
        self.task_record.id.set_value(record)
    
    def set_session_record(self, record: SessionRecord):
        # Set the Session ID Field from the ResponseTemplate
        self.session_record.id.set_value(record.node.iri)
    
    def set_request_record(self, record: typing.Union[str, RequestRecord]):
        iri = record if isinstance(record, str) else record.node.iri
        # Set the Request ID Field from the ResponseTemplate
        self.request_record.id.set_value(iri)
        if isinstance(record, str):
            split = record.rsplit("/", 2)
            temp_node_id = split[2]
            temp_namespace = self.session.context.get_ontology(split[0]).get_namespace(record)
            temp = self.session.framework_ontology.RequestRecord(temp_node_id, namespace=temp_namespace)
            self.node.hasRequestRecord = [temp]
        else:
            self.node.hasRequestRecord = [record.node]
