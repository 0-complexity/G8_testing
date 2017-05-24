from g8os import resourcepool
from testconfig import config


class GridPyclientBase(object):
    def __init__(self):
        self.config = config['main']
        self.api_base_url = self.config['api_base_url']
        client = resourcepool.Client(self.api_base_url)
        self.api_client = client.api
        