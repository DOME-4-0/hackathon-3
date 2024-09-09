from discomat.cuds.cuds import Cuds
from discomat.visualisation.cuds_vis import gvis
from discomat.cuds.utils import uuid_from_string, to_iri
from discomat.cuds.session import Session
from rdflib import URIRef, Graph, PROV, Literal
import copy

from discomat.ontology.namespaces import CUDS, MISO, MIO

my_simulation = Cuds(iri=CUDS.MySimulation1, ontology_type=CUDS.Simulation)

# First adding using string (iri)
my_simulation.add(MIO.has, MIO.something_1)
my_simulation.add(MIO.has, MIO.something_2)


provo_cuds = Cuds(ontology_type=CUDS.Provenance, iri=CUDS.MyProvoTest)
provo_cuds.add(PROV.generatedAtTime, Literal("5 pm")) # is this the best way?


my_simulation.add(CUDS.has, provo_cuds)

start_time = Cuds(ontology_type=CUDS.StartTime)  # or this one?
start_time.add(CUDS.hasValue, Literal("5pm"))

end_time = Cuds(ontology_type=CUDS.EndtTime)  # or this one?
end_time.add(CUDS.hasValue, Literal("6pm"))

activity_time = Cuds(CUDS.ActivityTime)
activity_time.add(CUDS.has, start_time)
activity_time.add(CUDS.has, end_time)

provo_cuds.add(CUDS.has, activity_time)

my_simulation.add(CUDS.has, provo_cuds)


other_simulation=Cuds(CUDS.Simulation, iri=CUDS.otherSimulation)
other_simulation.add(PROV.generatedAtTime, Literal("5pm"))
other_simulation.add(PROV.endedAtTime, Literal("6pm"))
other_simulation.add(CUDS.hasCreator, Literal("The Creator"))

print(my_simulation)  # pretty print, organised to name spaces.
my_simulation.print_graph()  # simply print the serialised graph
# test plot of Cuds
gvis(my_simulation, f"my_simulation.html")


# test plot of Cuds
gvis(other_simulation, f"other_simulation.html")

sim1_session = Session(iri=MIO.SessionOne)

