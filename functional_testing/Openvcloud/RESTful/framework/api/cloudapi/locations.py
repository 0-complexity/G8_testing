from framework.api import api_client

class Locations:
    def __init__(self):
        self._api = api_client

    def list():
        return self._api.cloudapi.locations.list()

    def getUrl(self):
        return self._api.cloudapi.locations.getUrl()