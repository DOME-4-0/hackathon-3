from discomat.cuds.cuds import Cuds
from discomat.visualisation.cuds_vis import gvis
from discomat.cuds.utils import uuid_from_string, to_iri
from discomat.cuds.session import Session
from rdflib import URIRef, Graph
import copy

c = Cuds()
print(c)  # pretty print, organised to name spaces.
c.print_graph()  # simply print the serialised graph


# test uuid_from_string
print(uuid_from_string(c.pid, 4))
str = "http://www.ddmd.io/mio#cuds_iri_b1b9e5d0-2a03-4665-a073-8feb57742fb1"
expected_uuid = "b1b9e5d0-2a03-4665-a073-8feb57742fb1"
extracted_uuid = uuid_from_string(str)
assert extracted_uuid == expected_uuid, f"Expected {expected_uuid} but got {extracted_uuid}"
