"""
Visualisation of graphs using Javascript via NetworkX and Pyvis

This version works well, for now, I only need to figure out why the title comes up double (heading)!
 """


import networkx as nx
from pyvis.network import Network
from rdflib import Graph, URIRef, RDF, RDFS, OWL
import wget
from discomat.visualisation.cuds_vis import gvis

g = Graph()
g.parse(data='''
    @prefix ex: <http://example.org/> .
    @prefix foaf: <http://xmlns.com/foaf/0.1/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix prov: <http://www.w3.org/ns/prov#> .

    ex:Person a rdfs:Class;
             rdfs:subClassOf prov:Agent .

    ex:PersonA rdf:type ex:Person;
               foaf:knows ex:PersonB ;
               ex:worksAt ex:CompanyX ;
               foaf:name "Alice" .

    ex:PersonB rdf:type ex:Person;
               foaf:name "Bob" .

    ex:CompanyX ex:locatedIn "CityY" .
''', format='turtle')

gvis(g, 'rdf_graph.html')

# note you may need to do this: Install Certificates.command (search the command in your python environment)
mio_url = "http://raw.githubusercontent.com/materials-discovery/MIO/main/mio/mio.ttl"
mio_file = "./mio.ttl"
wget.download(mio_url, out=mio_file)
mio=Graph()
mio.parse("./mio.ttl")
gvis(mio, 'mio_graph.html')
