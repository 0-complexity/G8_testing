from framework.api import api_client

class Images:
    def __init__(self):
        self._api = api_client.cloudapi.images

    def list(self, **kwargs):
        return self._api.list(**kwargs)

    def delete(self, imageId):
        return self._api.delete(imageId=imageId)