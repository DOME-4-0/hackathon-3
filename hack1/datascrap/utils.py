import arxiv
import pandas as pd
from tqdm.auto import tqdm
import urllib
import csv
def df_from_query(query, num_of_results=10):
    """
    Extract information from papers using arXiv API.
    Args:
        query (str): the query to search for
        num_of_results (int): the number of results that you want
    Returns:
        df (pandas DataFrame): a dataframe with information for the papers
    """
    search = arxiv.Search(
        query=query,
        max_results=num_of_results,
        sort_by=arxiv.SortCriterion.Relevance
    )

    df = pd.DataFrame(columns=['entry_id', 'title', 'abstract', 'authors', 'categories', 'pdf_url'])
    i = 0
    for result in search.results():
        title = result.title
        authors = result.authors
        abstract = result.summary
        categories = result.categories
        pdf_url = result.pdf_url

        authors_ = " ,".join(str(x) for x in authors)
        categories_ = " ,".join(str(x) for x in categories)

        df.loc[i, 'entry_id'] = result.entry_id
        df.loc[i, 'title'] = title
        df.loc[i, 'abstract'] = abstract.replace("\n", " ")
        df.loc[i, 'authors'] = authors_
        df.loc[i, 'categories'] = categories_

        df.loc[i, 'year'] = int(result.published.year)
        df.loc[i, 'pdf_url'] = pdf_url
        i += 1

    return df

def get_df_from_queries(queries, num_results=300):
    dfs = []
    for key in tqdm(queries):
        df_temp = df_from_query(queries[key], num_of_results=num_results)
        df_temp['text'] = df_temp['title'] + ' ' + df_temp['abstract']
        dfs.append(df_temp)

    df = pd.concat(dfs, ignore_index=True, sort=False)
    df.drop_duplicates(subset=["title"], keep=False, inplace=True, ignore_index=True)
    return df

def download_pdf(download_url, filename):
    try:
        response = urllib.request.urlopen(download_url)
        with open(filename + ".pdf", 'wb') as file:
            file.write(response.read())
    except Exception as e:
        print(f"Error downloading PDF: {e}")


import csv


def save_metadata_to_csv(df, file_path):
    """
    Save the metadata of papers to a CSV file.

    Args:
        df (pd.DataFrame): The dataframe containing paper information.
        file_path (str): The file path where the CSV will be saved.
    """
    # Specify the columns to save
    columns_to_save = ['title', 'authors', 'abstract', 'year', 'pdf_url']

    # Add a constant publisher as 'arXiv'
    df['publisher'] = 'arXiv'

    # Save dataframe to CSV
    df.to_csv(file_path, columns=columns_to_save + ['publisher'], index=False, encoding='utf-8')

    print(f"Metadata saved to {file_path}")

