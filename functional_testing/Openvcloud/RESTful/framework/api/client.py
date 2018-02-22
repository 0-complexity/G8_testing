from framework.api.cloudapi.cloudapi import Cloudapi
from framework.api.system.system import System
from framework.api.libcloud.libcloud import Libcloud
from framework.api.cloudbroker.cloudbroker import Cloudbroker
from testconfig import config

class Client:
    def __init__(self):
        self.cloudapi = Cloudapi()
        self.cloudbroker = Cloudbroker()
        self.libcloud = Libcloud()
        self.system = System()
        self._whoami = config['main']['username']

    def create_account(self, **kwargs):
        data, response = self.cloudbroker.account.create(username=self._whoami, ** kwargs)

        if response.status_code != 200:
            return False

        account_id = int(response.text)
        return account_id
    
    def create_cloudspace(self, accountId, location, **kwargs):
        data, response = self.cloudapi.cloudspaces.create(accountId=accountId, location=location, access=self._whoami, **kwargs)

        if response.status_code != 200:
            return False

        cloudspace_id = int(response.text)
        return cloudspace_id
        


