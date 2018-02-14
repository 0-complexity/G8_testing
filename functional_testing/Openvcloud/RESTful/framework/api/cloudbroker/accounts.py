from framework.api import *

class Accounts:
    def __init__(self):
        self._api = api_client.cloudbroker.accounts

    def addUser(self,username,accountId,**kwargs):
        accesstype = kwargs.get('maxVDiskCapacity',random.choise['R','RCX','ARCX'])
        response = self._api.addUser(username=username,accountId=accountId,accesstype=accesstype)
        return response,accesstype

    def create(self, username, **kwargs):
        data={
              "name" : utils.random_string(),
              "username" : username,
              "maxMemoryCapacity": -1,
              "maxVDiskCapacity": -1,
              "maxCPUCapacity": -1,
              "maxNetworkPeerTransfer": -1,
              "maxNumPublicIP": -1
             }
        data.update(** kwargs)
        return data, self._api.create(**data)

    def delete(self, accountId, **kwargs):
        reason = kwargs.get('reason', utils.random_string())
        return self._api.delete(accountId=accountId,reason=reason)
    
    def deleteAccounts(self, accountIds, **kwargs):
        reason = kwargs.get('reason', utils.random_string())
        return self._api.deleteAccounts(accountIds=accountIds,
                                        reason=reason
                                        )

    def update(self, accountId, **kwargs):
        data = {
                'accountId': accountId,
                'name': utils.random_string(),
                'maxMemoryCapacity': -1,
                'maxVDiskCapacity': -1,
                'maxCPUCapacity': -1,
                'maxNetworkPeerTransfer': -1,
                'maxNumPublicIP': -1
              }

        data.update(** kwargs)
        return data, self._api.cloudapi.cloudspaces.update(** data)

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

    def disable(self, accountId, **kwargs):
        reason = kwargs.get('reason', utils.random_string())
        return self._api.disable(accountId=accountId,reason=reason)

    def enable(self, accountId, **kwargs):
        reason = kwargs.get('reason', utils.random_string())
        return self._api.enable(accountId=accountId,reason=reason)
