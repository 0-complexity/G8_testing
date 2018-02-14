from framework.api import api_client, utils

class DocGenerator:
    def __init__(self):
        self._api = api_client

    def prepareCatalog(self):
        return self._api.system.docgenerator.prepareCatalog()