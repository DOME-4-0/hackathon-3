import copy
import uuid, datetime
from collections import defaultdict
from urllib.parse import urlparse, urldefrag, urlsplit
from rdflib import Dataset, Graph, URIRef, Literal, RDF, RDFS
from rdflib.namespace import DC, DCTERMS, PROV, XSD
from rdflib import Namespace
from discomat.cuds.utils import mnemonic_label, to_iri, arg_to_iri
from discomat.ontology.namespaces import CUDS, MIO
from discomat.cuds.cuds import Cuds, ProxyCuds
from discomat.cuds.session_manager import SessionManager
from discomat.cuds.engine import Engine, RdflibEngine
from pyvis.network import Network
from IPython.display import display, HTML

from abc import ABC, abstractmethod

import os, sys, warnings, pickle

from types import MappingProxyType
from typing import Union


class Session(Cuds):
    """
    Open a session, which by default uses the default local engine (its just easier way for us to handle the
    dataset of rdflib essentially).
    """

    def __init__(self,
                 iri: Union[str, URIRef] = None,
                 pid: Union[str, URIRef] = None,
                 description: str = None,
                 label: str = None,
                 engine: 'Engine' = None
                 ):
        ontology_type = CUDS.Session
        description = description or f"Session: No Description provided, dont be lazy.."
        super().__init__(ontology_type=ontology_type, iri=iri, pid=pid, description=description, label=label)

        self.remove(CUDS.Session, self.session)  # a session has no session
        self.engine = engine or RdflibEngine()  # this is teh actual engine
        self.engine_iri = self.engine.iri

        # new relationship, should be added and tracked. fixme: use the __set and __get attr methods to automanage.
        self.session_id = self.uuid

        self.is_open = False  # this is a helper, we do not need it in the ontology.

        # we need to define the graphs managed by the session, these are managed by the engire.
        # dict of all graphs.
        self._session_graphs = {'default_graph_id': self.engine.default_graph_id}
        self.add(CUDS.hasGraphId, self.engine.default_graph_id)
        self.default_graph_id = self.engine.default_graph_id

        self.session_manager = SessionManager()  # fixme: move the definition of SessionManager before Session.
        self.session_manager.register(self)  # pass self to session manager
        # Note: for q in d.quads((None, None, None, URIRef('urn:x-rdflib:default'))):
        #     print(q)

    def create_graph(self, graph_id):
        """
            Note: Session Graphs are not to be confused with teh _graph of a CUDS object,
            session graphs are entire knowledge graphs and not those that have only direct relations
            with one main root subject. Cuds objects (and triplets) live in these Graphs.
        """
        try:
            engine_graph_id = self.engine.create_graph(graph_id)
            self._session_graphs[graph_id] = engine_graph_id
            self.add(CUDS.hasGraphId, engine_graph_id)
            return engine_graph_id

        except ValueError as e:
            print(f"Engine could not create graph {graph_id}: returned {e} as error")
            return None

    # conflicts with cuds.graph method
    # def graph(self, graph_id):
    #    return self.create_graph(graph_id)

    def remove_graph(self, graph_id):
        try:
            self.engine.remove_graph(graph_id)
            if graph_id in self._session_graphs:
                del self._session_graphs[graph_id]
            self._graph.remove((to_iri(self.iri), to_iri(CUDS.hasGraph), to_iri(graph_id)))
        except KeyError:
            raise ValueError(f"Graph '{graph_id}' is not found in the session {e}")

        except RuntimeError as e:
            raise ValueError(f"Graph '{graph_id}' does not exist in this engine. {e}")

    def __iter__(self):
        return iter(self.engine)

    def __contains__(self, triple):
        # Delegate
        s, p, o = triple
        # Delegate
        s = to_iri(s)
        p = to_iri(p)
        o = to_iri(o)
        for g in self:
            if (s, p, o) in g:
                return True
        return False

    def quads(self, s=None, p=None, o=None, g=None):
        return self.engine.quads(to_iri(s), to_iri(p), to_iri(o), g)

    def triples(self, s=None, p=None, o=None):
        return self.engine.quads(s, p, o)

    def list_graphs(self):
        l = []
        # return a list of all graphs (graph_id's)
        for g in self.engine.graphs:
            l.append(g)
        return l

    def graphs(self):
        return self.engine.graphs

    def query(self, query=None):
        """
        sparql query
        ecample:


        query = \"""
            SELECT ?s ?p ?o
        WHERE {
        GRAPH <http://example.org/graph1> {
         ?s ?p ?o .
              }
            }
            \"""


        """
        if query is None:
            query = """
                    SELECT ?s ?p ?o
                    WHERE {
                    ?s ?p ?o .
                    }
                    """
        # by default, all the graphs are queried (Conjuctive) unless a graph is specified.
        return self.engine.query(query)

    @arg_to_iri
    def add_triple(self, s=None, p=None, o=None):
        # added None as python does not allow no default following default
        # if not any([s, p, o]):  # or use all() for all not None, not sure...
        #     raise ValueError("s, p, and o are all None, at least one should be not None")
        # print(f"need to check provenance...")
        self.engine.add_triple(s, p, o)

    @arg_to_iri
    def add_quad(self, s=None, p=None, o=None, g_id=None):
        # added None as python does not allow no default following default
        # if not any([s, p, o]):  # or use all() for all not None, not sure...
        #     raise ValueError("s, p, and o are all None, at least one should be not None")
        # print(f"need to check provenance...")
        self.engine.add_quad(to_iri(s), to_iri(p), to_iri(o), g_id)

    @arg_to_iri
    def remove_triple(self, s=None, p=None, o=None):
        if not any([s, p, o]):  # or use all() for all not None, not sure...
            raise ValueError("s, p, and o are all None, at least one should be not None")
        self.engine.remove_triple(s, p, o)  # need to add provenance...

    @arg_to_iri
    def remove_quad(self, s=None, p=None, o=None, g_id=None):
        if not any([s, p, o]):  # or use all() for all not None, not sure...
            raise ValueError("s, p, and o are all None, at least one should be not None")
        self.engine.remove_quad(s, p, o, g_id)  # need to add provenance...

    def add_cuds(self, cuds: Cuds, g_id=None):
        """add the cuds to the session, optionally specifying the graph.  """
        # every cuds instance (version) can belong to one and only one session
        #
        cuds.session_id = self.session_id
        self.engine.add_cuds(cuds, g_id)

        return ProxyCuds(cuds)

    def get_cuds(self, iri):
        """
        given an iri or the Cuds, search the session, i.e., all graphs for the
        properties needed for this Cuds.
        A Cuds is an iri with all direct relations including the basic ones (uuid, pid, etc).
        if A cuds cannot be built, create one using any partial information available
        """
        return NotImplemented

    def remove_cuds(self, iri):
        """
        """
        return NotImplemented

    def search_cuds(self, cuds):
        """ search for the CUDS, find if it is in the system using the iri of the CUDS
        could be replaced by smart __contains__ method, that based on the type of element queried, activates various
        methods. could be as simple as calling the engine with cuds iri on all graphs. """

        return NotImplemented

    def get_cuds_region(self, cuds, radius):
        """        get the cuds up to a specific radius
        could be same as get_cuds but with optional radius, see ontology manager etc for implementations.

        """

    def proxy_cuds(self, cuds_iri, *args, **kwargs):
        """

        Parameters
        ----------
        cuds_iri
        args
        kwargs
        """
        print(f"calling proxy cuds with {args} and {kwargs}")

    def proxy_handler(self, *, iri, ops, **kwargs):
        if iri is None:
            raise ValueError("iri in proxy handler CANNOT be not be None")
        run = {
            'setattr': self.proxy_setattr,
            'getattr': self.proxy_getattr,
            'properties': self.proxy_properties,
            'serialise': self.proxy_serialise,
            'add':self.proxy_add,
            'iter': self.proxy_iter
        }

    def proxy_setattr(self, *, iri, **kwargs):
        print(f"setting attribute of proxy cuds")
        """
        basically use the query or update of the engine (sparql really) to do the changes."""
        pass

    def proxy_getattr(self, *, iri, **kwargs):
        print(f"getting attribute of proxy cuds")
        pass

    def proxy_properties(self, *, iri, **kwargs):
        print(f"properties of proxy cuds")
        pass
