from framework.api import api_client
from framework.utils.utils import Utils

class Images:
    def __init__(self):
        self._api = api_client.cloudapi.images
        self.utils = Utils()

    def list(self, **kwargs):
        return self._api.list(**kwargs)

    def delete(self, imageId):
        return self._api.delete(imageId=imageId)