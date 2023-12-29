from ... import ontology

def create_pattern_metadata_pattern(session):
    title = "Pattern Metadata"
    metadata_pattern = ontology.IdentityStoragePattern(session, title)
    return metadata_pattern