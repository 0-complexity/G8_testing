import random
from framework.api import api_client, utils

class diagnostics:
    def __init__(self):
        self._api = api_client

    def checkVms(self):
        return self._api.cloudbroker.diagnostics.checkVms()