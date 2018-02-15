from framework.api.cloudapi.cloudapi import Cloudapi
from framework.api.system.system import System
from framework.api.libcloud.libcloud import Libcloud
from framework.api.cloudbroker.cloudbroker import Cloudbroker

class Client:
    def __init__(self):
        self.cloudapi = Cloudapi()
        self.cloudbroker = Cloudbroker()
        self.libcloud = Libcloud()
        self.system = System()
        


