from rdflib import Namespace
from discomat.ontology.namespaces import CUDS
from rdflib import RDF

"""
ideally we would have an automatic way to get from python attribute/property to ontology

example: CUDS.description could be 

c.cuds.description 
c.rdfs.class --> RDFS.Class etc 
here is an example:
"""
ONTOMAP = {
    'uuid': CUDS.uuid,
    'description': CUDS.description,
    'pid': CUDS.PID,
    'label': CUDS.label,
    'creation_time': CUDS.CreationTime,
    'ontology_type': RDF.type,
    'RDF.type': RDF.type,
    'session': CUDS.Session,
    'engine_iri': CUDS.EngineIri,
    'session_id': CUDS.SessionId,
    'session_status': CUDS.SessionStatus,
    'default_graph_id': CUDS.DefaultGraphId

}
