from rdflib import Namespace

MIO=Namespace("http://www.ddmd.io/mio#")
CUDS=Namespace("http://www.ddmd.io/mio/cuds#")
MISO=Namespace("http://www.ddmd.io/miso/")
DOMEDS = Namespace("http://dome40.eu/semantics/dome4.0_core_dataset#")
# Export the CUDS namespace for direct import
__all__ = ["CUDS"]
