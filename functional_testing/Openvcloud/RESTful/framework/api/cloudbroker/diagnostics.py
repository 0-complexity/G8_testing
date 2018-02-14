from framework.api import api_client, utils

class diagnostics:
    def __init__(self):
        self._api = api_client.cloudbroker.diagnostics

    def checkVms(self):
        return self._api.checkVms()