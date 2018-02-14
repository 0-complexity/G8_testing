from framework.api import api_client, utils

class qos:
    def __init__(self):
        self._api = api_client.cloudbroker.qos
    
    def limitCPU(self, machineId):
        return self._api.limitCPU(machineId=machineId)
    
    def resize(self, diskId, size):
        return self._api.resize(diskId=diskId, size=size)


    def limitIO(self, diskId,**kwargs):
        return self._api.limitIO(diskId, **kwargs)
    
    def limitInternetBandwith(self, cloudspacId, rate, burst):
        return self._api.limitInternetBandwith(cloudspacId=cloudspacId, rate=rate, burst=burst)
        
