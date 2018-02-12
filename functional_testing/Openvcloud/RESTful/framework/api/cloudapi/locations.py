from framework.api import api_client
from framework.utils.utils import Utils

class Locations:
    def __init__(self):
        self._api = api_client.cloudapi.locations
        self.utils = Utils()

    def list():
        return self._api.list()

    def getUrl(self):
        return self._api.getUrl()