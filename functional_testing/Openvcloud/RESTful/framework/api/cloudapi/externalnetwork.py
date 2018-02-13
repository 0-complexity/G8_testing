from framework.api import api_client

class ExternalNetwork:
    def __init__(self):
        self._api = api_client.cloudapi.externalnetwork

    def list(self, accountId):
        return self._api.list(accountId=accountId)