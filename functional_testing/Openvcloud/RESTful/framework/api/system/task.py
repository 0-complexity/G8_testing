from framework.api import api_client, utils

class Task:
    def __init__(self):
        self._api = api_client

    def authenticate(self, taskguid):
        return self._api.system.task.get(taskguid=taskguid)

    def authorize(self, taskguid):
        return self._api.system.task.kill(taskguid=taskguid)