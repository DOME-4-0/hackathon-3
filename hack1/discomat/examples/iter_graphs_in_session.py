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

[session.create_graph(g) for g in ["g1", "g2", "g3", "g4", "g5"]]

for g in session:
    prd(f"Session: {session.label} contains a graph {g}")

lg = session.list_graphs()
print(lg)