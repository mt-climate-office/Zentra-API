from os import getenv
from zentra.api import *
import requests

request = ZentraToken().build(username=getenv("zentra_un"),
                              password=getenv("zentra_pw"))

print(request.request)

print(Session().send(request.request).content)

print(requests.get('https://api.github.com/events'))
