import requests
import json

class Connector:
    def __init__(self, dome_url, api_key, provider_id):
        self.dome_url = dome_url
        self.api_key = api_key
        self.provider_id = provider_id

    def get_data(self, search_string):

        res_conn_query = requests.get(
            f"{self.dome_url}api/discover/results/{self.provider_id}",
            headers={'apikey': self.api_key},
            params={'search_string': search_string},
            timeout=10,
        )

        try:
            return res_conn_query.json()
        except:
            return res_conn_query.content

if __name__ == "__main__":
    API_KEY = "246a7efb25.1880f832921c4f879e9b87fe744b2dec"
    connector = Connector("https://nextgen.dome40.io/", API_KEY, "CHEMEO")
    result = connector.get_data("Carbon monoxide")
    print(json.dumps(result,indent=4))