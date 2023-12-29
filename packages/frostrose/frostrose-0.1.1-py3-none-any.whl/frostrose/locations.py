class Locations:
    def __init__(self, frost_client):
        """
        Initializes the Locations class with a FrostClient instance.

        :param frost_client: An instance of the FrostClient for making API requests.
        """
        self.frost_client = frost_client

    def get_locations(self, names=None, geometry=None, fields=None):
        """
        Retrieves location metadata from the frost.met.no API.

        :param names: Comma-separated list of location names to filter the results.
        :param geometry: Geometry filter in WKT format.
        :param fields: Comma-separated list of fields to include in the response.
        :return: A list of location metadata.
        """
        endpoint = 'locations/v0.jsonld'
        params = {}
        if names:
            params['names'] = names
        if geometry:
            params['geometry'] = geometry
        if fields:
            params['fields'] = fields

        return self.frost_client._make_request(endpoint, params=params)
