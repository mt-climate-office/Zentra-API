from os import getenv
from zentra.api import *

request = ZentraToken().build(username=getenv("zentra_un"),
                              password=getenv("zentra_pw"))

print(request.request)

print(Session().send(request.request))
