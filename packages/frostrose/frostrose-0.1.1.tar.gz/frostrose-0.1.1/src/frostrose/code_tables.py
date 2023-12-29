class CodeTables:
    def __init__(self, frost_client):
        """
        Initializes the CodeTables class with a FrostClient instance.

        :param frost_client: An instance of the FrostClient for making API requests.
        """
        self.frost_client = frost_client

    def get_code_tables(self, format='jsonld'):
        """
        Retrieves code tables data from the frost.met.no API.

        :param format: The format of the response, defaults to 'jsonld'.
        :return: A list or dictionary containing code tables data.
        """
        endpoint = f'elements/codeTables/v0.{format}'
        return self.frost_client._make_request(endpoint)
