from framework.api import api_client, utils

class InfoMgr:
    def __init__(self):
        self._api = api_client

    def addInfo(self, info):
        return self._api.system.infomgr.addInfo(info=info)

    def getInfoWithHeaders(self, id, start, stop, maxvalues):
        return self._api.system.infomgr.getInfoWithHeaders(
            id=id,
            start=start,
            stop=stop,
            maxvalues=maxvalues
        )

    def reset(self):
        return self._api.system.infomgr.reset()
