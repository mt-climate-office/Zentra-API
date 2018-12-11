import pytest
from os import getenv
from zentra.api import *


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
                               password=getenv("zentra_pw")).parse().token == getenv("zentra_token")


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


def test_settings_missing_station():
    with pytest.raises(Exception):
        ZentraSettings(token=token, station="06-12345")


def test_settings_correct_init():
    assert ZentraSettings(
        token=token, station="06-00187").device_info is not None


def test_settings_build():
    assert ZentraSettings().build(token=token,
                                  station="06-00187").request is not None


def test_settings_request():
    assert Session().send(ZentraSettings().build(token=token,
                                                 station="06-00187").request).status_code == 200


def test_settings_parse():
    assert ZentraSettings().build(token=token,
                                  station="06-00187").parse().device_info['device_sn'] == "06-00187"


def test_settings_get():
    assert ZentraSettings().get(token=token,
                                station="06-00187").device_info['device_sn'] == "06-00187"
