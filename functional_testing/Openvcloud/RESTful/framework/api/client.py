from framework.api.cloudapi.cloudapi import Cloudapi
from framework.api.libcloud.libcloud import Libcloud
class Client:
    def __init__(self):
        self.cloudapi = Cloudapi()
        self.libcloud = Libcloud()


