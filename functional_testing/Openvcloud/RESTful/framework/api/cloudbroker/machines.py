from framework.api import api_client
from framework.utils.utils import Utils

class machine:
    def __init__(self):
        self._api = api_client.cloudbroker.machine
        self.utils = Utils()

    def addDisk(self, machineId	,**kwargs):
        pass
    def addUser(self,username,machineId,**kwargs):
        accesstype = kwargs.get('maxVDiskCapacity',random.choise['R','RCX','ARCX'])
        response = self._api.addUser(username=username,machineId=machineId,accesstype=accesstype)
        return response,accesstype
    
    def attachExternalNetwork(self, machineId):
        return self._api.attachExternalNetwork(machineId=machineId)

    def deleteDisk(self, machineId, diskId):
        return self._api.deleteDisk(machineId=machineId, diskId=diskId)
    
    def deleteUser(self, machineId, userId):        
        return self._api.deleteUser(
            machineId=machineId,
            userId=userId)

    def destroy(self, machineId,**kwargs):
        reason = kwargs.get('reason',self.utils.random_string())       
        return self._api.destroy(machineId=machineId	,reason=reason)

    def destroyMachines(self, machineIds,**kwargs):
        reason = kwargs.get('reason',self.utils.random_string())       
        return self._api.destroyMachines(machineIds=machineIds,reason=reason)


    def detachExternalNetwork(self, machineId):
        return self._api.detachExternalNetwork(machineId=machineId)

    def get(self, machineId):
        return self._api.get(machineId=machineId)
        
    def getHistory(self, machineId):
        return self._api.getHistory(machineId=machineId)

    def listPortForwards(self, machineId,**kwargs):
        result = kwargs.get('reason',self.utils.random_string())       
        return self._api.destroy(machineId=machineId,result=result)

    def listSnapshots(self, machineId):
        return self._api.listSnapshots(machineId=machineId)

    def pause(self, machineId,**kwargs):
        reason = kwargs.get('reason',self.utils.random_string())       
        return self._api.pause(machineId=machineId,reason=reason)


    def reboot(self, machineId,**kwargs):
        reason = kwargs.get('reason',self.utils.random_string())       
        return self._api.reboot(machineId=machineId,reason=reason)

    def rebootMachines(self, machineIds,**kwargs):
        reason = kwargs.get('reason',self.utils.random_string())       
        return self._api.rebootMachines(machineIds=machineIds,reason=reason)

    def restore(self, machineId,**kwargs):
        reason = kwargs.get('reason',self.utils.random_string())       
        return self._api.restore(machineId=machineId,reason=reason)


    def resume(self, machineId,**kwargs):
        reason = kwargs.get('reason',self.utils.random_string())       
        return self._api.resume(machineId=machineId,reason=reason)


    def start(self, machineId,**kwargs):
        reason = kwargs.get('reason',self.utils.random_string())       
        return self._api.resume(machineId=machineId,reason=reason)


    def startMachines(self, machineIds,**kwargs):
        reason = kwargs.get('reason',self.utils.random_string())       
        return self._api.startMachines(machineIds=machineIds,reason=reason)

    def stop(self, machineId,**kwargs):
        reason = kwargs.get('reason',self.utils.random_string())       
        return self._api.stop(machineId=machineId,reason=reason)

    def stopMachines(self, machineIds,**kwargs):
        reason = kwargs.get('reason',self.utils.random_string())       
        return self._api.stopMachines(machineIds=machineIds,reason=reason)

