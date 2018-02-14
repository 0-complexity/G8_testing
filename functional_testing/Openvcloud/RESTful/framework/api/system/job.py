from framework.api import api_client, utils

class Job:
    def __init__(self):
        self._api = api_client

    def purge(self, age):
        return self._api.system.job.purge(age=age)