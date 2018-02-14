from framework.api import *
import random 

class User:
    def __init__(self):
        self._api = api_client.cloudbroker.user
    def create(self,**kwargs):
        username=utils.random_string()
        data={"username":username,
              "emailaddress":"%s@example.com" % username,
              "password":username,
              "groups":["level1","user","level2","level3","admin"]
              }
        data.update(**kwargs)
        response = self._api.create(**data)
        return data ,response

    def delete(self,username):
        return self._api.delete(username=username)

    def deleteByGuid(self,userguid):
        return self._api.deleteByGuid(userguid=userguid)
    
    def deleteUsers(self, userIds):
        return self._api.deleteUsers(userids=userIds)
    
    def generateAuthorizationKey(self, username):
        return self._api.generateAuthorizationKey(username=username)
    
    def sendResetPasswordLink(self,username):
        return self._api.sendResetPasswordLink(username=username)        

    def updatePassword(self,username,password=''):
        password=password or utils.random_string()
        return self._api.updatePassword(username=username, password=password)
