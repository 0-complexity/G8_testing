from framework.api import api_client

class Machines:
    def __init__(self):
        self._api = api_client

    def addDisk(self, machineId, **kwargs):
        diskName = kwargs.get('diskName', utils.random_string())
        description = kwargs.get('description', utils.random_string())
        size = kwargs.get('size', 25)
        disktype = kwargs.get('type', 'D')

        return self._api.cloudapi.machines.addDisk(
            machineId=machineId,
            diskName=diskName,
            description=description,
            size=size,
            disktype=disktype,
            **kwargs
        )

    def addUser(self, machineId, userId, accesstype='ARCXDU'):        
        return self._api.cloudapi.machines.addUser(
            machineId=machineId,
            userId=userId,
            accesstype=accesstype
        )

    def attachDisk(self, machineId, diskId):        
        return self._api.cloudapi.machines.attachDisk(
            machineId=machineId,
            diskId=diskId
        )
    
    def attachExternalNetwork(self, machineId):        
        return self._api.cloudapi.machines.attachExternalNetwork(
            machineId=machineId
        )

    def clone(self, machineId, **kwargs):   
        name = kwargs.get('name', utils.random_string())     
        return self._api.cloudapi.machines.clone(
            machineId=machineId,
            name=name,
            **kwargs
        )

    def convertToTemplate(self, machineId, **kwargs):   
        templatename = kwargs.get('templatename', utils.random_string())     
        return self._api.cloudapi.machines.convertToTemplate(
            machineId=machineId,
            templatename=templatename
        )

    def create(self, cloudspaceId, sizeId, imageId, disksize, **kwargs):   
        name = kwargs.get('name', utils.random_string())    
        description = kwargs.get('description', utils.random_string()) 
        datadisks = kwargs.get('datadisks', [])

        return self._api.cloudapi.machines.create(
            cloudspaceId=cloudspaceId,
            name=name,
            description=description,
            sizeId=sizeId,
            imageId=imageId,
            disksize=disksize,
            datadisks=datadisks,
            **kwargs
        )

    def delete(self, machineId):   
        return self._api.cloudapi.machines.delete(machineId=machineId)

    def deleteSnapshot(self, machineId, **kwargs):
        return self._api.cloudapi.machines.deleteSnapshot(machineId=machineId, **kwargs)

    def deleteUser(self, machineId, userId):
        return self._api.cloudapi.machines.deleteUser(machineId=machineId, userId=userId)

    def detachDisk(self, machineId, diskId):
        return self._api.cloudapi.machines.deletedetachDiskUser(machineId=machineId, userId=userId)

    def detachExternalNetwork(self, machineId):
        return self._api.cloudapi.machines.detachExternalNetwork(machineId=machineId)

    def exportOVF(self, link, username, passwd, path, machineId, **kwargs):
        return self._api.cloudapi.machines.exportOVF(
            link=link,
            username=username,
            passwd=passwd,
            path=path,
            machineId=machineId,
            **kwargs
        )

    def importOVF(self, link, username, passwd, path, cloudspaceId, sizeId, **kwargs):
        name = kwargs.get('name', utils.random_string())    
        description = kwargs.get('description', utils.random_string()) 

        return self._api.cloudapi.machines.importOVF(
            link=link,
            username=username,
            passwd=passwd,
            path=path,
            cloudspaceId=cloudspaceId,
            name=name,
            description=description,
            sizeId=sizeId,
            **kwargs
        )

    def get(self, machineId):   
        return self._api.cloudapi.machines.get(machineId=machineId)

    def getConsoleUrl(self, machineId):   
        return self._api.cloudapi.machines.getConsoleUrl(machineId=machineId)

    def getHistory(self, machineId):   
        return self._api.cloudapi.machines.getHistory(machineId=machineId)

    def list(self, cloudspaceId):   
        return self._api.cloudapi.machines.list(cloudspaceId=cloudspaceId)

    def listSnapshots(self, machineId):   
        return self._api.cloudapi.machines.listSnapshots(machineId=machineId)

    def pause(self, machineId):   
        return self._api.cloudapi.machines.pause(machineId=machineId)
    
    def reboot(self, machineId):   
        return self._api.cloudapi.machines.reboot(machineId=machineId)

    def reset(self, machineId):   
        return self._api.cloudapi.machines.reset(machineId=machineId)

    def resume(self, machineId):   
        return self._api.cloudapi.machines.resume(machineId=machineId)

    def start(self, machineId):   
        return self._api.cloudapi.machines.start(machineId=machineId)

    def stop(self, machineId):   
        return self._api.cloudapi.machines.stop(machineId=machineId)

    def resize(self, machineId, sizeId):   
        return self._api.cloudapi.machines.resize(machineId=machineId, sizeId=sizeId)

    def rollbackSnapshot(self, machineId, **kwargs):
        return self._api.cloudapi.machines.rollbackSnapshot(machineId=machineId, **kwargs)

    def snapshot(self, machineId, **kwargs):
        name = kwargs.get('name', utils.random_string())
        return self._api.cloudapi.machines.snapshot(machineId=machineId, name=name)

    def update(self, machineId, **kwargs):
        name = kwargs.get('name', utils.random_string())
        description = kwargs.get('description', utils.random_string())
        return self._api.cloudapi.machines.update(
            machineId=machineId, 
            name=name,
            description=description
        )

    def updateUser(self, machineId, userId, accesstype):
        return self._api.cloudapi.machines.updateUser(
            machineId=machineId, 
            userId=userId,
            accesstype=accesstype
        )