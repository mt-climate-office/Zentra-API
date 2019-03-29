"""Bindings to the Zentra API

This module allows users easy access to the Zentra API, as documented at
https://zentracloud.com/api/v1/guide. It only implements the tokenized
API endpoints over their less secure alternatives.

This script requires that `requests` and `pandas` be installed within the Python
environment you are running this script in. All API calls are returned
as python dictionaries with nested pandas dataframes.

"""

from requests import Session, Request
import pandas as pd
from dfply import *
import datetime
import json


class ZentraToken:
    """
    A class used to represent an user's access token

    Attributes
    ----------
    request : Request
        a Request object defining the request made to the Zentra server
    response : Response
        a json response from the Zentra server
    token : str
        a string providing the user's access token

    """

    def __init__(self, username=None, password=None, token=None, json_file=None):
        """
        Gets a user token using a POST request to the Zentra API.

        Parameters
        ----------
        username : str, optional
            The username
        password : str, optional
            The password
        json_file : str, optional
            The path to a local json file to parse.

        """
        self.request = None
        self.response = None
        self.token = None

        if token:
            self.token = token

        elif username and password:
            self.get(username, password)

        elif json_file:
            self.response = json.load(open(json_file))
            self.parse()

        if self.request and not self.token:
            self.make_request()
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
        self.make_request()
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

    def make_request(self):
        """
        Sends a token request to the Zentra API and parses the response.
        """
        # Send the request and get the JSON response
        self.response = Session().send(self.request). \
            json()

        return self

    def parse(self):
        """
        Parses the response.
        """
        # parse the respons
        self.token = self.response. \
            get('token')

        return self


class ZentraSettings:
    """
    A class used to represent a device's settings

    Attributes
    ----------
    request : Request
        a Request object defining the request made to the Zentra server
    response : Response
        a json response from the Zentra server
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

    def __init__(self, sn=None, token=None, start_time=None, end_time=None, json_file=None):
        """
        Gets a device settings using a GET request to the Zentra API.

        Parameters
        ----------
        sn : str
            The serial number of the device
        token : ZentraToken
            The user's access token
        start_time : int, optional
            Return settings with timestamps ≥ start_time. Specify start_time in UTC seconds.
        end_time : int, optional
            Return settings with timestamps ≤ end_time. Specify end_time in UTC seconds.
        json_file : str, optional
            The path to a local json file to parse.

        """

        if json_file:
            self.response = json.load(open(json_file))
            self.parse()
        elif sn and token:
            self.get(sn, token, start_time, end_time)
        elif sn or token:
            raise Exception(
                '"sn" and "token" parameters must both be included.')
        else:
            # build an empty ZentraToken
            self.request = None
            self.response = None
            self.device_info = None
            self.measurement_settings = None
            self.time_settings = None
            self.locations = None
            self.installation_metadata = None

    def get(self, sn, token, start_time=None, end_time=None):
        """
        Gets a device settings using a GET request to the Zentra API.
        Wraps build and parse functions.

        Parameters
        ----------
        sn : str
            The serial number of the device
        token : ZentraToken
            The user's access token
        start_time : int, optional
            Return settings with timestamps ≥ start_time. Specify start_time in UTC seconds.
        end_time : int, optional
            Return settings with timestamps ≤ end_time. Specify end_time in UTC seconds.

        """
        self.build(sn, token, start_time, end_time)
        self.make_request()
        self.parse()

        return self

    def build(self, sn, token, start_time=None, end_time=None):
        """
        Gets a device settings using a GET request to the Zentra API.

        Parameters
        ----------
        sn : str
            The serial number of the device
        token : ZentraToken
            The user's access token
        start_time : int, optional
            Return settings with timestamps ≥ start_time. Specify start_time in UTC seconds.
        end_time : int, optional
            Return settings with timestamps ≤ end_time. Specify end_time in UTC seconds.

        """
        self.request = Request('GET',
                               url='https://zentracloud.com/api/v1/settings',
                               headers={
                                   'Authorization': "Token " + token.token},
                               params={'sn': sn,
                                       'start_time': start_time,
                                       'end_time': end_time}).prepare()

        return self

    def make_request(self):
        """
        Sends a token request to the Zentra API and stores the response.
        """
        # Send the request and get the JSON response
        resp = Session().send(self.request)
        if resp.status_code != 200:
            raise Exception(
                'Incorrectly formatted request. Please ensure the user token and device serial number are correct.')

        self.response = resp.json()

        return self

    def parse(self):
        """
        Parses the response.
        """
        # parse the response
        self.device_info = self.response['device']['device_info']
        self.measurement_settings = pd.DataFrame(
            self.response['device']['measurement_settings'])
        self.time_settings = pd.DataFrame(
            self.response['device']['time_settings'])
        self.locations = pd.DataFrame(self.response['device']['locations'])
        self.response['device']['installation_metadata'] = self.response['device']['installation_metadata'][0]
        self.response['device']['installation_metadata']['sensor_elevations'] = \
            pd.DataFrame(self.response['device']['installation_metadata']
                         ['sensor_elevations'])
        self.installation_metadata = self.response['device']['installation_metadata']

        return self


class ZentraStatus:
    """
    A class used to represent a device's status

    Attributes
    ----------
    request : Request
        a Request object defining the request made to the Zentra server
    response : Response
        a json response from the Zentra server
    device_info : dict
        a dictionary providing the device info
    device_error_counters : dict
        a dictionary providing the device errors
    cellular_statuses : pd.DataFrame
        a pandas DataFrame providing the cellular statuses
    cellular_error_counters : dict
        a dictionary providing the cellular errors

    """

    def __init__(self, sn=None, token=None, start_time=None, end_time=None, json_file=None):
        """
        Gets a device status using a GET request to the Zentra API.

        Parameters
        ----------
        sn : str
            The serial number of the device
        token : ZentraToken
            The user's access token
        start_time : int, optional
            Return status with timestamps ≥ start_time. Specify start_time in UTC seconds.
        end_time : int, optional
            Return status with timestamps ≤ end_time. Specify end_time in UTC seconds.
        json_file : str, optional
            The path to a local json file to parse.

        """

        if json_file:
            self.response = json.load(open(json_file))
            self.parse()
        elif sn and token:
            self.get(sn, token, start_time, end_time)
        elif sn or token:
            raise Exception(
                '"sn" and "token" parameters must both be included.')
        else:
            # build an empty ZentraToken
            self.request = None
            self.response = None
            self.device_info = None
            self.measurement_settings = None
            self.time_settings = None
            self.locations = None
            self.installation_metadata = None

    def get(self, sn, token, start_time=None, end_time=None):
        """
        Gets a device status using a GET request to the Zentra API.
        Wraps build and parse functions.

        Parameters
        ----------
        sn : str
            The serial number of the device
        token : ZentraToken
            The user's access token
        start_time : int, optional
            Return status with timestamps ≥ start_time. Specify start_time in UTC seconds.
        end_time : int, optional
            Return status with timestamps ≤ end_time. Specify end_time in UTC seconds.

        """
        self.build(sn, token, start_time, end_time)
        self.make_request()
        self.parse()

        return self

    def build(self, sn, token, start_time=None, end_time=None):
        """
        Gets a device status using a GET request to the Zentra API.

        Parameters
        ----------
        sn : str
            The serial number of the device
        token : ZentraToken
            The user's access token
        start_time : int, optional
            Return status with timestamps ≥ start_time. Specify start_time in UTC seconds.
        end_time : int, optional
            Return status with timestamps ≤ end_time. Specify end_time in UTC seconds.

        """
        self.request = Request('GET',
                               url='https://zentracloud.com/api/v1/statuses',
                               headers={
                                   'Authorization': "Token " + token.token},
                               params={'sn': sn,
                                       'start_time': start_time,
                                       'end_time': end_time}).prepare()

        return self

    def make_request(self):
        """
        Sends a token request to the Zentra API and stores the response.
        """
        # Send the request and get the JSON response
        resp = Session().send(self.request)
        if resp.status_code != 200:
            raise Exception(
                'Incorrectly formatted request. Please ensure the user token and device serial number are correct.')

        self.response = resp.json()

        return self

    def parse(self):
        """
        Parses the response.
        """
        self.device_info = self.response['device']['device_info']
        self.response['device']['device_error_counters']['sensor_errors'] = pd.DataFrame(
            self.response['device']['device_error_counters']['sensor_errors'])
        self.device_error_counters = self.response['device']['device_error_counters']
        self.cellular_statuses = pd.DataFrame(
            self.response['device']['cellular_statuses'])
        self.cellular_error_counters = self.response['device']['cellular_error_counters']

        return self


class ZentraReadings:
    """
    A class used to represent a device's readings

    Attributes
    ----------
    request : Request
        a Request object defining the request made to the Zentra server
    response : Response
        a json response from the Zentra server
    device_info : dict
        a dictionary providing the device info
    timeseries : list
        a list of ZentraTimeseriesRecord objects

    """

    def __init__(self, sn=None, token=None, start_time=None, end_time=None, start_mrid=None, end_mrid=None,
                 json_file=None):
        """
        Gets a device readings using a GET request to the Zentra API.

        Parameters
        ----------
        sn : str
            The serial number of the device
        token : ZentraToken
            The user's access token
        start_time : int, optional
            Return readings with timestamps ≥ start_time. Specify start_time in UTC seconds.
        end_time : int, optional
            Return readings with timestamps ≤ end_time. Specify end_time in UTC seconds.
        start_mrid : int, optional
            Return readings with mrid ≥ start_mrid.
        end_mrid : int, optional
            Return readings with mrid ≤ start_mrid.
        json_file : str, optional
            The path to a local json file to parse.

        """
        if json_file:
            self.response = json.load(open(json_file))
            self.parse()
        elif sn and token:
            self.get(sn, token, start_time, end_time, start_mrid, end_mrid)
        elif sn or token:
            raise Exception(
                '"sn" and "token" parameters must both be included.')
        else:
            # build an empty ZentraToken
            self.request = None
            self.response = None
            self.device_info = None
            self.measurement_settings = None
            self.time_settings = None
            self.locations = None
            self.installation_metadata = None

    def get(self, sn, token, start_time=None, end_time=None, start_mrid=None, end_mrid=None):
        """
        Gets a device readings using a GET request to the Zentra API.
        Wraps build and parse functions.

        Parameters
        ----------
        sn : str
            The serial number of the device
        token : ZentraToken
            The user's access token
        start_time : int, optional
            Return readings with timestamps ≥ start_time. Specify start_time in UTC seconds.
        end_time : int, optional
            Return readings with timestamps ≤ end_time. Specify end_time in UTC seconds.
        start_mrid : int, optional
            Return readings with mrid ≥ start_mrid.
        end_mrid : int, optional
            Return readings with mrid ≤ start_mrid.

        """
        self.build(sn, token, start_time, end_time, start_mrid, end_mrid)
        self.make_request()
        self.parse()

        return self

    def build(self, sn, token, start_time=None, end_time=None, start_mrid=None, end_mrid=None):
        """
        Gets a device readings using a GET request to the Zentra API.

        Parameters
        ----------
        sn : str
            The serial number of the device
        token : ZentraToken
            The user's access token
        start_time : int, optional
            Return readings with timestamps ≥ start_time. Specify start_time in UTC seconds.
        end_time : int, optional
            Return readings with timestamps ≤ end_time. Specify end_time in UTC seconds.
        start_mrid : int, optional
            Return readings with mrid ≥ start_mrid.
        end_mrid : int, optional
            Return readings with mrid ≤ start_mrid.

        """
        self.request = Request('GET',
                               url='https://zentracloud.com/api/v1/readings',
                               headers={
                                   'Authorization': "Token " + token.token},
                               params={'sn': sn,
                                       'start_time': start_time,
                                       'end_time': end_time,
                                       'start_mrid': start_mrid,
                                       'end_mrid': end_mrid}).prepare()

        return self

    def make_request(self):
        """
        Sends a token request to the Zentra API and stores the response.
        """
        # Send the request and get the JSON response
        resp = Session().send(self.request)
        if resp.status_code != 200:
            raise Exception(
                'Incorrectly formatted request. Please ensure the user token and device serial number are correct.')
        elif str(resp.content) == str(b'{"Error": "Device serial number entered does not exitst"}'):
            raise Exception(
                'Error: Device serial number entered does not exist')

        self.response = resp.json()

        return self

    def parse(self):
        """
        Parses the response.
        """
        self.device_info = self.response['device']['device_info']
        self.timeseries = list(
            map(lambda x: ZentraTimeseriesRecord(x), self.response['device']['timeseries']))

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
            A Zentra configuration record returned as part of a ZentraReadings API call.

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
                ['datetime', 'mrid', 'rssi'] +
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
             mutate(datetime=[datetime.datetime.fromtimestamp(x, datetime.timezone.utc) for x in
                              vals['datetime'].tolist()]) >>
             gather('port', 'values', columns_from(X['1'])) >>
             arrange(X.datetime, X.port)
             ).apply(lambda x: (x['values'] >>
                                mutate(datetime=x['datetime'],
                                       mrid=x['mrid'],
                                       rssi=x['rssi'],
                                       port=x['port']) >>
                                select(X.datetime,
                                       X.mrid,
                                       X.rssi,
                                       X.port,
                                       everything())
                                ),
                     axis=1).tolist()
        )
