from framework.api import api_client
from framework.utils.utils import Utils

class ExternalNetwork:
    def __init__(self):
        self._api = api_client.cloudapi.externalnetwork
        self.utils = Utils()

    def list(self, accountId):
        return self._api.list(accountId=accountId)