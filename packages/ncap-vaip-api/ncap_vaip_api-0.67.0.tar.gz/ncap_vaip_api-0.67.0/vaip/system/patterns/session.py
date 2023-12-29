from ...ontology import SessionPattern, RequestPattern, ResponsePattern

def create_session_pattern(session):
    pattern = SessionPattern(session)
    content = pattern.set_content("Response Records", field=None)
    content.add_structure_representation("Format")
    content.add_semantic_representation("Description")
    
    context = pattern.add_context("Request Record", field={'title': "ID", 'is_link': True})
    context.add_structure_representation("Format")
    context.add_semantic_representation("Description")
    
    context2 = pattern.add_context("Process Record", field={'title': "ID", 'is_link': True})
    context2.add_structure_representation("Format")
    context2.add_semantic_representation("Description")
    
    description = pattern.add_description("CHANGE ME Description")
    description.add_structure_representation("Format")
    description.add_semantic_representation("Meaning")
    
    packaging = pattern.add_packaging("CHANGE ME Packaging")
    packaging.add_structure_representation("Format")
    packaging.add_semantic_representation("Description")
    
    access_rights = pattern.add_access_rights("CHANGE ME Access Rights")
    access_rights.add_structure_representation("Format")
    access_rights.add_semantic_representation("Description")
    
    fixity = pattern.add_fixity("CHANGE ME Fixity")
    fixity.add_structure_representation("Format")
    fixity.add_semantic_representation("Description")
    
    provenance = pattern.add_provenance("CHANGE ME Provenance")
    provenance.add_structure_representation("Format")
    provenance.add_semantic_representation("Description")
    
    reference = pattern.add_reference("CHANGE ME Reference")
    reference.add_structure_representation("Format")
    reference.add_semantic_representation("Description")
    return pattern
    
def create_request_pattern(session):
    pattern = RequestPattern(session)
    content = pattern.set_content("Field Map", field={"title": "Link", "is_link": True})
    content.add_structure_representation("Format")
    content.add_semantic_representation("Description")
    
    context = pattern.add_context("Session Record", field={'title': "ID", 'is_link': True})
    context.add_structure_representation("Format")
    context.add_semantic_representation("Description")
    
    description = pattern.add_description("CHANGE ME Description")
    description.add_structure_representation("Format")
    description.add_semantic_representation("Meaning")
    
    packaging = pattern.add_packaging("CHANGE ME Packaging")
    packaging.add_structure_representation("Format")
    packaging.add_semantic_representation("Description")
    
    access_rights = pattern.add_access_rights("CHANGE ME Access Rights")
    access_rights.add_structure_representation("Format")
    access_rights.add_semantic_representation("Description")
    
    fixity = pattern.add_fixity("CHANGE ME Fixity")
    fixity.add_structure_representation("Format")
    fixity.add_semantic_representation("Description")
    
    provenance = pattern.add_provenance("CHANGE ME Provenance")
    provenance.add_structure_representation("Format")
    provenance.add_semantic_representation("Description")
    
    reference = pattern.add_reference("CHANGE ME Reference")
    reference.add_structure_representation("Format")
    reference.add_semantic_representation("Description")
    return pattern
    
def create_response_pattern(session):
    pattern = ResponsePattern(session)
    content = pattern.set_content("AIP Records", field=None)
    content.add_structure_representation("Format")
    content.add_semantic_representation("Description")
    
    context = pattern.add_context("Session Record", field={'title': "ID", 'is_link': True})
    context.add_structure_representation("Format")
    context.add_semantic_representation("Description")
    
    context = pattern.add_context("Request Record", field={'title': "ID", 'is_link': True})
    context.add_structure_representation("Format")
    context.add_semantic_representation("Description")
    
    fixity = pattern.add_fixity("Status", field={"title": "Success"})
    fixity.add_structure_representation("Format")
    fixity.add_semantic_representation("Description")
    
    provenance = pattern.add_provenance("Task Record", field={"title": "ID", "is_link": True})
    provenance.add_structure_representation("Format")
    provenance.add_semantic_representation("Description")
    
    description = pattern.add_description("CHANGE ME Description")
    description.add_structure_representation("Format")
    description.add_semantic_representation("Meaning")
    
    packaging = pattern.add_packaging("CHANGE ME Packaging")
    packaging.add_structure_representation("Format")
    packaging.add_semantic_representation("Description")
    
    access_rights = pattern.add_access_rights("CHANGE ME Access Rights")
    access_rights.add_structure_representation("Format")
    access_rights.add_semantic_representation("Description")
    
    reference = pattern.add_reference("CHANGE ME Reference")
    reference.add_structure_representation("Format")
    reference.add_semantic_representation("Description")
    return pattern