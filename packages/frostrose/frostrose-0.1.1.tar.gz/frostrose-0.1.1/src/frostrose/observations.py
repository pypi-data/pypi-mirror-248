from datetime import datetime

class ObservationTimeSeries:
    def __init__(self, raw_data):
        """
        Initializes the ObservationTimeSeries with raw observation data.

        :param raw_data: The raw data returned from fetch_observations.
        """
        self.raw_data = raw_data

    def to_flat_dict_list(self):
        """
        Transforms the raw data into a list of flat dictionaries, where each dictionary 
        represents a single observation, with the timestamp parsed as a datetime object.

        :return: A list of flat dictionaries.
        """
        flat_data = []
        for record in self.raw_data.get('data', []):
            reference_time = datetime.fromisoformat(record['referenceTime'].replace('Z', '+00:00'))
            for observation in record.get('observations', []):
                flat_data.append({
                    'referenceTime': reference_time,
                    observation['elementId']: observation['value']
                })
        return flat_data




class Observations:
    def __init__(self, frost_client):
        """
        Initializes the Observations class with a FrostClient instance.
        """
        self.frost_client = frost_client

    def get_available_timeseries(self, params):
        """
        Finds available timeseries based on provided parameters.
        """
        endpoint = 'observations/availableTimeSeries/v0.jsonld'
        return self.frost_client._make_request(endpoint, params=params)

    def get_observations_for_element(self, element, referencetime='2017-01-01'):
        """
        Retrieves observations for a specific element.
        """
        params = {'elements': element, 'referencetime': referencetime}
        return self.get_available_timeseries(params)

    def get_data_for_station(self, station_id, referencetime='2017-01-01'):
        """
        Retrieves data available for a specific station.
        """
        params = {'sources': station_id, 'referencetime': referencetime}
        return self.get_available_timeseries(params)

    def get_stations_with_performance_category(self, category, referencetime='2017-01-01'):
        """
        Finds stations with a specific performance category.
        """
        params = {'performancecategory': category, 'referencetime': referencetime}
        return self.get_available_timeseries(params)

    def get_historical_data_availability(self, element, start_date, end_date):
        """
        Checks data availability for a specific period and element.
        """
        referencetime = f'{start_date}/{end_date}'
        params = {'elements': element, 'referencetime': referencetime}
        return self.get_available_timeseries(params)

    def fetch_observations(self, params):
        """
        Fetches observation data based on provided parameters.
        """
        endpoint = 'observations/v0.jsonld'
        return self.frost_client._make_request(endpoint, params=params)
    
    def get_data_for_source_element_for_period(self, source_id, element, date_start, date_end=None):
        """
        Retrieves observation data for a specific source, element, and time period.

        :param source_id: The ID of the source.
        :param element: The element to retrieve data for.
        :param date_start: The start date of the period (YYYY-MM-DD format).
        :param date_end: The end date of the period (YYYY-MM-DD format). Defaults to current date if not provided.
        :return: Observation data for the specified criteria.
        """
        if date_end is None:
            date_end = datetime.now().strftime('%Y-%m-%d')

        referencetime = f'{date_start}/{date_end}'
        params = {
            'sources': source_id,
            'elements': element,
            'referencetime': referencetime
        }
        return ObservationTimeSeries(self.fetch_observations(params))
