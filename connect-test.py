from os import getenv
from zentra.api import *

print(Session().send(ZentraToken().build(username=getenv("zentra_un"),
                                         password=getenv("zentra_pw")).request))
