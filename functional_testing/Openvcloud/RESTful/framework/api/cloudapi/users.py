from framework.api import api_client

class Users:
    def __init__(self):
        self._api = api_client.cloudapi.users

    def get(username, password):
        return self._api.get(username=username)
        
    def authenticate(username, password):
        return self._api.authenticate(username=username, password=password)

    def getMatchingUsernames(usernameregex, limit):
        return self._api.getMatchingUsernames(usernameregex=usernameregex, limit=limit)
    
    def getResetPasswordInformation(resettoken):
        return self._api.getResetPasswordInformation(resettoken=resettoken)

    def isValidInviteUserToken(inviteusertoken, emailaddress):
        return self._api.authenticate(inviteusertoken=inviteusertoken, emailaddress=emailaddress)

    def registerInvitedUser(inviteusertoken, emailaddress, username, password, confirmpassword):
        return self._api.registerInvitedUser(
            inviteusertoken=inviteusertoken, 
            emailaddress=emailaddress,
            username=username,
            password=password,
            confirmpassword=confirmpassword
        )

    def resetPassword(resettoken, newpassword):
        return self._api.resetPassword(resettoken=resettoken, newpassword=newpassword)

    def sendResetPasswordLink(emailaddress):
        return self._api.sendResetPasswordLink(emailaddress=emailaddress)

    def setData(data):
        return self._api.setData(data=data)

    def updatePassword(data):
        return self._api.updatePassword(oldPassword=oldPassword, newPassword=newPassword)

    def validate(validationtoken, password):
        return self._api.validate(validationtoken=validationtoken, password=password)

    
