from framework.api import utils

class Accounts:
    def __init__(self, api_client):
        self._api = api_client

    def list(self):
        return self._api.cloudapi.accounts.list()
    
    def get(self, accountId):
        return self._api.cloudapi.accounts.get(accountId=accountId)

    def create(self, access, **kwargs):
        data = {
            'name': utils.random_string(),
            'access': access,
            'maxMemoryCapacity': -1,
            'maxVDiskCapacity': -1,
            'maxCPUCapacity': -1,
            'maxNetworkPeerTransfer': -1,
            'maxNumPublicIP': -1,
        }
        data.update(** kwargs)
        return data, self._api.cloudapi.accounts.create(** data)

    def update(self, accountId, **kwargs):
        return self._api.cloudapi.accounts.update(accountId=accountId, **kwargs)
    
    def addUser(self, accountId, userId, accesstype='ARCXDU'):
        return self._api.cloudapi.accounts.addUser(
            accountId=accountId,
            userId=userId,
            accesstype=accesstype
        )

    def deleteUser(self, accountId, userId, recursivedelete=False):        
        return self._api.cloudapi.accounts.deleteUser(
            accountId=accountId,
            userId=userId,
            recursivedelete=recursivedelete
        )

    def updateUser(self, accountId, userId, accesstype):
        return self._api.cloudapi.accounts.addUser(
            accountId=accountId,
            userId=userId,
            accesstype=accesstype
        )

    def listTemplates(self, accountId):
        return self._api.cloudapi.accounts.listTemplates(accountId=accountId)

    def getConsumedCloudUnits(self, accountId):
        return self._api.cloudapi.accounts.getConsumedCloudUnits(accountId=accountId)
    
    def getConsumedCloudUnitsByType(self, accountId, cutype):
        return self._api.cloudapi.accounts.getConsumedCloudUnitsByType(accountId=accountId, cutype=cutype)

    def getConsumption(self, accountId, start, end):
        return self._api.cloudapi.accounts.getConsumption(
            accountId=accountId,
            start=start,
            end=end
        )
    
