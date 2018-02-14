from framework.api import *

class ovsnode:
    def __init__(self):
        self._api = api_client.cloudbroker.iaas

    def addExternalIPs(self,externalnetworkId,startip,endip):
        return self._api.addExternalIPs(externalnetworkId=externalnetworkId, startip=startip, endip=endip)

    def changeIPv4Gateway(self, externalnetworkId, gateway):
        return self._api.changeIPv4Gateway(externalnetworkId=externalnetworkId, gateway=gateway)

    def deleteExternalNetwork(self, externalnetworkId):
        return self._api.deleteExternalNetwork(externalnetworkId=externalnetworkId)

    def deleteSize(self, sizeid):
        return self._api.deleteSize(size_id=sizeid)
  
    def editPingIps(self, externalnetworkId,pingips ):
        return self._api.editPingIps(externalnetworkId=externalnetworkId,pingips=pingips)
  
    def removeExternalIP(self, externalnetworkId, ip):
        return self._api.removeExternalIP(externalnetworkId=externalnetworkId, ip=ip)

  
    def removeExternalIPs(self, externalnetworkId, freeips):
        return self._api.removeExternalIP(externalnetworkId=externalnetworkId, freeips=freeips)

 
        