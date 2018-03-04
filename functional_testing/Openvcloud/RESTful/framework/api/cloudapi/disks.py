from framework.api import  utils
import random

class Disks:
    def __init__(self, api_client):
        self._api = api_client

    def list(self, accountId, ** kwargs):
        disktype = kwargs.get('type')
        return self._api.cloudapi.disks.list(accountId=accountId, type=disktype)
    
    def get(self, diskId):
        return self._api.cloudapi.disks.get(diskId=diskId)

    def create(self, accountId, gid, **kwargs):
        data = {
            'accountId': accountId,
            'gid': gid,
            'name': utils.random_string(),
            'description': utils.random_string(),
            'type': random.choice(['D', 'B', 'T']),
            'size': random.randint(1, 1000),
            'ssdSize': random.randint(1, 1000),
            'iops': random.randint(100, 5000)
        }
        data.update(**kwargs)        
        return data, self._api.cloudapi.disks.create(** data)

    def resize(self, diskId, size):
        return self._api.cloudapi.disks.resize(diskId=diskId, size=size)

    def delete(self, diskId, ** kwargs):
        detach = kwargs.get('detach', False)
        return self._api.cloudapi.disks.delete(diskId=diskId, detach=detach)