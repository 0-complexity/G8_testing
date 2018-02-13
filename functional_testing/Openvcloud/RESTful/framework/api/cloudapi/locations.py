from framework.api import api_client

class Locations:
    def __init__(self):
        self._api = api_client.cloudapi.locations

    def list():
        return self._api.list()

    def getUrl(self):
        return self._api.getUrl()