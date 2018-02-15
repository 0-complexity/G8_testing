import random
from framework.api import api_client, utils

class OVSNode:
    def __init__(self):
        self._api = api_client

    def activateNodes(self, nids):
        return self._api.cloudbroker.ovsnode.activateNodes(nids=nids)

    def deactivateNodes(self, nids):
        return self._api.cloudbroker.ovsnode.deactivateNodes(nids=nids)
        

