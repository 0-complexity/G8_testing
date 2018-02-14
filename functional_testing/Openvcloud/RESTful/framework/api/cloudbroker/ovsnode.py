from framework.api import api_client, utils

class ovsnode:
    def __init__(self):
        self._api = api_client.cloudbroker.diagnostics

    def activateNodes(self, nids):
        return self._api.activateNodes(nids=nids)

    def deactivateNodes(self, nids):
        return self._api.activateNodes(nids=nids)
        

