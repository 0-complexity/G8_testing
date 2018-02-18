import random
from framework.api import api_client, utils

class Health:
    def __init__(self):
        self._api = api_client

    def status(self):
        return self._api.cloudbroker.health.status()