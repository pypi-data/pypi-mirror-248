# Frostrose

`frostrose` is a Python library for easy access to the Norwegian Meteorological Institute's frost.met.no API. It simplifies the process of fetching weather data from various endpoints.

## Installation

```bash
pip install frostrose
```

## Usage

### Setting up the Client

You can use the `FrostClient` either by setting an environment variable `FROST_CLIENT_ID` or by providing the client ID directly during instantiation.

#### Using an Environment Variable

Set the environment variable `FROST_CLIENT_ID` with your API key:

```bash
export FROST_CLIENT_ID='your_api_key_here'
```

Then, in your Python code:

```python
from frostrose import FrostClient

client = FrostClient()
```

#### Providing Client ID on Instantiation

Alternatively, you can provide the client ID directly:

```python
from frostrose import FrostClient

client = FrostClient('your_api_key_here')
```

### Working with Sources (Weather Stations)

Weather stations are referred to as "sources" in the frost.met.no API. `frostrose` provides methods to find sources by name, near a specific longitude and latitude, or near another source.

#### Finding Sources by Name

```python
from frostrose import Sources

sources = Sources(client)
sources.fetch_all_sources()
tynset_sources = sources.get_sources_with_name_icontains('tynset')
```

#### Finding Sources Near a Specific Location

```python
nearby_sources = sources.get_sources_within_radius_of_lonlat(lon=5.1963, lat=59.2555, radius_km=50)
```

#### Finding Sources Near Another Source

```python
nearby_sources_of_id = sources.get_sources_within_radius_of_source_id('SN47230', radius_km=50)
```

### Finding Weather Elements

To find available weather elements:

```python
from frostrose import Elements

elements = Elements(client)
elements_data = elements.get_elements()
```

### Getting Observation Time Series

To get an observation time series for a specific weather element:

```python
from frostrose import Observations

observations = Observations(client)
temperature = observations.get_data_for_source_element_for_period('SN9580', 'air_temperature', date_start='2023-01-01')
```

### Converting to Pandas DataFrame

To convert the observation time series into a pandas DataFrame:

```python
import pandas as pd

flat_data = temperature.to_flat_dict_list()
df = pd.DataFrame.from_records(flat_data)
```

## License

Frostrose is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
