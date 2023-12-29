import typing
from . import ontology, utils
from rdflib import Graph
from rdflib.plugins.shared.jsonld.context import Context

def create_record(session, storage_template_iri, template_field_values):
  template = utils.load(session, storage_template_iri, as_copy=False)
  cmap = dict([
    (ontology.IdentityStorageTemplate, ontology.IdentityStorageRecord),
    (ontology.TransformationStorageTemplate, ontology.TransformationStorageRecord),
    (ontology.OutputStorageTemplate, ontology.OutputStorageRecord),
  ])
  recordFn = cmap[type(template)]
  record = recordFn(template, template_field_values)
  return record

def create_member_description_record(session, template_field_values, mem_desc_template: typing.Union[ontology.MemberDescriptionTemplate, str]):
  mem_desc_template = mem_desc_template if not isinstance(mem_desc_template, str) else utils.load(session, mem_desc_template, as_copy=False)
  new_membership = ontology.MemberDescriptionRecord(session, source_template=mem_desc_template, template_field_values=template_field_values)
  return new_membership
 
def create_aic_member(session, member_iri, description_record: ontology.MemberDescriptionRecord, aic_record: ontology.TransformationStorageRecord):
  template_id = aic_record.aic_template_id
  node_id = utils.generate_node_id()
  member_record_namespace_str = utils.get_aic_member_record_namespace(template_id)
  record_ontology = session.context.get_ontology(f"{member_record_namespace_str}/{node_id}")
  record_namespace = record_ontology.get_namespace(f"{member_record_namespace_str}/{node_id}/")
  temp_content = ontology.InformationObject(session, session.core_ontology.ContentInformationObject, record_namespace, title="Temp", labels=[], node_id=node_id)
  aip_member = temp_content.add_link_field("AIP Member", value=member_iri)
  
  temp_content.destroy(cascade=False)
  return aip_member
 
def convert_to_jsonld(resource):
    rdf = resource.serialize(format="rdfxml")
    graph = Graph()
    graph.parse(data=rdf, format="xml")
    context = Context(
        {
            "vaip-core": "https://ncei.noaa.gov/vaip/ontologies/vaip-core#",
            "vaip-fmk": "http://ncei.noaa.gov/vaip/ontologies/vaip-framework#"
        }
    )
    json_ld = graph.serialize(format="json-ld", context=context)
    return json_ld