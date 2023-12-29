class Elements:
    def __init__(self, frost_client):
        """
        Initializes the Elements class with a FrostClient instance.
        """
        self.frost_client = frost_client
        self.all_elements = None

    def fetch_all_elements(self, format='jsonld'):
        """
        Retrieves and stores all elements data from the frost.met.no API.
        """
        endpoint = f'elements/v0.{format}'
        response = self.frost_client._make_request(endpoint)
        self.all_elements = response.get('data', [])

    def _ensure_elements_fetched(self):
        """
        Ensures that the elements data is fetched. If not, fetches the data.
        """
        if self.all_elements is None:
            self.fetch_all_elements()

    def get_elements_name_icontains(self, name_substr):
        """
        Finds elements where the name contains the given substring (case-insensitive).
        """
        self._ensure_elements_fetched()
        return [element for element in self.all_elements if name_substr.lower() in element.get('name','').lower()]

