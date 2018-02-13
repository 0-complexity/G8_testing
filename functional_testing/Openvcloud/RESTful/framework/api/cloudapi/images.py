from framework.api import api_client

class Images:
    def __init__(self):
        self._api = api_client

    def list(self, **kwargs):
        return self._api.cloudapi.images.list(**kwargs)

    def delete(self, imageId):
        return self._api.cloudapi.images.delete(imageId=imageId)