from framework.api import api_client

class Sizes:
    def __init__(self):
        self._api = api_client.cloudapi.sizes

    def list(** kwargs):
        return self._api.list(** kwargs)
