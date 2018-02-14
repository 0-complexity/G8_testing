from framework.api import api_client, utils

class Log:
    def __init__(self):
        self._api = api_client

    def purge(self, age):
        return self._api.system.log.purge(age=age)