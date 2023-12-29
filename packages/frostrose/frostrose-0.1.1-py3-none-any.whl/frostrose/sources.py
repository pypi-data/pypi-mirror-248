import math

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great-circle distance between two points 
    on the Earth (specified in decimal degrees).

    :param lon1: Longitude of the first point.
    :param lat1: Latitude of the first point.
    :param lon2: Longitude of the second point.
    :param lat2: Latitude of the second point.
    :return: Distance in kilometers.
    """
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of Earth in kilometers
    return c * r


class Sources:
    def __init__(self, frost_client):
        """
        Initializes the Sources class with a FrostClient instance.
        """
        self.frost_client = frost_client
        self.all_sources = None

    def fetch_all_sources(self, format='jsonld',  params=None):
        """
        Retrieves and stores all sources data from the frost.met.no API.
        :param format: The format of the response, defaults to 'jsonld'.
        :param params: Additional parameters for the API request as a dictionary.
        """
        endpoint = f'sources/v0.{format}'
        response = self.frost_client._make_request(endpoint, params=params)
        self.all_sources = response.get('data', [])

    def _ensure_sources_fetched(self):
        """
        Ensures that the sources data is fetched. If not, fetches the data.
        """
        if self.all_sources is None:
            self.fetch_all_sources()

    def get_sources_within_radius_of_lonlat(self, lon, lat, radius_km):
        """
        Finds sources within a certain radius of a given longitude and latitude.
        """
        self._ensure_sources_fetched()
        nearby_sources = []
        for source in self.all_sources:
            try:
                source_coords = source['geometry']['coordinates']
                distance = haversine(lon, lat, source_coords[0], source_coords[1])
                if distance <= radius_km:
                    nearby_sources.append(source)
            except KeyError:
                pass
        return nearby_sources

    def get_sources_within_radius_of_source_id(self, source_id, radius_km):
        """
        Finds sources within a certain radius of a given source ID.
        """
        self._ensure_sources_fetched()
        primary_source = next((s for s in self.all_sources if s['id'] == source_id), None)
        if not primary_source:
            return []

        primary_coords = primary_source['geometry']['coordinates']
        return self.get_sources_within_radius_of_lonlat(primary_coords[0], primary_coords[1], radius_km)

    def get_sources_with_name_icontains(self, name_substr):
        """
        Finds sources where the name contains the given substring (case-insensitive).
        """
        self._ensure_sources_fetched()
        return [s for s in self.all_sources if name_substr.lower() in s.get("name","").lower()]
