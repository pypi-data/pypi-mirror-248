import os
import requests

class FrostClient:
    def __init__(self, client_id=None, base_url='https://frost.met.no'):
        """
        Initializes the FrostClient with the given client ID and base URL.

        If the client ID is not provided, the constructor tries to fetch it from 
        the FROST_CLIENT_ID environment variable.

        :param client_id: The client ID for authenticating with the frost.met.no API.
                         If None, attempts to fetch from FROST_CLIENT_ID env variable.
        :param base_url: The base URL for the frost.met.no API. Defaults to 'https://frost.met.no'.
        """
        if client_id is None:
            client_id = os.environ.get('FROST_CLIENT_ID')
            if client_id is None:
                raise ValueError("Client ID is not provided and not found in FROST_CLIENT_ID environment variable.")

        self.client_id = client_id
        self.base_url = base_url
        self.session = requests.Session()
        self.session.auth = (client_id, '')

    def _make_request(self, endpoint, params=None):
        """
        Makes a GET request to the specified endpoint with the given parameters.

        :param endpoint: The API endpoint to make the request to.
        :param params: The parameters to pass to the API request.
        :return: The response from the API as a JSON object.
        """
        url = f"{self.base_url}/{endpoint}"
        response = self.session.get(url, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API request failed with status code {response.status_code}: {response.text}")

