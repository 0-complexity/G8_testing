from framework.api import api_client
from framework.utils.utils import Utils

class Disks:
    def __init__(self):
        self._api = api_client.cloudapi.disks
        self.utils = Utils()

    def list(self, accountId):
        disktype = kwargs.get('type')
        return self._api.list(accountId=accountId, type=disktype)
    
    def get(self, diskId):
        return self._api.get(diskId=diskId)

    def create(self, accountId, gid, type, **kwargs):
        name = kwargs.get('name', self.utils.random_string())
        description = kwargs.get('description', self.utils.random_string())
        disktype = kwargs.get('type', 'D')

        return self._api.create(
            accountId=accountId,
            gid=gid,
            name=name,
            description=description,
            type=disktype,
            **kwargs
        )

    def resize(self, diskId, size):
        return self._api.resize(diskId=diskId, size=size)

    def delete(self, diskId, detach):
        detach = kwargs.get('detach')
        return self._api.delete(diskId=diskId, detach=detach)