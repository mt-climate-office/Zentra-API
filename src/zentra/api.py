"""Bindings to the Zentra API

This module allows users easy access to the Zentra API, as documented at
https://zentracloud.com/api/v1/guide. It only implements the tokenized
API endpoints over their less secure alternatives.

This script requires that `requests` and `pandas` be installed within the Python
environment you are running this script in. All API calls are returned
as python dictionaries with nested pandas dataframes.

This module contains the following functions:

    * get_token - returns the a user access token given a username and password
    * get_station_settings - returns the settings for a given station
    * get_station_status - returns the status for a given station
    * get_station_readings - returns the readings for a given station

"""

from requests import Session, Request
import pandas as pd
from dfply import *
import datetime


class ZentraToken:
    """
    A class used to represent an user's access token

    Attributes
    ----------
    request : Request
        a Request object defining the request made to the Zentra server
    token : str
        a string providing the user's access token

    """

    def __init__(self, username=None, password=None, token=None):
        """
        Gets a user token using a POST request to the Zentra API.

        Parameters
        ----------
        username : str, optional
            The username
        password : str, optional
            The password

        """
        self.request = None
        self.token = None

        if token:
            self.token = token

        if username:
            self.build(username, password)

        if self.request and not self.token:
            self.parse()

    def get(self, username, password):
        """
        Gets a user token using a POST request to the Zentra API.
        Wraps build and parse functions.

        Parameters
        ----------
        username : str
            The username
        password : str
            The password

        """
        self.build(username, password)
        self.parse()

        return self

    def build(self, username, password):
        """
        Builds a POST request to the Zentra API to get a user's token.

        Parameters
        ----------
        username : str
            The username
        password : str
            The password

        """
        self.request = Request('POST',
                               url="https://zentracloud.com/api/v1/tokens",
                               data={'username': username,
                                     'password': password}).prepare()

        return self

    def parse(self):
        """
        Sends a token request to the Zentra API and parses the response.
        """
        # Send the request and get the JSON response
        resp = Session().send(self.request). \
            json()

        # parse the respons
        self.token = resp. \
            get('token')

        return self


class ZentraSettings:
    """
    A class used to represent a station's settings

    Attributes
    ----------
    request : Request
        a Request object defining the request made to the Zentra server
    device_info : dict
        a dictionary providing the device info
    measurement_settings : pd.DataFrame
        a pandas DataFrame providing the measurement settings
    time_settings : pd.DataFrame
        a pandas DataFrame providing the time settings
    locations : pd.DataFrame
        a pandas DataFrame providing the locations
    installation_metadata : dict
        a dictionary providing the installation metadata

    """

    def __init__(self, station=None, token=None, start_time=None, end_time=None):
        """
        Gets a station settings using a GET request to the Zentra API.

        Parameters
        ----------
        station : str
            The serial number of the station
        token : ZentraToken
            The user's access token
        start_time : int, optional
            Return settings with timestamps ≥ start_time. Specify start_time in UTC seconds.
        end_time : int, optional
            Return settings with timestamps <= end_time. Specify end_time in UTC seconds.

        """

        if username:
            self.get(station, token, start_time, end_time)
        else:
            # build an empty ZentraToken
            self.request = None
            self.device_info = None
            self.measurement_settings = None
            self.time_settings = None
            self.locations = None
            self.installation_metadata = None

    def get(self, station, token, start_time=None, end_time=None):
        """
        Gets a station settings using a GET request to the Zentra API.
        Wraps build and parse functions.

        Parameters
        ----------
        station : str
            The serial number of the station
        token : ZentraToken
            The user's access token
        start_time : int, optional
            Return settings with timestamps ≥ start_time. Specify start_time in UTC seconds.
        end_time : int, optional
            Return settings with timestamps <= end_time. Specify end_time in UTC seconds.

        """
        self.build(station, token, start_time, end_time)
        self.parse()

        return self

    def build(self, station, token, start_time=None, end_time=None):
        """
        Gets a station settings using a GET request to the Zentra API.

        Parameters
        ----------
        station : str
            The serial number of the station
        token : ZentraToken
            The user's access token
        start_time : int, optional
            Return settings with timestamps ≥ start_time. Specify start_time in UTC seconds.
        end_time : int, optional
            Return settings with timestamps <= end_time. Specify end_time in UTC seconds.

        """
        self.request = Request('GET',
                               url='https://zentracloud.com/api/v1/settings',
                               headers={'Authorization': "Token " + token.token},
                               params={'sn': station,
                                       'start_time': start_time,
                                       'end_time': end_time}).prepare()

        return self

    def parse(self):
        """
        Sends a token request to the Zentra API and parses the response.
        """
        # Send the request and get the JSON response
        resp = Session().send(self.request). \
            json()

        # parse the response
        self.device_info = resp['device']['device_info']
        self.measurement_settings = pd.DataFrame(resp['device']['measurement_settings'])
        self.time_settings = pd.DataFrame(resp['device']['locations'])
        self.locations = pd.DataFrame(resp['device']['locations'])
        resp['device']['installation_metadata'] = resp['device']['installation_metadata'][0]
        resp['device']['installation_metadata']['sensor_elevations'] = \
            pd.DataFrame(resp['device']['installation_metadata']['sensor_elevations'])
        self.installation_metadata = resp['device']['installation_metadata']

        return self


class ZentraStatus:
    """
    A class used to represent a station's status

    Attributes
    ----------
    request : Request
        a Request object defining the request made to the Zentra server
    device_info : dict
        a dictionary providing the device info
    device_error_counters : dict
        a dictionary providing the device errors
    cellular_statuses : pd.DataFrame
        a pandas DataFrame providing the cellular statuses
    cellular_error_counters : dict
        a dictionary providing the cellular errors

    """

    def __init__(self, station=None, token=None, start_time=None, end_time=None):
        """
        Gets a station status using a GET request to the Zentra API.

        Parameters
        ----------
        station : str
            The serial number of the station
        token : ZentraToken
            The user's access token
        start_time : int, optional
            Return settings with timestamps ≥ start_time. Specify start_time in UTC seconds.
        end_time : int, optional
            Return settings with timestamps <= end_time. Specify end_time in UTC seconds.

        """

        if username:
            self.get(station, token, start_time, end_time)
        else:
            # build an empty ZentraToken
            self.request = None
            self.device_info = None
            self.measurement_settings = None
            self.time_settings = None
            self.locations = None
            self.installation_metadata = None

    def get(self, station, token, start_time=None, end_time=None):
        """
        Gets a station status using a GET request to the Zentra API.
        Wraps build and parse functions.

        Parameters
        ----------
        station : str
            The serial number of the station
        token : ZentraToken
            The user's access token
        start_time : int, optional
            Return settings with timestamps ≥ start_time. Specify start_time in UTC seconds.
        end_time : int, optional
            Return settings with timestamps <= end_time. Specify end_time in UTC seconds.

        """
        self.build(station, token, start_time, end_time)
        self.parse()

        return self

    def build(self, station, token, start_time=None, end_time=None):
        """
        Gets a station status using a GET request to the Zentra API.

        Parameters
        ----------
        station : str
            The serial number of the station
        token : ZentraToken
            The user's access token
        start_time : int, optional
            Return settings with timestamps ≥ start_time. Specify start_time in UTC seconds.
        end_time : int, optional
            Return settings with timestamps <= end_time. Specify end_time in UTC seconds.

        """
        self.request = Request('GET',
                               url='https://zentracloud.com/api/v1/statuses',
                               headers={'Authorization': "Token " + token.token},
                               params={'sn': station,
                                       'start_time': start_time,
                                       'end_time': end_time}).prepare()

        return self

    def parse(self):
        """
        Sends a token request to the Zentra API and parses the response.
        """
        # Send the request and get the JSON response
        resp = Session().send(self.request). \
            json()

        # parse the response
        self.device_info = resp['device']['device_info']
        resp['device']['device_error_counters']['sensor_errors'] = pd.DataFrame(
            resp['device']['device_error_counters']['sensor_errors'])
        self.device_error_counters = resp['device']['device_error_counters']
        self.cellular_statuses = pd.DataFrame(resp['device']['cellular_statuses'])
        self.cellular_error_counters = resp['device']['cellular_error_counters']

        return self


class ZentraReadings:
    """
    A class used to represent a station's readings

    Attributes
    ----------
    request : Request
        a Request object defining the request made to the Zentra server
    device_info : dict
        a dictionary providing the device info
    timeseries : list
        a list of ZentraTimeseriesRecord objects

    """

    def __init__(self, station=None, token=None, start_time=None, start_mrid=None):
        """
        Gets a station readings using a GET request to the Zentra API.

        Parameters
        ----------
        station : str
            The serial number of the station
        token : ZentraToken
            The user's access token
        start_time : int, optional
            Return settings with timestamps ≥ start_time. Specify start_time in UTC seconds.
        start_mrid : int, optional
            Return readings with mrid ≥ start_mrid.

        """

        if token:
            self.get(station, token, start_time, start_mrid)
        else:
            # build an empty ZentraToken
            self.request = None
            self.device_info = None
            self.measurement_settings = None
            self.time_settings = None
            self.locations = None
            self.installation_metadata = None

    def get(self, station, token, start_time=None, start_mrid=None):
        """
        Gets a station readings using a GET request to the Zentra API.
        Wraps build and parse functions.

        Parameters
        ----------
        station : str
            The serial number of the station
        token : ZentraToken
            The user's access token
        start_time : int, optional
            Return settings with timestamps ≥ start_time. Specify start_time in UTC seconds.
        start_mrid : int, optional
            Return readings with mrid ≥ start_mrid.

        """
        self.build(station, token, start_time, start_mrid)
        self.parse()

        return self

    def build(self, station, token, start_time=None, start_mrid=None):
        """
        Gets a station readings using a GET request to the Zentra API.

        Parameters
        ----------
        station : str
            The serial number of the station
        token : ZentraToken
            The user's access token
        start_time : int, optional
            Return settings with timestamps ≥ start_time. Specify start_time in UTC seconds.
        start_mrid : int, optional
            Return readings with mrid ≥ start_mrid.

        """
        self.request = Request('GET',
                               url='https://zentracloud.com/api/v1/readings',
                               headers={'Authorization': "Token " + token.token},
                               params={'sn': station,
                                       'start_time': start_time,
                                       'start_mrid': start_mrid}).prepare()

        return self

    def parse(self):
        """
        Sends a token request to the Zentra API and parses the response.
        """
        # Send the request and get the JSON response
        resp = Session().send(self.request). \
            json()

        # parse the response
        self.device_info = resp['device']['device_info']
        self.timeseries = list(map(lambda x: ZentraTimeseriesRecord(x), resp['device']['timeseries']))

        return self


class ZentraTimeseriesRecord:
    """
    A class used to represent a timeseries record

    Attributes
    ----------
    valid_since : datetime
        The datetime since this record is valid
    sensors : pd.DataFrame
        a pandas DataFrame providing the sensor configuration
    values : pd.DataFrame
        a pandas DataFrame providing the readings

    """

    def __init__(self, configuration):
        """
        Initializes a ZentraTimeseriesRecord object

        Parameters
        ----------
        configuration : dictionary
            A Zentra conficuration record returned as part of a ZentraReadings API call.

        """
        self.valid_since = configuration['configuration']['valid_since']
        self.sensors = pd.DataFrame(configuration['configuration']['sensors'])

        # configuration = resp['device']['timeseries'][0]
        vals = pd.DataFrame(configuration['configuration']['values'])

        for port in range(3, vals.columns.max() + 1):
            vals[port] = \
                vals[port].map(pd.DataFrame)

        vals.columns = \
            (
                    ['datetime', 'mrid', 'unknown'] +
                    list(
                        str(s)
                        for s
                        in list(
                            range(1, vals.columns.max() - 1)
                        )
                    )
            )

        self.values = pd.concat(
            (vals >>
             mutate(datetime=list(map(datetime.datetime.fromtimestamp, vals['datetime'].tolist()))) >>
             gather('port', 'values', columns_from(X['1'])) >>
             arrange(X.datetime, X.port)
             ).apply(lambda x: (x['values'] >>
                                mutate(datetime=x['datetime'],
                                       mrid=x['mrid'],
                                       unknown=x['unknown'],
                                       port=x['port']) >>
                                select(X.datetime, X.mrid, X.unknown, X.port, everything())
                                ),
                     axis=1).tolist()
        )
