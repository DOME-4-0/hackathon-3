import uuid, datetime
from collections import defaultdict
from urllib.parse import urlparse, urldefrag, urlsplit

from rdflib import Dataset, Graph, URIRef, Literal, RDF, RDFS
from rdflib.namespace import DC, DCTERMS, PROV, XSD
from rdflib import Namespace

from discomat.ontology.namespaces import CUDS, MIO
from discomat.cuds.cuds import Cuds
from discomat.cuds.engine import Engine, RdflibEngine

from pyvis.network import Network
from IPython.display import display, HTML

from abc import ABC, abstractmethod

import os, sys, warnings, pickle

from types import MappingProxyType
from typing import Union
import threading


class SessionManager:
    """
    # not making this a CUDS for now, too complex..
    The session manager is essentially a session tracker, as the actual management is done
    directly by the session instances themselves who have access to all information, but we need a reference to
    store information about all sessions open in one python run.

    we could have just defined this as a
        - class variable (as an instance session manager). This could be confusing as we could instantiate another
        session manager.
        - all tracking state is stored as a data structure in the session class again as class variables. could be
        cumbersome to maintain.

        - as a singelton class, contacted by the various sessions in order to
            - register them selves when created
            - deregister when closed
            - convey any other needed provenance related information.

    """

    # Singleton setup
    # class variable, flag is not none if the sclass is instantiated

    _self = None

    # this overrides the new method to check if _self is set!
    def __new__(cls):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self

    def __init__(self):
        self._sessions = {}
        self.created = datetime.datetime.now()
        self._provenance_graph = Graph()  # should this be here?

        self._sessions = {}
        self._engines = {}  # Maps engine object to session object
        self._lock = threading.Lock()

    def register(self, session: 'Session'):
        #     if session.session_id in self._sessions:
        #         raise ValueError(f"Session {session.session_id} with label {session.label}  already exists.")
        #     self._sessions[session.session_id] = session
        #     self._provenance_graph.add((session.iri, RDF.type, URIRef("http://www.ddmd.io/mio#Session")))
        #     self._provenance_graph.add((session.iri, RDF.type, PROV.Entity))
        #     self._provenance_graph.add((session.iri,
        #                                 self._provenance_graph.add((session.iri, DC.identifier, Literal(session.uuid)))
        #     self._provenance_graph.add((session.iri, DCTERMS.created, Literal(session.creation_time)))
        #     self._provenance_graph.add((session.IRI, DC.identifier, Literal(session.uuid)))
        #
        #     return True
        with self._lock:
            from discomat.cuds.session import Session

            if session.uuid in self._sessions:  # compare the keys
                raise ValueError(f"Session {session.iri} is already registered and active")

            if session.engine.uuid in self._engines:
                s_uuid = self._engines[session.engine.uuid]
                raise ValueError(f"Engine {session.engine.uuid} is already in use by session "
                                 f"{self._sessions[s_uuid].iri}")

            self._sessions[session.uuid] = session
            self._engines[session.engine.uuid] = session.uuid

    def get_session(self, uuid):
        return self._sessions.get(uuid, False)  # return session if exits, else false.

    @property
    def sessions(self):
        return MappingProxyType(self._sessions)

    @property
    def engines(self):
        return MappingProxyType(self._engines)

    def remove(self, session_uuid):
        # when you remove a session, also close the engine, unless we want to allow for another session to use it..

        with self._lock:
            session = self._sessions.pop(session_uuid, None)
            if session.engine:
                engine = self._engines.pop(session_uuid, None)
                # we keep the engine now open, but it should be more explicit. for now we return the engine.

    def info(self):
        print(f"Session id\tDescription\tlabel\t\tEngine id\tDescription\tlabel")

        with self._lock:
            for id, session in self._sessions:
                print(f"{id}\t{session.description}\t{session.label}l\t\t{session.engine.uuid}\t"
                      f"{session.engine.description}\t{session.engine.label}")
