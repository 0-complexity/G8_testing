from framework.api import api_client

class Users:
    def __init__(self):
        self._api = api_client

    def get(username, password):
        return self._api.cloudapi.users.get(username=username)
        
    def authenticate(username, password):
        return self._api.cloudapi.users.authenticate(username=username, password=password)

    def getMatchingUsernames(usernameregex, limit):
        return self._api.cloudapi.users.getMatchingUsernames(usernameregex=usernameregex, limit=limit)
    
    def getResetPasswordInformation(resettoken):
        return self._api.cloudapi.users.getResetPasswordInformation(resettoken=resettoken)

    def isValidInviteUserToken(inviteusertoken, emailaddress):
        return self._api.cloudapi.users.authenticate(inviteusertoken=inviteusertoken, emailaddress=emailaddress)

    def registerInvitedUser(inviteusertoken, emailaddress, username, password, confirmpassword):
        return self._api.cloudapi.users.registerInvitedUser(
            inviteusertoken=inviteusertoken, 
            emailaddress=emailaddress,
            username=username,
            password=password,
            confirmpassword=confirmpassword
        )

    def resetPassword(resettoken, newpassword):
        return self._api.cloudapi.users.resetPassword(resettoken=resettoken, newpassword=newpassword)

    def sendResetPasswordLink(emailaddress):
        return self._api.cloudapi.users.sendResetPasswordLink(emailaddress=emailaddress)

    def setData(data):
        return self._api.cloudapi.users.setData(data=data)

    def updatePassword(data):
        return self._api.cloudapi.users.updatePassword(oldPassword=oldPassword, newPassword=newPassword)

    def validate(validationtoken, password):
        return self._api.cloudapi.users.validate(validationtoken=validationtoken, password=password)

    
