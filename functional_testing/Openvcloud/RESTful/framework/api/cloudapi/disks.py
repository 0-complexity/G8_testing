from framework.api import api_client
from framework.utils.utils import Utils

class Disks:
    def __init__(self):
        self._api = api_client.cloudapi.disks
        self.utils = Utils()

    def list(self, accountId):
        disktype = kwargs.get('type', None)
        return self._api.list(accountId=accountId, type=disktype)
    
    def get(self, diskId):
        return self._api.get(diskId=diskId)

    def create(self, accountId, gid, type, **kwargs):
        name = kwargs.get('name', self.utils.random_string())
        description = kwargs.get('description', self.utils.random_string())
        disktype = kwargs.get('type', 'D')
        size = kwargs.get('size', None)
        ssdSize = kwargs.get('ssdSize', None)
        iops = kwargs.get('iops', None)

        return self._api.create(
            accountId=accountId,
            gid=gid,
            name=name,
            description=description,
            type=disktype,
            size=size,
            ssdSize=ssdSize,
            iops=iops,
        )