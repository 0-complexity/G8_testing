from framework.api import *

class machine:
    def __init__(self):
        self._api = api_client.cloudbroker.machine

    def addDisk(self, machineId	,**kwargs):
        pass
    def addUser(self,username,machineId,**kwargs):
        accesstype = kwargs.get('maxVDiskCapacity',random.choise['R','RCX','ARCX'])
        response = self._api.addUser(username=username,machineId=machineId,accesstype=accesstype)
        return response,accesstype
    
    def attachExternalNetwork(self, machineId):
        return self._api.attachExternalNetwork(machineId=machineId)

    def clone(self, machineId, **kwargs ):
        data={'machineId':machineId,
              'cloneName':utils.random_string(),
              'reason':utils.random_string}
        data.update(** kwargs)
        return data, self._api.clone(**data)        

    def convertToTemplate(self, machineId, **kwargs):
        data={'machineId':machineId,
              'templateName':utils.random_string(),
              'reason':utils.random_string}
        data.update(** kwargs)
        return data, self._api.convertToTemplate(**data)     

    def create(self, cloudspaceId, **kwargs):
        data = {
            'cloudspaceId': cloudspaceId,
            'name': utils.random_string(),
            'description': utils.random_string(),
            'datadisks': [],
            'userdata': ''
        }
        response = self._api.cloudapi.images.list()
        response.raise_for_status()
        image = random.choice([x for x in response.json() if x.startswith(('Window', 'Linux'))])
        data['imageId'] = image['id']
        sizes = api_client.cloudapi.sizes.list(cloudspaceId=cloudspaceId)

        basic_sizes=[512,1024,4096,8192,16384,2048]
        size=[size for size in sizes if size['memory'] in basic_sizes][0]
        data['disksize']= random.choice(size['disks'])
        data['sizeId']=size['id']
        if kwargs.get('stackid'):
            data['stackid']=kwargs['stackid']

        data.update(** kwargs)

        return data,self._api.cloudapi.machines.create(**data)

    def createPortForward(self, machineId, localport=22,destPort=444,proto='tcp'):
        return self._api.createPortForward(machineId=machineId,localport=localport, destPort=destPort,proto=proto)


    def deletePortForward(self, machineId, localport=22,destPort=444,proto='tcp'):
        return self._api.deletePortForward(machineId=machineId,localport=localport, destPort=destPort,proto=proto)
        


    def deleteDisk(self, machineId, diskId):
        return self._api.deleteDisk(machineId=machineId, diskId=diskId)
    
    def deleteUser(self, machineId, userId):        
        return self._api.deleteUser(
            machineId=machineId,
            userId=userId)
    def deleteSnapshot(self, machineId, epoch, reason):
        return self._api.deleteSnapshot(machineId=machineId, epoch=epoch, reason=reason)

    def destroy(self, machineId,**kwargs):
        reason = kwargs.get('reason',utils.random_string())       
        return self._api.destroy(machineId=machineId	,reason=reason)

    def destroyMachines(self, machineIds,**kwargs):
        reason = kwargs.get('reason',utils.random_string())       
        return self._api.destroyMachines(machineIds=machineIds,reason=reason)


    def detachExternalNetwork(self, machineId):
        return self._api.detachExternalNetwork(machineId=machineId)

    def get(self, machineId):
        return self._api.get(machineId=machineId)
        
    def getHistory(self, machineId):
        return self._api.getHistory(machineId=machineId)

    def listPortForwards(self, machineId,**kwargs):
        result = kwargs.get('reason',utils.random_string())       
        return self._api.destroy(machineId=machineId,result=result)

    def listSnapshots(self, machineId):
        return self._api.listSnapshots(machineId=machineId)

    def pause(self, machineId,**kwargs):
        reason = kwargs.get('reason',utils.random_string())       
        return self._api.pause(machineId=machineId,reason=reason)


    def reboot(self, machineId,**kwargs):
        reason = kwargs.get('reason', utils.random_string())       
        return self._api.reboot(machineId=machineId,reason=reason)

    def rebootMachines(self, machineIds,**kwargs):
        reason = kwargs.get('reason', utils.random_string())       
        return self._api.rebootMachines(machineIds=machineIds,reason=reason)

    def restore(self, machineId,**kwargs):
        reason = kwargs.get('reason', utils.random_string())       
        return self._api.restore(machineId=machineId,reason=reason)


    def resume(self, machineId,**kwargs):
        reason = kwargs.get('reason', utils.random_string())       
        return self._api.resume(machineId=machineId,reason=reason)


    def start(self, machineId,**kwargs):
        reason = kwargs.get('reason', utils.random_string())       
        return self._api.resume(machineId=machineId,reason=reason)


    def startMachines(self, machineIds,**kwargs):
        reason = kwargs.get('reason', utils.random_string())       
        return self._api.startMachines(machineIds=machineIds,reason=reason)

    def stop(self, machineId,**kwargs):
        reason = kwargs.get('reason', utils.random_string())       
        return self._api.stop(machineId=machineId,reason=reason)

    def stopMachines(self, machineIds,**kwargs):
        reason = kwargs.get('reason', utils.random_string())       
        return self._api.stopMachines(machineIds=machineIds,reason=reason)

    def moveToDifferentComputeNode(self, machineId,**kwargs):
        pass

    def rollbackSnapshot(self, machineId, **kwargs):
        snapshotEpoch = api_client.cloudapi.machines.listSnapshots(machineId=machineId)[0]['epoch']
        data = {'machineId':machineId,
                'epoch':snapshotEpoch,
                'reason':utils.random_string()}
        data.update(** kwargs)        
        response = self._api.rollbackSnapshot(**data)
        return data,response

    def snapshot(self, machineId, **kwargs):
        data={"machineId":machineId,
              "snapshotname":utils.random_string(),
              "reason":utils.random_string
              }

        data.update(**kwargs)
        response = self._api.snapshot(**data)
        return data , response 

    def tag(self, machineId,**kwargs):
        tagName = kwargs.get('tag', utils.random_string())       
        response =  self._api.tag(machineId=machineId, tagName=tagName)        
        return tagName,response 


    def untag(self, machineId, tagName):
        return self._api.untag(machineId=machineId, tagName=tagName)


    def update(self, machineId, **kwargs):
        data = {
            'machineId': machineId,
            'name': utils.random_string(),
            'description': utils.random_string(),
        }
        data.update(** kwargs)
        return data, self._api.update(** data)

        
