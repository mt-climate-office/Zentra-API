# Zentra API
The `zentra` library provides python bindings to the Zentra Cloud RESTful API. [Read the docs here.](https://mt-climate-office.github.io/Zentra-API/)

## What is Zentra Cloud?
[Zentra Cloud](https://www.metergroup.com/environment/zentra-cloud/) is a service of the [METER Group](https://www.metergroup.com/) for delivering data collected by METER data-loggers. The service allows logger owners to invite users to view and download their data. Zentra Cloud provides a graphical user interface as well as a [RESTful](https://en.wikipedia.org/wiki/Representational_state_transfer) application programming interface (API). Authenticated users can access data through either interface.

## Installation
The `zentra` library is not yet available on PyPI. Until then, install directly from Github using `pip`:

```bash
pip install git+https://github.com/mt-climate-office/Zentra-API
```

## Usage
The `zentra` library is designed to conform as closely as possible to the Zentra Cloud REST API, while returning data in useful [pandas](https://pandas.pydata.org/) data structures. For security reasons, `zentra` enforces the use of personal access tokens as opposed to station-level passwords. It assumes that a user already has an account and password set up with Zentra Cloud. Please refer to the [Zentra Cloud API documentation](https://zentracloud.com/api/v1/guide) for API call and parameter details.

The `zentra` library defines four primary classes:

- `ZentraToken` holds methods and data relating to authentication into the Zentra Cloud API.
- `ZentraSettings` holds methods and data relating to logger settings.
- `ZentraStatus` holds methods and data relating to logger status.
- `ZentraReadings` holds methods and data relating to logger readings.

Each class has methods to `build` an API request, send a request and `parse` it, `get` the data (which wraps the `build` and `parse` steps), and an initialization method that if passed adequate information also builds the request, requests the data, and parses it.
Methods for `ZentraSettings`, `ZentraStatus`, and `ZentraReadings` classes all require a parsed `ZentraToken` object in order to request data from the Zentra Cloud.

### Loading the library
After installation, load the `zentra` library with a standard import call to the `api` module:

```python
import zentra.api
```

### `ZentraToken`
The `ZentraToken` class holds methods and data relating to authentication into the Zentra Cloud API.
The classes initialization, `build`, and `get` methods accept two parameters:

- `username`: your Zentra Cloud username
- `password`: your Zentra Cloud password

Create a `ZentraToken` by initializing with a username and password:

```python
token = ZentraToken(username="[USERNAME]",
                    password="[PASSWORD]")

# access the token by calling the 'token' attribute
token.token
```

You are **strongly** encouraged not to hard-code your credentials into a python script, or to enter them in the terminal.
One way to avoid this is to save them as environment variables, and call them using the

```python
from os import getenv

token = ZentraToken(username=getenv("zentra_un"),
                    password=getenv("zentra_pw"))

token.token
```

Alternatively, you can `build` then `parse` the token:

```python
from os import getenv

token = ZentraToken().build(username=getenv("zentra_un"),
                            password=getenv("zentra_pw")).parse()

token.token
```

Or, if you already have a valid token stored locally, you can create a `ZentraToken` object without a username or password:

```python
from os import getenv

token = ZentraToken(token=getenv("zentra_token"))

token.token
```

### `ZentraSettings`, `ZentraStatus`, `ZentraReadings`
The `ZentraSettings`, `ZentraStatus`, `ZentraReadings` each require authentication with a `ZentraToken`, and all return information about or from a particular METER device given that device's unique serial number. Like `ZentraToken`, the classes each have `build`, `parse`, and `get` methods. Parameters include:

- `token` (required): a parsed `ZentraToken` object
- `sn` (required): the serial number for the device
- `start_time` (optional): Return data with timestamps ≥ start_time. Specify start_time in UTC seconds.
- `end_time` (optional; `ZentraSettings` and `ZentraStatus` only): Return data with timestamps <= end_time. Specify end_time in UTC seconds.
- `start_mrid` (optional; `ZentraReadings` only): Return readings with mrid ≥ start_mrid.

The `ZentraReadings` records are stored as a list of objects of class `ZentraTimeseriesRecord`, which stores data on the sensors that reported and their records.

After defining a valid `ZentraToken`, retrieve settings, status, and readings data like this, for example:

```python
from zentra.api import *
from os import getenv

token = ZentraToken(username=getenv("zentra_un"),
                    password=getenv("zentra_pw"))

# Get the settings for a device
settings = ZentraSettings(sn="06-00187",
                          token=token)
# Report the measurement settings
settings.measurement_settings

# Get the status messages for a device
status = ZentraStatus(sn="06-00187",
                      token=token)
# Report the cellular statuses
status.cellular_statuses

# Get the readings for a device
readings = ZentraReadings(sn="06-00761",
                          token=token,
                          start_time=int(datetime.datetime(year=2019,
                                                           month=7,
                                                           day=4).timestamp()))
# Report the readings from the first ZentraTimeseriesRecord
readings.timeseries[0].values

```

## Development
This project has been set up using PyScaffold 3.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.

First, clone this project and change into the project directory:

``` bash
git clone https://github.com/mt-climate-office/Zentra-API
cd Zentra-API
```

Then, to install the library and its dependencies into your current python environment, run:

```bash
python setup.py develop
```

### Testing
This project uses [pytest](https://docs.pytest.org/en/latest/) for testing and coverage analysis.
To test, from the project directory run:

```bash
python setup.py test
```

### Documentation
This project uses [`pdoc`](https://github.com/mitmproxy/pdoc) to auto-generate documentation from docstrings in the code. Documentation was generated using this command in the terminal:
```bash
pdoc --html --html-dir docs --overwrite ./src/zentra/api.py
mv -i docs/api.m.html docs/index.html
```
