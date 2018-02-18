from framework.api import api_client, utils

class Audits:
    def __init__(self):
        self._api = api_client

    def listAudits(self, **kwargs):
        return self._api.system.audits.listAudits(** kwargs)
