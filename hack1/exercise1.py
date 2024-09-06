from discomat.cuds.cuds import Cuds
from discomat.cuds.session import Session
from discomat.visualisation.cuds_vis import gvis
from discomat.ontology.namespaces import DOMEDS
import csv

# In this exercise we're going to use the DOME dataset ontology to create a CUDS of data for DOME


# Here we'll use the package discomat to create triples of data using the DOME dataset ontology

ds_001 = Cuds(ontology_type=DOMEDS.data_set, description="Example of DOME4.0 dataset")
ds_001.add(DOMEDS.has_dataset_creator, "KOK_FOONG_LEE")
ds_001.add(DOMEDS.has_dataset_license, "licence1")
ds_001.add(DOMEDS.has_dataset_publisher, "DOME4.0_CONSORTIUM")
ds_001.add(DOMEDS.has_dataset_topic, "SEA_Vessels")
ds_001.add(DOMEDS.has_dataset_URL, "https://sintef.sharepoint.com/teams/DOME4.0/Delte%20dokumenter/WP4/T4.1%20Example%20files/Showcase%20#1%20(CMCL)/ship.txt")
ds_001.add(DOMEDS.has_dataset_description, "Ship location example data (for a given ship at a given time")
ds_001.add(DOMEDS.has_dataset_issued_date, "2024-05-31")
ds_001.add(DOMEDS.has_dataset_semantic_keyword, "https://schema.org/Vehicle")
ds_001.add(DOMEDS.has_syntactic_keyword, "ship")
ds_001.add(DOMEDS.has_dataset_title, "DATASET 001")

# Here we can print our dataset
print(ds_001)

# Using the gvis function in discomat we can visualise our dataset

gvis(ds_001, "ds_001.html")


# Part 2

# In this part we will import data from a CSV file

# Initialize session
session = Session()

# Load dataset from CSV
with open('.csv', mode='r') as file:
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
gvis(gall, "ds_002.html")