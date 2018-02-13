from framework.api import api_client

class Cloudspaces:
    def __init__(self):
        self._api = api_client.cloudapi.cloudspaces

    def list(self):
        return self._api.list()

    def get(self, cloudspaceId):
        return self._api.get(cloudspaceId=cloudspaceId)

    def create(self, accountId, location, access, **kwargs):
        name = kwargs.get('name', utils.random_string())
        maxMemoryCapacity = kwargs.get('maxMemoryCapacity', -1)
        maxVDiskCapacity = kwargs.get('maxVDiskCapacity', -1)
        maxCPUCapacity = kwargs.get('maxCPUCapacity', -1)
        maxNetworkPeerTransfer = kwargs.get('maxNetworkPeerTransfer', -1)
        maxNumPublicIP = kwargs.get('maxNumPublicIP', -1)
        
        return self._api.create(
            accountId=accountId,
            location=location,
            access=access,
            name=name,
            maxMemoryCapacity=maxMemoryCapacity,
            maxVDiskCapacity=maxVDiskCapacity,
            maxCPUCapacity=maxCPUCapacity,
            maxNetworkPeerTransfer=maxNetworkPeerTransfer,
            maxNumPublicIP=maxNumPublicIP,
            **kwargs
        )

    def update(self, cloudspaceId, **kwargs):
        return self._api.update(cloudspaceId=cloudspaceId, **kwargs)

    def delete(self, cloudspaceId):
        return self._api.delete(cloudspaceId=cloudspaceId)

    def deploy(self, cloudspaceId):
        return self._api.deploy(cloudspaceId=cloudspaceId)

    def enable(self, cloudspaceId, **kwargs):
        reason = kwargs.get('reason', utils.random_string())
        return self._api.enable(cloudspaceId=cloudspaceId, reason=reason)

    def disable(self, cloudspaceId, **kwargs):
        reason = kwargs.get('reason', utils.random_string())
        return self._api.disable(cloudspaceId=cloudspaceId, reason=reason)

    def getDefenseShield(self, cloudspaceId):
        return self._api.getDefenseShield(cloudspaceId=cloudspaceId)
    
    def getOpenvpnConfig(self, cloudspaceId):
        return self._api.getOpenvpnConfig(cloudspaceId=cloudspaceId)

    def addAllowedSize(self, cloudspaceId, sizeId):
        return self._api.addAllowedSize(cloudspaceId=cloudspaceId, sizeId=sizeId)

    def removeAllowedSize(self, cloudspaceId, sizeId):
        return self._api.removeAllowedSize(cloudspaceId=cloudspaceId, sizeId=sizeId)

    def addUser(self, cloudspaceId, userId, accesstype='ARCXDU'):
        return self._api.addUser(
            cloudspaceId=cloudspaceId,
            userId=userId,
            accesstype=accesstype
        )

    def deleteUser(self, cloudspaceId, userId, recursivedelete=False):        
        return self._api.deleteUser(
            cloudspaceId=cloudspaceId,
            userId=userId,
            recursivedelete=recursivedelete
        )

    def updateUser(self, cloudspaceId, userId, accesstype):
        return self._api.addUser(
            cloudspaceId=cloudspaceId,
            userId=userId,
            accesstype=accesstype
        )

    def executeRouterOSScript(self, cloudspaceId, script):
        return self._api.executeRouterOSScript(cloudspaceId=cloudspaceId, script=script)

    