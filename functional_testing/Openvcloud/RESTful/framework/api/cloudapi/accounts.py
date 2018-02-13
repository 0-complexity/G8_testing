from framework.api import api_client

class Accounts:
    def __init__(self):
        self._api = api_client.cloudapi.accounts

    def list(self):
        return self._api.list()
    
    def get(self, accountId):
        return self._api.get(accountId=accountId)

    def create(self, access, **kwargs):
        name = kwargs.get('name', utils.random_string())
        maxMemoryCapacity = kwargs.get('maxMemoryCapacity', -1)
        maxVDiskCapacity = kwargs.get('maxVDiskCapacity', -1)
        maxCPUCapacity = kwargs.get('maxCPUCapacity', -1)
        maxNetworkPeerTransfer = kwargs.get('maxNetworkPeerTransfer', -1)
        maxNumPublicIP = kwargs.get('maxNumPublicIP', -1)

        return self._api.create(
            name=name,
            access=access,
            maxMemoryCapacity=maxMemoryCapacity,
            maxVDiskCapacity=maxVDiskCapacity,
            maxCPUCapacity=maxCPUCapacity,
            maxNetworkPeerTransfer=maxNetworkPeerTransfer,
            maxNumPublicIP=maxNumPublicIP
        )

    def update(self, accountId, **kwargs):
        return self._api.update(accountId=accountId, **kwargs)
    
    def addUser(self, accountId, userId, accesstype='ARCXDU'):
        return self._api.addUser(
            accountId=accountId,
            userId=userId,
            accesstype=accesstype
        )

    def deleteUser(self, accountId, userId, recursivedelete=False):        
        return self._api.deleteUser(
            accountId=accountId,
            userId=userId,
            recursivedelete=recursivedelete
        )

    def updateUser(self, accountId, userId, accesstype):
        return self._api.addUser(
            accountId=accountId,
            userId=userId,
            accesstype=accesstype
        )

    def listTemplates(self, accountId):
        return self._api.listTemplates(accountId=accountId)

    def getConsumedCloudUnits(self, accountId):
        return self._api.getConsumedCloudUnits(accountId=accountId)
    
    def getConsumedCloudUnitsByType(self, accountId, cutype):
        return self._api.getConsumedCloudUnitsByType(accountId=accountId, cutype=cutype)

    def getConsumption(self, accountId, start, end):
        return self._api.getConsumption(
            accountId=accountId,
            start=start,
            end=end
        )
    
