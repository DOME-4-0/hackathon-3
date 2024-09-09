from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, FOAF, XSD, PROV
from discomat.cuds.cuds import Cuds
from discomat.visualisation.cuds_vis import gvis
from discomat.cuds.utils import uuid_from_string, to_iri
from discomat.cuds.session import Session
from rdflib import URIRef, Graph
import copy

s = Session(iri="http://dome40.org/Sessions/DOMEample_provenance_1/",
            description="DOMEample showing provenance in Dome 4.0")
gvis(s, "prov_session_DOME1.html")

print(f"This session has an engine of type: {type(s.engine)}")
gvis(s.engine, "prov_DOME01_engine.html")



# Namespaces
DOME = Namespace("http://dome40.eu/")
PROV = Namespace("http://www.w3.org/ns/prov#")

# Create a new graph
g=s.create_graph(DOME.g1)
g2=s.create_graph(DOME.g2)
# fix me, to simplify, we define a default_graph keyword which can be different names for
# different sessions! hence we do not need to have session.add() but rather just get the graph work on it. the
# session provides simple interface to the graph. A Cuds, does not need be assigned to a specific session,
# but we need to think about copies. At the same time, we are allowing access to teh graph by passing the session!
# the better option is that create graph (and other similar methods) return the g_id, and only the session is the
# interface to create the datasets.

# Bind the namespaces
g.bind("DOME", DOME)
g.bind("prov", PROV)

# Create entities
dataset = DOME.Dataset1 # fixme: this should be Cuds, which will be added to the graph later.

g.add((dataset, RDF.type, PROV.Entity))
g.add((dataset, RDF.type, DOME.DataSet))
g.add((dataset, RDFS.label, Literal("Dataset1", datatype=XSD.string)))

# Create agents
user1 = DOME.User1
g.add((user1, RDF.type, PROV.Agent))
g.add((user1, RDF.type, DOME.User))

g.add((user1, FOAF.name, Literal("Muster Musterman", datatype=XSD.string)))

user2 = DOME.User2
g.add((user2, RDF.type, PROV.Agent))
g.add((user2, RDF.type, DOME.User))
g.add((user2, FOAF.name, Literal("Muster Musterfrau", datatype=XSD.string)))

user3 = DOME.User3
g.add((user3, RDF.type, PROV.Agent))
g.add((user3, RDF.type, DOME.User))

g.add((user3, FOAF.name, Literal("John Doe", datatype=XSD.string)))

# Activities
upload = DOME.Upload
g.add((upload, RDF.type, PROV.Activity))
g.add((upload, RDFS.label, Literal("Upload Dataset", datatype=XSD.string)))

update = DOME.Update
g.add((update, RDF.type, PROV.Activity))
g.add((update, RDFS.label, Literal("Update Dataset", datatype=XSD.string)))

acquire = DOME.Acquire
g.add((acquire, RDF.type, PROV.Activity))
g.add((acquire, RDFS.label, Literal("Acquire Dataset", datatype=XSD.string)))

# Linking entities, activities, and agents
g.add((upload, PROV.wasAssociatedWith, user1))
g.add((upload, PROV.used, dataset))
g.add((dataset, PROV.wasGeneratedBy, upload))

g.add((update, PROV.wasAssociatedWith, user2))
g.add((update, PROV.used, dataset))
g.add((dataset, PROV.wasDerivedFrom, dataset))
g.add((dataset, PROV.wasGeneratedBy, update))

g.add((acquire, PROV.wasAssociatedWith, user3))
g.add((acquire, PROV.used, dataset))
s.add_triple(DOME.DataSet2, DOME.has, DOME.Nothing)
# Output the graph in RDF/XML format
#print(g.serialize(format="turtle"))


gvis(g, "prov_DOME01.html")

for i in s.graphs():
    print ("i=",i)

s.list_graphs()

for s, p, o, g in s.quads():
    print (s, p, i, g)
