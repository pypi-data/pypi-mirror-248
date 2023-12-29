from ... import ontology

def create_aic_pattern(session, title="AIC"):
    pattern = ontology.TransformationStoragePattern(session, title)

    reference = pattern.add_reference("DOI", field={'title': 'Value', 'is_link': False})
    semantic = reference.add_semantic_representation("Description")
    structure = reference.add_structure_representation("Format")
    semantic.node.addsMeaningTo.append(structure.node)

    checksum = pattern.add_fixity("Checksum", field={'title': 'Value', 'is_link': False})
    checksum_semantic = checksum.add_semantic_representation("Definition")
    checksum_structure = checksum.add_structure_representation("Format")
    checksum_semantic.node.addsMeaningTo.append(checksum_structure.node)

    file_content = pattern.set_content("Members", field=None)
    #TODO: Allow System Patterns to be incomplete, and remove below line.
    file_content.add_value_field("Pattern Placeholder")
    file_semantic = file_content.add_semantic_representation("Description")
    file_structure = file_content.add_structure_representation("Format")
    file_semantic.node.addsMeaningTo.append(file_structure.node)
    

    description = pattern.add_overview_description("Overview Description")
    description.add_semantic_representation("Meaning")
    description.add_structure_representation("Format")

    memDesc = pattern.add_member_description("Member Description")
    mem_field = memDesc.add_literal("Placeholder Field Please Remove", is_required=False)
    mem_field.set_value("The Member Field Value")

    access = pattern.add_access_rights("Access Rights")
    access.add_semantic_representation("Meaning")
    access.add_structure_representation("Format")

    context = pattern.add_context("Help Guide")
    context.add_semantic_representation("Meaning")
    context.add_structure_representation("Format")

    provenance = pattern.add_provenance("Provenance", field=None)
    provenance.add_semantic_representation("Meaning")
    provenance.add_structure_representation("Format")
    provenance.add_link_field("Process")
    provenance.add_link_field("Task")

    packaging = pattern.add_packaging("Packaging")
    packaging.add_semantic_representation("Packaging Strategy")
    packaging.add_structure_representation("Packaging Format")

    return pattern