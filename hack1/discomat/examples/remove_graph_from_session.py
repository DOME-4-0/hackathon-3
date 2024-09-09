from discomat.cuds.cuds import Cuds
from discomat.visualisation.cuds_vis import gvis
from discomat.cuds.utils import uuid_from_string, to_iri, pr, prd
from discomat.cuds.session import Session
from discomat.ontology.namespaces import CUDS, MIO, MISO

from rdflib import URIRef, Graph
from rdflib.namespace import RDF, RDFS
import copy
from discomat.ontology.namespaces import CUDS, MISO, MIO

session = Session()

session.create_graph("graph1")
session.create_graph("graph2")

print(session)
print(session.engine)

session.remove_graph("graph1")
print(session)
print(session.engine)
gvis(session, "session_example.html")
