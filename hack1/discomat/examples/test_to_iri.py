from discomat.cuds.cuds import Cuds
from discomat.visualisation.cuds_vis import gvis
from discomat.cuds.utils import uuid_from_string, to_iri
from discomat.cuds.session import Session
from rdflib import URIRef, Graph
import copy

c = Cuds()
print(f"TESTING to_iri \n {50 * '='}")

original_iri = "https://predicate.org/predicate"
obtained_iri = to_iri(original_iri)
print(f"original_iri: {original_iri} of type {type(original_iri)}")
print(f"Testing to_iri: obtained_iri = {obtained_iri} is of type: {type(obtained_iri)}")
assert isinstance(obtained_iri, URIRef)

original_iri = URIRef("https://predicate.org/predicate")
obtained_iri = to_iri(original_iri)
print(f"original_iri: {original_iri} of type {type(original_iri)}")
print(f"Testing to_iri:  obtained_iri = {obtained_iri} is "
      f"of type:"
      f" {type(obtained_iri)}")
assert isinstance(obtained_iri, URIRef), f"Expected type URIRef but got {type(obtained_iri)}"

original_iri = c.iri
obtained_iri = to_iri(original_iri)
print(f"original_iri: {original_iri} of type {type(original_iri)}")
print(f"Testing to_iri: obtained_iri = {obtained_iri} is of type: {type(obtained_iri)}")
assert isinstance(obtained_iri, URIRef)
