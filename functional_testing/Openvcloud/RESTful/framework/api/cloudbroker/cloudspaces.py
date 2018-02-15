import random
from framework.api import api_client, utils 

class Cloudspaces:
    def __init__(self):
        self._api = api_client

    def addExtraIP(self, cloudspaceId, ipaddress):
        return self._api.cloudbroker.Cloudspace.addExtraIP(cloudspaceId=cloudspaceId, ipaddress=ipaddress)

    def addUser(self, username, cloudspaceId,**kwargs):
        data = {
            'username': username, 
            'cloudspaceId': cloudspaceId,
            'accesstype': random.choise(['R','RCX','ARCX'])
        }
        data.update(** kwargs)
        return data, self._api.cloudbroker.Cloudspace.addUser(** data)

    def create(self, accountId, location, access, **kwargs):
        data = {
            'accountId': accountId,
            'location': location,
            'access': access,
            'name': utils.random_string(),
            'maxMemoryCapacity': -1,
            'maxVDiskCapacity': -1,
            'maxCPUCapacity': -1,
            'maxNetworkPeerTransfer': -1,
            'maxNumPublicIP': -1,
            'allowedVMSizes': [],
            'privatenetwork': ''
            
        }
        data.update(** kwargs)
        return data, self._api.cloudbroker.Cloudspace.create(** data)

    def update(self, cloudspaceId, **kwargs):
        data = {
            'cloudspaceId': cloudspaceId,
            'name': utils.random_string(),
            'maxMemoryCapacity': -1,
            'maxVDiskCapacity': -1,
            'maxCPUCapacity': -1,
            'maxNetworkPeerTransfer': -1,
            'maxNumPublicIP': -1,
            'allowedVMSizes': [],
        }
        data.update(** kwargs)
        return data, self._api.cloudbroker.Cloudspace.update(** data)

    def applyConfig(self, cloudspaceId):
        return self._api.cloudbroker.Cloudspace.appapplyConfig(cloudspaceId=cloudspaceId)

    def delete(self, cloudspaceId):
        return self._api.cloudbroker.Cloudspace.delete(cloudspaceId=cloudspaceId)

    def deletePortForward(self, cloudspaceId, publicIp, publicPort, protocol):
        return self._api.cloudbroker.Cloudspace.deletePortForward(
            cloudspaceId =cloudspaceId,
            publicIp=publicIp,
            publicPort=publicPort,
            protocol=protocol
        )

    def deleteUser(self, cloudspaceId, userId, recursivedelete=False):        
        return self._api.cloudbroker.Cloudspace.deleteUser(
            cloudspaceId=cloudspaceId,
            userId=userId,
            recursivedelete=recursivedelete
        )

    def deployVFW(self, cloudspaceId):
        return self._api.cloudbroker.Cloudspace.deployVFW(cloudspaceId=cloudspaceId)
    
    def moveVirtualFirewallToFirewallNode(self, cloudspaceId, targetNid):
        return self._api.cloudbroker.Cloudspace.moveVirtualFirewallToFirewallNode(cloudspaceId=cloudspaceId, targetNid=targetNid)
      
    def destroy(self, cloudspaceId, accountId, **kwargs):
        reason = kwargs.get('reason',utils.random_string())       
        return self._api.cloudbroker.Cloudspace.deployVFW(accountId=accountId, cloudspaceId=cloudspaceId, reason=reason)

    def destroyCloudSpaces(self, cloudspaceIds, **kwargs):
        reason = kwargs.get('reason',utils.random_string())       
        return self._api.cloudbroker.Cloudspace.deployVFW(cloudspaceIds=cloudspaceIds, reason=reason)

    def destroyVFW(self, cloudspaceId):
        return self._api.cloudbroker.Cloudspace.destroyVFW(cloudspaceId=cloudspaceId)

    def getVFW(self, cloudspaceId):
        return self._api.cloudbroker.Cloudspace.getVFW(cloudspaceId=cloudspaceId)

    def removeIP(self, cloudspaceId, ipaddress):
        return self._api.cloudbroker.Cloudspace.removeIP(cloudspaceId=cloudspaceId,ipaddress=ipaddress)     

    def startVFW(self, cloudspaceId):
        return self._api.cloudbroker.Cloudspace.startVFW(cloudspaceId=cloudspaceId)

    def stopVFW(self, cloudspaceId):
        return self._api.cloudbroker.Cloudspace.stopVFW(cloudspaceId=cloudspaceId)
    
    def resetVFW(self, cloudspaceId, resettype):
        return self._api.cloudbroker.Cloudspace.resetVFW(cloudspaceId=cloudspaceId, resettype=resettype)
