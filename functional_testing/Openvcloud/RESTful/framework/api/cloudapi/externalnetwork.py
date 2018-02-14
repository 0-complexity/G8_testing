from framework.api import api_client, utils

class ExternalNetwork:
    def __init__(self):
        self._api = api_client

    def list(self, accountId):
        return self._api.cloudapi.externalnetwork.list(accountId=accountId)