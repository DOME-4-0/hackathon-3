from discomat.cuds.cuds import Cuds
from discomat.visualisation.cuds_vis import gvis
from discomat.cuds.utils import uuid_from_string, to_iri, pr, prd
from discomat.cuds.session import Session
from discomat.ontology.namespaces import CUDS, MIO, MISO

from rdflib import URIRef, Graph
from rdflib.namespace import RDF, RDFS
import copy
from discomat.ontology.namespaces import CUDS, MISO, MIO

# test session
session = Session()
gvis(session, "cuds_session.html")
print(f"This session has an engine of type: {type(session.engine)}")
gvis(session.engine, "session_engine.html")

prd("add graphs")
session.create_graph("graph1")
session.create_graph("graph2")
session.create_graph("graph3")
gvis(session, "session_with_three_graphs.html")
print(session)

prd("remove graph2")
session.remove_graph("graph2")
print(session)
gvis(session, "session_removed_graph2.html")
session.print_graph()

# should loop over all graphs and the graph objects like and return something like
"""
<urn:x-rdflib:default> a rdfg:Graph;rdflib:storage [a rdflib:Store;rdfs:label 'Memory'].
<graph1> a rdfg:Graph;rdflib:storage [a rdflib:Store;rdfs:label 'Memory'].
<graph3> a rdfg:Graph;rdflib:storage [a rdflib:Store;rdfs:label 'Memory'].
"""
prd("-- iter over graphs")
for g in session:
    print(g)

prd(f"\nList_graphs:")
lg = session.list_graphs()
prd(lg)

gs = session.graphs()
print(f"type(gs): {type(gs)}, {gs}")
# print(gs['graph1'].serialize(format="ttl"))
# print("loop over all graphs()")
# for g in gs:
#     print(type(g))

prd("\n Add  triples")
session.add_triple(MISO.Simulation, RDF.type, RDFS.Class)
session.add_triple(MISO.Simulation, RDFS.subClassOf, CUDS.Cuds)
session.add_triple(MISO.simulation, RDF.type, MISO.Simulation)

session.add_quad(MISO.simulation, RDF.type, MISO.Simulation, "graph1")
session.add_quad(MISO.simulation, CUDS.has, MISO.SimulationEngine, "graph1")


# add it again as we use it below:
session.create_graph("graph2")
session.create_graph("graph3")
session.create_graph("graph4")

prd(f"add quads")
session.add_quad(CUDS.root0, RDF.type, CUDS.RootNode)
session.add_quad(CUDS.root1, RDF.type, CUDS.RootNode, "graph1")
session.add_quad(CUDS.root2, RDF.type, CUDS.RootNode, "graph2")
session.add_quad(CUDS.root3, RDF.type, CUDS.RootNode, "graph3")
session.add_quad(CUDS.root4, RDF.type, CUDS.RootNode, "graph4")

session.add_quad("s1", "p1", "o1", "graph1")
session.add_quad("s2", "p2", "o1", "graph1")
session.add_quad("s3", "p3", "o3", "graph1")
session.add_quad("o3", "p4", "o4", "graph1")
session.add_quad("s3", "p5", "o4", "graph1")
session.add_quad("s3", "p2", "o3", "graph1")
session.add_quad("s3", "p3", "o3", "graph1")
session.add_quad("s3", "p3", "o3", "graph1")
session.add_quad("s4", "p4", "o4", "graph2")
session.add_quad("s5", "p5", "o5", "graph2")
session.add_quad("s6", "p6", "o6", "graph2")

prd("\n Print and count quads")
print(len(list(session.quads())))
for quad in session.quads():
    print(quad)
for s, p, o, g in session.quads():
    print("quads:", s, p, o, g)

prd("test quads ")
for s, p, o, g in session.quads((None, None, None, "graph1")):
    print(s, p, o, g)

prd("test triples\n")
for s, p, o, g in session.triples(None, None, None):
    print("triples:", s, p, o, g)

prd("test serialise gs['graph1']")
print(URIRef('graph1'))
print(gs[to_iri('graph1')])

prd("Delete a quad (s4, p4, o4, graph1)")

if ("s4", "p4", "o4") in session:
    prd("its in")
else:
    prd("not in")
gvis(session, "session_all.html")

session.remove_triple("s4", "p4", "o4")
gvis(session, "session_after_remove.html")

if ("s4", "p4", "o4") in session:
    prd("its in")
else:
    prd("not in")
