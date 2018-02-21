from framework.api import utils

class UserManager:
    def __init__(self, api_client):
        self._api = api_client

    def authenticate(self, username, password):
        return self._api.system.usermanager.authenticate(name=username, secret=password)

    def create(self, **kwargs):
        data = {
            'username': utils.random_string(),
            'password': utils.random_string(),
            'groups': ['admin'],
            'emails': [utils.random_string()],
            'domain': utils.random_string(),
            'provider': utils.random_string()
        }
        data.update(** kwargs)
        return data, self._api.cloudapi.usermanager.create(** data)

    def createGroup(self, **kwargs):
        data = {
            'name': utils.random_string(),
            'domain': utils.random_string(),
            'description': utils.random_string(),
        }
        data.update(** kwargs)
        return data, self._api.cloudapi.usermanager.createGroup(** data)

    def delete(self, username):
        return self._api.cloudapi.usermanager.delete(username=username)

    def deleteGroup(self, id):
        return self._api.cloudapi.usermanager.deleteGroup(id=id)

    def editGroup(self, name, **kwargs):
        data = {
            'name': name,
            'domain': utils.random_string(),
            'description': utils.random_string(),
            'users': []
        }
        data.update(** kwargs)
        return data, self._api.cloudapi.usermanager.editGroup(** data)

    def editUser(self, username, **kwargs):
        data = {
            'username': username,
            'domain': utils.random_string(),
            'password': utils.random_string(),
            'emails': [utils.random_string() + '@test.com'],
            'groups': ['admin']
        }
        data.update(** kwargs)
        return data, self._api.cloudapi.usermanager.editUser(** data)

    def userexists(self, name):
        return self._api.cloudapi.usermanager.userexists(name=name)

    def userget(self, name):
        return self._api.cloudapi.usermanager.userget(name=name)

    def whoami(self):
        return self._api.cloudapi.usermanager.whoami()