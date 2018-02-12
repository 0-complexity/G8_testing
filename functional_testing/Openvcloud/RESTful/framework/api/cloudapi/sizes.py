from framework.api import api_client
from framework.utils.utils import Utils

class Sizes:
    def __init__(self):
        self._api = api_client.cloudapi.sizes
        self.utils = Utils()

    def list(** kwargs):
        return self._api.list(** kwargs)
