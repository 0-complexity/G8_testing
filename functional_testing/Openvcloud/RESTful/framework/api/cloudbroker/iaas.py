from framework.api import a

class ovsnode:
    def __init__(self):
        self._api = api_client.cloudbroker.iaas

    def addExternalIPs(self,externalnetworkId,startip,endip):
        return self._api.addExternalIPs(externalnetworkId=externalnetworkId, startip=startip, endip=endip)

