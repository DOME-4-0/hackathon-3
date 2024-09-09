from discomat.cuds.cuds import Cuds, ProxyCuds
from discomat.cuds.session_manager import SessionManager
from discomat.visualisation.cuds_vis import gvis
from discomat.cuds.utils import uuid_from_string, to_iri
from discomat.cuds.session import Session
from rdflib import URIRef, Graph, PROV, Literal

import copy

from discomat.ontology.namespaces import CUDS, MISO, MIO

sim = Cuds(ontology_type=MISO.Simulation)

# First adding using string (iri)
sim.add(MIO.has, MISO.Method)
sim.add(MIO.has, MISO.MaterialsSystem)

session = Session()
sm = SessionManager()

sim2=session.add_cuds(sim)

# print(sim2)
# sim2=ProxyCuds(sim)
# print(f"and the proxy is: {sim_proxy}")
#
#  /
# print(f"my_simulation={my_simulation} ")
