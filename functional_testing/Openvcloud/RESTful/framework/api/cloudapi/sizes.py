from framework.api import api_client, utils

class Sizes:
    def __init__(self):
        self._api = api_client

    def list(self, ** kwargs):
        return self._api.cloudapi.sizes.list(** kwargs)
