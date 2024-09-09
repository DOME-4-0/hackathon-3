from datascrap.app import handler

# Part 1
# In this exercise, we'll use NLPs to search and download papers from arXiv

# Select keywords and topics of papers to download
event = {
    'keyphrases': 'ML',
    'queries': {'DFT': 'nasicon'},
    'num_results': 5
}

context = {}

result = handler(event, context)

# Convert the keyphrases and queries from the event
keyphrases = event['keyphrases'].split('-')
queries = event['queries']

print(result)


# Part 2

from discomat.cuds.cuds import Cuds
from discomat.visualisation.cuds_vis import gvis
from discomat.ontology.namespaces import DOMEDS
import csv

# Now we'll use del to create a dataset of the downlaoded papers

# Load dataset from CSV
with open('papers/metadata.csv', mode='r') as file:
    reader = csv.reader(file)
    headers = next(reader)  # Read the headers

    # Here we'll use list comprehension instead of creating each triple line by line

    # Clean and map the headers to ontology fields
    ontology_fields = [getattr(DOMEDS, header.strip()) for header in headers if header.strip()]

    # Read the dataset rows
    dataset = [tuple(row) for row in reader]

gall = []

# Loop through the dataset and create CUDS objects
for data in dataset:
    ds_001 = Cuds(ontology_type=DOMEDS.data_set, description="Example of DOME4.0 dataset")

    # Use list comprehension to add each field to the CUDS object
    [ds_001.add(field, value) for field, value in zip(ontology_fields, data)]

    print(ds_001)


    # accumulate the current dataset graph to gall
    gall += ds_001.graph

# Visualize the combined graph and export to HTML
gvis(gall, "papers.html")