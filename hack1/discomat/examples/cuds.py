from discomat.cuds.cuds import Cuds
from discomat.visualisation.cuds_vis import gvis
from discomat.cuds.utils import uuid_from_string, to_iri
from discomat.cuds.session import Session
from rdflib import URIRef, Graph
import copy

c = Cuds()
print(c)  # pretty print, organised to name spaces.
c.print_graph()  # simply print the serialised graph

# test plot of Cuds
gvis(c, f"c.html")

# test adding triplet to Cuds

# first adding using string (iri)
c.add("https://predicate.org/predicate_str_iri", "https://subject.org/subject_str_iri")

# then adding using URIRef's
c.add(URIRef("https://predicate.org/predicate_uriref_iri"), URIRef("https://subject.org/subject_uriref_iri"))

#  adding using IRI (str) and URIRef's
c.add("https://predicate.org/1predicate_str_iri", URIRef("https://1subject.org/subject_uriref_iri"))

#  adding using Cuds
c2=Cuds()
c.add("https://predicate.org/1predicate_str_iri",c2) # fixme

print(f"c after adding some triples")
gvis(c, "c_after_adding_triplets.html")
print(c)  # pretty print, organised to name spaces.


print(f"Testing the Cuds.remove Method")
# c1 = Graph().parse(data=c.serialize(format="turtle"), format="turtle")
c3=copy.deepcopy(c)
gvis(c2, "deep_copy_c.html")
c2.add("ThePredicate", "TheObject")
gvis(c2, "c1.html")
c3=copy.deepcopy(c2)
c3.remove("ThePredicate", "TheObject")
gvis(c3, "c3.html")

cdiff = c2.graph - c3.graph
gvis(cdiff, "cdiff.html") # gvis works both on Cuds and graph alike.


print(f"TESTING Iter on Cuds: \n{50*'-'}")
triple_count=0
for s, p, o in c.graph:
    triple_count=triple_count +1

print(f"c has  {len(c._graph)} == {triple_count} triples")
assert (len(c._graph) == triple_count), f"iterator is not working"

if (c.rdf_iri, None, None) in c.graph:
    print("Cuds contains triples about itself!")
else:
    print(f"Something is Wrong {c.rdf_iri}")
