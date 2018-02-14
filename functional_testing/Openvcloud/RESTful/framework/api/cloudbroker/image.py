from framework.api import *
import random 

class Image:
    def __init__(self):
        self._api = api_client.cloudbroker.image
    
    def delete(self,imageId):
        return self._api.delete(imageId=imageId)
    
    def disable(self,imageId):
        return self._api.disable(imageId=imageId)   
    
    def enable(self,imageId):
        return self._api.disable(imageId=imageId)   

    def updateNodes(self,imageId , enabledStacks):
        return self._api.disable(imageId=imageId, enabledStacks=enabledStacks)   
    
        
    