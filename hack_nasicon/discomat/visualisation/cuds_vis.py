"""
Visualisation of cuds graphs using Javascript via NetworkX and Pyvis

This version works well, for now, I only need to figure out why the title comes up double (heading)!


The main purpose is to get a graph, assuming it is not huge, and focusing on showing the main class and individual relations with basic filtering. 

"""
import argparse, urllib.parse, os
from typing import Union
import networkx as nx
from pyvis.network import Network
from rdflib import Graph, URIRef, RDF, RDFS, OWL
from discomat.cuds.utils import uuid_from_string, short_uuid
from discomat.cuds.cuds import Cuds
from discomat.cuds.session import Session
from discomat.cuds.utils import extract_fragment

def gvis(graph: Union[Graph, Cuds], output_html_file: str = 'mygraph.html'):
    """
    Plot the RDF graph using NetworkX and Pyvis. 
    Showing only the fragments of IRIs and ignoring RDFS.comments.

    :param graph: The RDFLib graph to vizualize.

    Could be a single CUDS or a whole graph, though performance could be an issue.


    :param output_html_file: The HTML/JS output. Simply open in a browser!

    fixme: add option to support notebooks.
    """

    #G = nx.DiGraph()
    G = nx.MultiDiGraph()
    """
    A MultiDiGraph in Python's NetworkX library is a 
    directed graph that allows multiple edges between any pair of nodes. 
    """
    if isinstance(graph, Session):
        x=Graph()
        for g in graph:
            x=x+g
        graph = x+graph._graph
    elif isinstance(graph, Cuds):
        graph = graph._graph

    for s, p, o in graph:

        # Ignore comments, as some are quite large.
        if p == RDFS.comment:
            continue

        if (p == RDF.type and o in {RDFS.Class, OWL.Class, OWL.DatatypeProperty, OWL.ObjectProperty,
                                    OWL.NamedIndividual}):
            continue

        if (p in {RDFS.range, RDFS.domain}):
            continue

        s_fragment = extract_fragment(str(s))
        p_fragment = extract_fragment(str(p))
        o_fragment = extract_fragment(str(o))

        # s_fragment = uuid_from_string(s_fragment, 5) or s_fragment
        # o_fragment = uuid_from_string(o_fragment, 5) or o_fragment
        if len(o_fragment)>8:
            o_fragment = short_uuid(o_fragment)

        if len(s_fragment) > 8:
            s_fragment = short_uuid(s_fragment)


        # fixme: quick code, it has duplication and not efficient...

        # Identify if the subject or object is a class
        if (s, None, RDFS.Class) in graph or (s, None, OWL.Class) in graph:
            G.add_node(s_fragment, title=str(s), color='orange')  # classes are RED
        elif (s, None, None) not in graph:
            G.add_node(s_fragment, title=str(s), color='green')
        else:
            G.add_node(s_fragment, title=str(s), color='red')

        if (o, None, RDFS.Class) in graph or (o, None, OWL.Class) in graph:
            G.add_node(o_fragment, title=str(o), color='orange')
        elif (o, None, None) not in graph:
            G.add_node(o_fragment, title=str(o), color='green')
        else:
            G.add_node(o_fragment, title=str(o), color='red')

            # Add edges, using thick orange for subclass relations
        edge_color = 'orange' if p == RDFS.subClassOf else 'red'
        edge_width = 5 if p == RDFS.subClassOf else 2

        G.add_edge(s_fragment, o_fragment, label=p_fragment, title=str(p), color=edge_color, width=edge_width)
        # edges = G.edges(data=True)
        # for edge in edges:
        #     print(edge)
    # Create a Pyvis network
    net = Network(
        height='850px',
        heading=f"Visualisation of {output_html_file}",
        neighborhood_highlight=True,
        directed=True,
        notebook=False,  # Ensure this is set to False for non-notebook environments
        select_menu=True,  # Optional: to select nodes and edges in the plot
        filter_menu=True

    )

    net.set_options("""
    var options = {
        "configure": {
    "enabled": true,
    "filter": ["physics"]
        },
        "physics": {
    "barnesHut": {
      "gravitationalConstant": -36200,
            "springLength": 40

    },
    "minVelocity": 0.75
  }
    }
    """)

    net.from_nx(G)  # Create directly from the NetworkX graph

    #net.show_buttons(filter_=['physics', 'nodes'])  # Show physics control in the UI
    # for edge in net.edges:
    #     print(edge)
    # Save the network to an HTML file
    net.write_html(output_html_file)  # Write HTML file

    file_uri = os.path.join(os.getcwd(), output_html_file)
    file_uri = f"file://{urllib.parse.quote(file_uri)}"

    print(f"Graph saved to {file_uri}")

# Usage example
# g = Graph()
# g.parse(data='''
#     @prefix ex: <http://example.org/> .
#     @prefix foaf: <http://xmlns.com/foaf/0.1/> .
#     @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
#     @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
#     @prefix prov: <http://www.w3.org/ns/prov#> .
# 
#     ex:Person a rdfs:Class;
#              rdfs:subClassOf prov:Agent .
# 
#     ex:PersonA rdf:type ex:Person;
#                foaf:knows ex:PersonB ;
#                ex:worksAt ex:CompanyX ;
#                foaf:name "Alice" .
# 
#     ex:PersonB rdf:type ex:Person;
#                foaf:name "Bob" .
# 
#     ex:CompanyX ex:locatedIn "CityY" .
# ''', format='turtle')
# 
# pyvis_graph_to_js(g, 'rdf_graph.html')
# 
# 
# g2=Graph()
# g2.parse("/Users/adham/dev/materials-discovery/MIO/mio/mio.ttl")
# pyvis_graph_to_js(g2, 'rdf_graph3.html')
# 
# 
# n=Graph()
# n.parse("/Users/adham/Downloads/nasicon.ttl")
# pyvis_graph_to_js(n, 'nasicon_graph.html')
#
def main():
    parser = argparse.ArgumentParser(description="Visualize an ontology into a javascript/html file.")

    parser.add_argument('in_file', type=str, help='Input File Path  (e.g.; ontology.ttl).')
    parser.add_argument('out_file', type=str, nargs='?', default='mygraph.html', help='HTML File Path  (e.g.; '
                                                                                      'ontology.html).')

    args = parser.parse_args()

    g = Graph()
    g.parse(args.in_file)
    gvis(g, args.out_file)


# Check if the script is being run directly
if __name__ == "__main__":
    main()