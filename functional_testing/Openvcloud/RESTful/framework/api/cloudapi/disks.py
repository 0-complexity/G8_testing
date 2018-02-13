from framework.api import api_client

class Disks:
    def __init__(self):
        self._api = api_client

    def list(self, accountId):
        disktype = kwargs.get('type')
        return self._api.cloudapi.disks.list(accountId=accountId, type=disktype)
    
    def get(self, diskId):
        return self._api.cloudapi.disks.get(diskId=diskId)

    def create(self, accountId, gid, type, **kwargs):
        name = kwargs.get('name', utils.random_string())
        description = kwargs.get('description', utils.random_string())
        disktype = kwargs.get('type', 'D')

        return self._api.cloudapi.disks.create(
            accountId=accountId,
            gid=gid,
            name=name,
            description=description,
            type=disktype,
            **kwargs
        )

    def resize(self, diskId, size):
        return self._api.cloudapi.disks.resize(diskId=diskId, size=size)

    def delete(self, diskId, detach):
        detach = kwargs.get('detach')
        return self._api.cloudapi.disks.delete(diskId=diskId, detach=detach)