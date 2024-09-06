import os
import utils

def handler(event, context):
    try:
        keyphrases = event['keyphrases'].split('-')
        queries = event['queries']
        num_results = event['num_results']

        # Use ArXiv API to fetch papers
        df = utils.get_df_from_queries(queries, num_results=num_results)
        df['text'] = df['title'] + ' ' + df['abstract']

        # Create a local folder to save downloaded PDFs
        local_folder = './papers'
        os.makedirs(local_folder, exist_ok=True)

        # Download the PDFs locally
        for i in range(df.shape[0]):
            pdf_path = df.iloc[i]['pdf_url']
            filename = df.iloc[i]['title']
            filename = filename.replace('/', ' ')  # Replace characters not suitable for filenames
            filename = filename.replace(':', ' ')
            filename = filename.replace('%', ' ')
            filename = filename.replace('!', ' ')
            filename = filename.replace('&', 'and')
            filename = filename.replace('.', ' ')
            utils.download_pdf(pdf_path, os.path.join(local_folder, f'{filename}.pdf'))

        # Save metadata to CSV
        metadata_file = os.path.join(local_folder, 'metadata.csv')
        utils.save_metadata_to_csv(df, metadata_file)

        # Print or return the resulting dataframe
        print(df)

        return {
            'statusCode': 200,
            'message': 'Successfully fetched and downloaded papers',
            'dataframe': df.to_dict(orient='records')
        }

    except Exception as e:
        print(e)
        print("Something went wrong. Can't get papers")
        return {
            'statusCode': 404,
            'message': str(e)
        }