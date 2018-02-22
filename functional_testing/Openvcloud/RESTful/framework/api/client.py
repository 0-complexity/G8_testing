from framework.api.cloudapi.cloudapi import Cloudapi
from framework.api.system.system import System
from framework.api.libcloud.libcloud import Libcloud
from framework.api.cloudbroker.cloudbroker import Cloudbroker
from testconfig import config
from framework.utils.ovc_client import Client as api_client
import random


class Client:
    def __init__(self):
        ip = config['main']['ip']
        port = int(config['main']['port'])
        client_id = config['main']['client_id']
        client_secret = config['main']['client_secret']
        self.api_client = api_client(ip, port, client_id, client_secret)
        self.api_client.load_swagger()
        self.cloudapi = Cloudapi(self.api_client)
        self.cloudbroker = Cloudbroker(self.api_client)
        self.libcloud = Libcloud(self.api_client)
        self.system = System(self.api_client)


    def set_auth_header(self, value):
        self.api_client._session.headers['Authorization'] = value

    def get_random_locations(self):
        return random.choice(self.cloudapi.locations.list())['locationCode']
