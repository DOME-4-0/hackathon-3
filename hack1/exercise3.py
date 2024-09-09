from datascrap.app import handler
import pandas as pd
import os

# In this exercise, we'll map to the metadata of the papers dataset with the DOME dataset ontology
def map_and_save_metadata(df, file_path, keyphrases=None, queries=None):
    """
    Map the dataframe columns to the custom ontology headers and save it as a CSV file.

    Args:
        df (pd.DataFrame): The dataframe containing paper information.
        file_path (str): The file path where the CSV will be saved.
        keyphrases (list): A list of keyphrases (semantic keywords).
        queries (dict): A dictionary of queries used (syntactic keywords).
    """
    # Map the DataFrame columns to custom headers
    df['has_dataset_creator'] = df['authors']  # Mapping authors to creator
    df['has_dataset_license'] = ''  # Assuming no license information available
    df['has_dataset_publisher'] = 'arXiv'  # Publisher set to arXiv
    df['has_dataset_topic'] = df['categories']  # Mapping categories to topic
    df['has_dataset_description'] = df['abstract']  # Mapping abstract to description
    df['has_dataset_issued_date'] = df['year']  # Mapping year to issued date
    df['has_dataset_semantic_keyword'] = ','.join(keyphrases) if keyphrases else ''  # Mapping keyphrases
    df['has_syntactic_keyword'] = ','.join(queries.keys()) if queries else ''  # Mapping queries
    df['has_dataset_title'] = df['title']  # Mapping title to dataset title

    # Specify the custom columns order for the CSV file
    custom_columns = [
        'has_dataset_creator',
        'has_dataset_license',
        'has_dataset_publisher',
        'has_dataset_topic',
        'has_dataset_description',
        'has_dataset_issued_date',
        'has_dataset_semantic_keyword',
        'has_syntactic_keyword',
        'has_dataset_title'
    ]

    # Save the DataFrame with custom headers to CSV
    df.to_csv(file_path, columns=custom_columns, index=False, encoding='utf-8')

    print(f"Metadata saved to {file_path}")


event = {
    'keyphrases': 'nasicon',
    'queries': {'DFT': 'ML'},
    'num_results': 5
}

context = {}

result = handler(event, context)

# Convert the keyphrases and queries from the event
keyphrases = event['keyphrases'].split('-')
queries = event['queries']

# Create a local folder to save the CSV
local_folder = './papers'
os.makedirs(local_folder, exist_ok=True)

# Save the mapped dataframe to CSV using the custom headers
metadata_file = os.path.join(local_folder, 'metadata_custom.csv')
df = pd.DataFrame(result['dataframe'])  # Convert the result into a DataFrame
map_and_save_metadata(df, metadata_file, keyphrases=keyphrases, queries=queries)


print(result)

# Part 2

# This time we'll make a CUDS using the DOMEDS ontology

from discomat.cuds.cuds import Cuds
from discomat.visualisation.cuds_vis import gvis
from discomat.ontology.namespaces import DOMEDS
import csv

# Now we'll use del to create a dataset of the downlaoded papers

# Load dataset from CSV
with open('papers/metadata_custom.csv', mode='r') as file:
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
