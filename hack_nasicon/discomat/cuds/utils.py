import random
import re
import uuid
from functools import wraps
from typing import Union

from mnemonic import Mnemonic
from rdflib import URIRef, Literal


def to_iri(e: Union[str, URIRef]):
    try:
        # first, we assume it is a CUds (we do not want to import it to avoid circular import).
        e = to_iri(e.iri)
    except AttributeError:
        if isinstance(e, str) and (e.startswith("http://") or e.startswith("https://")):
            e = URIRef(e)
        elif isinstance(e, URIRef):
            pass
        elif isinstance(e, uuid.UUID):
            e = Literal(e)
        elif e is None:
            return Literal("None")
        else:
            e = Literal(str(e))
    return e


def uuid_from_string(s: str = None, length: int = None):
    """

    scan string, identify a UUID part and either return it in whole, or the last length chars.
    """

    # Regular expression pattern for UUID
    # uuid_pattern = re.compile(r'\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b')
    uuid_pattern = re.compile(r'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}')

    # Search for UUID in the string
    match = uuid_pattern.search(s)

    if match:
        # Extract the UUID
        uuid = match.group(0)
        return uuid if length is None else uuid[-5:]
    else:
        return None


def short_uuid(s: str) -> str:
    # Regular expression to find the UUID pattern in the string
    uuid_pattern = r'(\w{8}-\w{4}-\w{4}-\w{4}-\w{12})'

    match = re.search(uuid_pattern, s)
    if not match:
        if len(s) > 50:
            return (s[-12:])
        else:
            return (s)
    # Everything before the UUID is treated as the prefix
    prefix = s[:match.start()]
    uuid = match.group(1)

    # Get the last 4 characters of the UUID
    short_suffix = uuid[-4:]

    # Combine prefix with short suffix
    return f"{prefix}{short_suffix}".rstrip('_')  # Remove trailing underscore if no prefix


def extract_fragment(iri):  # we have this in so many versions and incarnations, should fixme move to utils
    """extract the fragment or the last part of an IRI."""
    return iri.split('#')[-1].split('/')[-1]


def mnemonic_label(number_of_words: int = 2):
    # word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
    # response = requests.get(word_site)
    # WORDS = response.content.splitlines()
    # print (WORDS)

    mnemo = Mnemonic("english")
    words = mnemo.generate(strength=128)
    label = '_'.join(random.sample(list(words.split()), number_of_words))
    # seed = mnemo.to_seed(words, passphrase="")
    # entropy = mnemo.to_entropy(words)
    return label


def _arg_to_iri(func):
    def wrapper(*args, **kwargs):
        args = tuple(to_iri(arg) for arg in args)
        kwargs = {key: to_iri(value) for key, value in kwargs.items()}
        return func(*args, **kwargs)

    return wrapper


def arg_to_iri(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if args and hasattr(args[0], "__class__"):
            self, *new_args = args
            new_args = tuple(to_iri(arg) for arg in new_args)
            new_kwargs = {key: to_iri(value) for key, value in kwargs.items()}
            return func(self, *new_args, **new_kwargs)
        else:
            new_args = tuple(to_iri(arg) for arg in args)
            new_kwargs = {key: to_iri(value) for key, value in kwargs.items()}
            return func(*new_args, **new_kwargs)

    return wrapper


def pr(s):
    print(s.format(**locals()))


def prd(s):
    dashes = '-' * len(s)
    # print(dashes)
    print(s)
    print(dashes)


"""
simple but often used sparql queries

"""


class query_lib:
    @staticmethod
    def all_triples():
        return """
        SELECT ?s ?p ?o WHERE {
          ?s ?p ?o .
        }"""

    @staticmethod
    def all_subjects():
        return """
        SELECT DISTINCT ?s WHERE {
          ?s ?p ?o .
        }"""

    @staticmethod
    def all_predicates():
        return """
        SELECT DISTINCT ?p WHERE {
          ?s ?p ?o .
        }"""

    @staticmethod
    def all_objects():
        return """
        SELECT DISTINCT ?o WHERE {
          ?s ?p ?o .
        }"""

    @staticmethod
    def subject_contains(substring):
        return f"""
        SELECT ?s ?p ?o WHERE {{
          ?s ?p ?o .
          FILTER(CONTAINS(LCASE(STR(?s)), "{substring.lower()}"))
        }}"""

    @staticmethod
    def all_objects_containing(substring):
        return f"""
        SELECT ?s ?p ?o WHERE {{
          ?s ?p ?o .
          FILTER(CONTAINS(LCASE(STR(?o)), "{substring.lower()}"))
        }}"""

    @staticmethod
    def all_subjects_containing(substring):
        return f"""
        SELECT ?s ?p ?o WHERE {{
          ?s ?p ?o .
          FILTER(CONTAINS(LCASE(STR(?s)), "{substring.lower()}"))
        }}"""

    @staticmethod
    def all_predicates_containing(substring):
        return f"""
            SELECT ?s ?p ?o WHERE {{
              ?s ?p ?o .
              FILTER(CONTAINS(LCASE(STR(?p)), "{substring.lower()}"))
            }}"""

    @staticmethod
    def all_triples_with_literal_objects():
        return """
            SELECT ?s ?p ?o WHERE {
              ?s ?p ?o .
              FILTER(isLiteral(?o))
            }"""
