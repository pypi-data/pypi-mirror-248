class ClimateNormals:
    def __init__(self, frost_client):
        """
        Initializes the ClimateNormals class with a FrostClient instance.

        :param frost_client: An instance of the FrostClient for making API requests.
        """
        self.frost_client = frost_client

    def get_climate_normals(self, format='jsonld', params=None):
        """
        Retrieves climate normals data from the frost.met.no API.

        :param format: The format of the response, defaults to 'jsonld'.
        :param params: Additional parameters for the API request as a dictionary.
        :return: A list or dictionary containing climate normals data.
        """
        endpoint = f'climatenormals/v0.{format}'
        return self.frost_client._make_request(endpoint, params=params)
