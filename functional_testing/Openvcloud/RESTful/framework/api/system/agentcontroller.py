from framework.api import api_client, utils

class AgentController:
    def __init__(self):
        self._api = api_client

    def executeJumpscript(self, gid, organization, name, **kwargs):
        return self._api.system.agentcontroller.executeJumpscript(
            gid=gid,
            organization=organization,
            name=name,
            **kwargs
        )

    def listActiveSessions(self):
        return self._api.system.agentcontroller.listActiveSessions()

    def listSessions(self):
        return self._api.system.agentcontroller.listSessions()

    def loadJumpscripts(self, path):
        return self._api.system.agentcontroller.loadJumpscripts(path=path)

    