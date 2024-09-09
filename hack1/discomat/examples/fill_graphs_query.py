from discomat.cuds.cuds import Cuds
from discomat.visualisation.cuds_vis import gvis
from discomat.cuds.utils import uuid_from_string, to_iri, pr, prd
from discomat.cuds.session import Session
from discomat.ontology.namespaces import CUDS, MIO, MISO
import csv

from rdflib import URIRef, Graph
from rdflib.namespace import RDF, RDFS
import copy
from discomat.ontology.namespaces import CUDS, MISO, MIO

session = Session()

[session.create_graph(g) for g in ["g1", "g2", "g3", "g4", "g5", "MISO-ONTOLOGY"]]
quads=[]
with open('quads.csv', mode='r') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        quads.append(tuple(row))

print(session)
for quad in quads:
    session.add_quad(*quad[:4])  # unpack


print(session)
gvis(session, "session5.html")