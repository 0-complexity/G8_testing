from framework.api import *
import random 

class Cloudspaces:
    def __init__(self):
        self._api = api_client.cloudbroker.Cloudspace

    def addExtraIP(self, cloudspaceId,**kwargs):
        ip = '192.168.%i.%i/24' % (random.randint(1, 254),random.randint(1, 254))
        ipaddress=kwargs.get('ipaddress',ip)
        return self._api.addExtraIP(cloudspaceId=cloudspaceId,ipaddress=ipaddress)

    def addUser(self,username,cloudspaceId,**kwargs):
        accesstype = kwargs.get('maxVDiskCapacity', random.choise(['R','RCX','ARCX']))
        response = self._api.addUser(username=username,cloudspaceId=cloudspaceId,accesstype=accesstype)
        return response,accesstype

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
        return data, self._api.create(** data)

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
        return data, self._api.update(** data)

    def applyConfig(self, cloudspaceId):
        return self._api.appapplyConfig(cloudspaceId=cloudspaceId)

    def delete(self, cloudspaceId):
        return self._api.delete(cloudspaceId=cloudspaceId)

    def deletePortForward(self, cloudspaceId, publicIp, publicPort,proto):
        return self._api.deletePortForward(cloudspaceId =cloudspaceId,
                                            publicIp=publicIp,
                                            publicPort=publicPort,
                                            proto=proto
                                            )
    def deleteUser(self, cloudspaceId, userId, recursivedelete=False):        
        return self._api.deleteUser(
            cloudspaceId=cloudspaceId,
            userId=userId,
            recursivedelete=recursivedelete
                                    )

    def deploy(self, cloudspaceId):
        return self._api.deploy(cloudspaceId=cloudspaceId)

    def deployVFW(self, cloudspaceId):
        return self._api.deployVFW(cloudspaceId=cloudspaceId)
    
    def moveVirtualFirewallToFirewallNode(self, cloudspaceId, targetNid):
        return self._api.moveVirtualFirewallToFirewallNode(cloudspaceId=cloudspaceId, targetNid=targetNid)
      

    def destroy(self, cloudspaceId, accountId, **kwargs):
        reason = kwargs.get('reason',utils.random_string())       
        return self._api.deployVFW(accountId=accountId, cloudspaceId=cloudspaceId,reason=reason)

    def destroyCloudSpaces(self, cloudspaceIds, **kwargs):
        reason = kwargs.get('reason',utils.random_string())       
        return self._api.deployVFW(cloudspaceIds=cloudspaceIds,reason=reason)

    def destroyVFW(self, cloudspaceId):
        return self._api.destroyVFW(cloudspaceId=cloudspaceId)


    def getVFW(self, cloudspaceId):
        return self._api.getVFW(cloudspaceId=cloudspaceId)

    def removeIP(self, cloudspaceId, ipaddress):
        return self._api.removeIP(cloudspaceId=cloudspaceId,ipaddress=ipaddress)     

    def startVFW(self, cloudspaceId):
        return self._api.startVFW(cloudspaceId=cloudspaceId)

    def stopVFW(self, cloudspaceId):
        return self._api.stopVFW(cloudspaceId=cloudspaceId)
    
    def resetVFW(self, cloudspaceId, **kwargs):
        resettype=kwargs.get("resettype",random.choice(["factory","restore"]))
        return self._api.resetVFW(cloudspaceId=cloudspaceId, resettype=resettype )
