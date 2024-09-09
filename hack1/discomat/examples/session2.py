from discomat.cuds.cuds import Cuds
from discomat.visualisation.cuds_vis import gvis
from discomat.cuds.utils import uuid_from_string, to_iri
from discomat.cuds.session import Session
from rdflib import URIRef, Graph
import copy
from discomat.ontology.namespaces import CUDS, MISO, MIO


sim = Cuds(MISO.Simulation)

bc=Cuds(MISO.BoundaryConditions)

sim.add(MIO.hasPart, bc)

g=Graph()
g = sim.graph + bc.graph

gvis(sim, "sim.html")

gvis(g, "g.html")


s = Session()
s.add(sim)

# graph into cuds, given a subject, the function searches the graph for label, iri, description, etc and then calls
# Cuds. and then adds the graph to teh _graph of the Cuds, however, we need to check that it contains only first
# order relations! or do we relax this and allow a cuds to be anything?

# we need a tighter control over Cuds.attributes and Cuds._graph. I think I must go back any make sure
"""
1. we can do a search over a graph, and only retain those relations that are first order neighbors to one particular 
subject. 
2. if iri. description, subject, uuid, etc are not in the graph, create them (using __init__). 

we cannot have cuds.attribute which is not first in the graph, and doing cuds.uuid=something should be an interface 
to add it to the cuds_graph. 

rename _graph to cuds_graph. 

cuds are atomic then, in the sense they describe one subject. 

the subject could have graphs, essentially this is session.



Option 2: 

Cuds are not atomic, but can be made so. Hence they can be anything. 

atomic_cuds = To_atom(graph/Cuds). 

what are the interfaces of rdflib graphs? 

"""
