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


token = ZentraToken(username=getenv("zentra_un"),
                    password=getenv("zentra_pw"))
