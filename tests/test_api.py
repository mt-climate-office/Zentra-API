import pytest
from os import getenv
from zentra.api import *
from datetime import datetime, timedelta


def test_token_empty():
    assert ZentraToken().token is None


def test_token_unpw():
    assert ZentraToken(username=getenv("zentra_un"),
                       password=getenv("zentra_pw")).token == getenv("zentra_token")


def test_token_token():
    assert ZentraToken(token=getenv("zentra_token")
                       ).token == getenv("zentra_token")


def test_token_build():
    assert ZentraToken().build(username=getenv("zentra_un"),
                               password=getenv("zentra_pw")).request is not None


def test_token_request():
    assert Session().send(ZentraToken().build(username=getenv("zentra_un"),
                                              password=getenv("zentra_pw")).request).status_code == 200


def test_token_parse():
    assert ZentraToken().build(username=getenv("zentra_un"),
                               password=getenv("zentra_pw")).make_request().parse().token == getenv("zentra_token")


def test_token_get():
    assert ZentraToken().get(username=getenv("zentra_un"),
                             password=getenv("zentra_pw")).token == getenv("zentra_token")


token = ZentraToken(username=getenv("zentra_un"),
                    password=getenv("zentra_pw"))


def test_settings_empty():
    assert ZentraSettings().request is None


def test_settings_token_only():
    with pytest.raises(Exception):
        ZentraSettings(token=token)


def test_settings_missing_sn():
    with pytest.raises(Exception):
        ZentraSettings(token=token, sn="06-12345")


def test_settings_correct_init():
    assert ZentraSettings(
        token=token, sn="06-00187").device_info is not None


def test_settings_build():
    assert ZentraSettings().build(token=token,
                                  sn="06-00187").request is not None


def test_settings_request():
    assert Session().send(ZentraSettings().build(token=token,
                                                 sn="06-00187").request).status_code == 200


def test_settings_parse():
    assert ZentraSettings().build(token=token,
                                  sn="06-00187").make_request().parse().device_info['device_sn'] == "06-00187"


def test_settings_get():
    assert ZentraSettings().get(token=token,
                                sn="06-00187").device_info['device_sn'] == "06-00187"


def test_status_empty():
    assert ZentraStatus().request is None


def test_status_token_only():
    with pytest.raises(Exception):
        ZentraStatus(token=token)


def test_status_missing_sn():
    with pytest.raises(Exception):
        ZentraStatus(token=token,
                     sn="06-12345")


def test_status_correct_init():
    assert ZentraStatus(token=token,
                        sn="06-00187").device_info is not None


def test_status_build():
    assert ZentraStatus().build(token=token,
                                sn="06-00187").request is not None


def test_status_request():
    assert Session().send(ZentraStatus().build(token=token,
                                               sn="06-00187").request).status_code == 200


def test_status_parse():
    assert ZentraStatus().build(token=token,
                                sn="06-00187").make_request().parse().device_info['device_sn'] == "06-00187"


def test_status_get():
    assert ZentraStatus().get(token=token,
                              sn="06-00187").device_info['device_sn'] == "06-00187"


def test_readings_empty():
    assert ZentraReadings().request is None


def test_readings_token_only():
    with pytest.raises(Exception):
        ZentraReadings(token=token)


def test_readings_missing_sn():
    with pytest.raises(Exception):
        ZentraReadings(token=token,
                       sn="06-12345",
                       start_time=yesterday)


def test_readings_wrong_token():
    with pytest.raises(Exception):
        ZentraReadings(token=ZentraToken(token="blah"),
                       sn="06-00187",
                       start_time=yesterday)


yesterday = int((datetime.today() - timedelta(1)).timestamp())


def test_readings_correct_init():
    assert ZentraReadings(token=token,
                          sn="06-00187",
                          start_time=yesterday).device_info is not None


def test_readings_build():
    assert ZentraReadings().build(token=token,
                                  sn="06-00187",
                                  start_time=yesterday).request is not None


def test_readings_request():
    assert Session().send(ZentraReadings().build(token=token,
                                                 sn="06-00187",
                                                 start_time=yesterday).request).status_code == 200


def test_readings_parse():
    assert ZentraReadings().build(token=token,
                                  sn="06-00187",
                                  start_time=yesterday).make_request().parse().device_info['device_sn'] == "06-00187"


def test_readings_get():
    assert ZentraReadings().get(token=token,
                                sn="06-00187",
                                start_time=yesterday).device_info['device_sn'] == "06-00187"


def test_readings_get_mrid_range():
    assert ZentraReadings().get(token=token,
                                sn="06-00761",
                                start_mrid=28350,
                                end_mrid=28350).device_info['device_sn'] == "06-00761"


def test_init_timeseries_record():
    assert str(type(ZentraTimeseriesRecord(Session().
                                           send(ZentraReadings().
                                                build(token=token,
                                                      sn="06-00187",
                                                      start_time=yesterday).
                                                request).
                                           json()['device']['timeseries'][0]).
                    values)) == "<class 'pandas.core.frame.DataFrame'>"
