from framework.api import api_client, utils

class health:
    def __init__(self):
        self._api = api_client.cloudbroker.health

    def status(self):
        return self._api.status()