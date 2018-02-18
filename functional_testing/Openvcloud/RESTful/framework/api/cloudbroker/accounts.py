import random
from framework.api import api_client, utils

class Accounts:
    def __init__(self):
        self._api = api_client

    def addUser(self, username, accountId, **kwargs):
        data = {
            'username': username,
            'accountId': accountId,
            'accesstype': random.choice(['R','RCX','ARCX'])
        }
        data.update(** kwargs)
        return data, self._api.cloudbroker.accounts.addUser(** data)

    def create(self, username, **kwargs):
        data = {
            "name" : utils.random_string(),
            "username" : username,
            "maxMemoryCapacity": -1,
            "maxVDiskCapacity": -1,
            "maxCPUCapacity": -1,
            "maxNetworkPeerTransfer": -1,
            "maxNumPublicIP": -1
        }
        data.update(** kwargs)
        return data, self._api.cloudbroker.accounts.create(**data)

    def delete(self, accountId, **kwargs):
        reason = kwargs.get('reason', utils.random_string())
        return self._api.cloudbroker.accounts.delete(accountId=accountId,reason=reason)
    
    def deleteAccounts(self, accountIds, **kwargs):
        reason = kwargs.get('reason', utils.random_string())
        return self._api.cloudbroker.accounts.deleteAccounts(accountIds=accountIds, reason=reason)

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
        return data, self._api.cloudbroker.accounts.update(** data)

    def deleteUser(self, accountId, userId, recursivedelete=False):        
        return self._api.cloudbroker.accounts.deleteUser(
            accountId=accountId,
            userId=userId,
            recursivedelete=recursivedelete
        )

    def updateUser(self, accountId, userId, accesstype):
        return self._api.cloudbroker.accounts.addUser(
            accountId=accountId,
            userId=userId,
            accesstype=accesstype
        )

    def disable(self, accountId, **kwargs):
        reason = kwargs.get('reason', utils.random_string())
        return self._api.cloudbroker.accounts.disable(accountId=accountId, reason=reason)

    def enable(self, accountId, **kwargs):
        reason = kwargs.get('reason', utils.random_string())
        return self._api.cloudbroker.accounts.enable(accountId=accountId, reason=reason)
