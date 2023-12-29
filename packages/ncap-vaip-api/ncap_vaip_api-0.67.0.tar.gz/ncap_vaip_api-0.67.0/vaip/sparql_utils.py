from urllib.parse import urlparse

def query_title_and_labels(rdf_graph, iri):
    title = ""
    labels = []
    res = rdf_graph.query(f"""
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?title
        WHERE {{
            <{iri}> skos:prefLabel ?title
        }}
    """)
    for r in res:
        title = str(r.title)
        break
    
    res = rdf_graph.query(f"""
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?label
        WHERE {{
            <{iri}> skos:altLabel ?label
        }}
    """)
    for r in res:
        labels.append(str(r.label))
    return (title, labels)
    
def query_vaip_core_class(rdf_graph, iri):
    res = rdf_graph.query(f"""
    SELECT ?type
    WHERE {{
        <{iri}> rdf:type ?type
    }}
    """)
    vaip_type = ""
    for r in res:
        if str(r.type).startswith("https://ncei.noaa.gov/vaip/ontologies/vaip-core#"):
            vaip_type = urlparse(str(r.type)).fragment
            return vaip_type
    raise Exception(f"SPARQL query of vaip-core class for entity {iri} did not return any results")
    
def query_vaip_framework_class(rdf_graph, iri):
    res = rdf_graph.query(f"""
    SELECT ?type
    WHERE {{
        <{iri}> rdf:type ?type
    }}
    """)
    fmk_type = ""
    for r in res:
        if str(r.type).startswith("http://ncei.noaa.gov/vaip/ontologies/vaip-framework#"):
            fmk_type = urlparse(str(r.type)).fragment
            return fmk_type
    raise Exception(f"SPARQL query of vaip-framework class for entity {iri} did not return any results")
