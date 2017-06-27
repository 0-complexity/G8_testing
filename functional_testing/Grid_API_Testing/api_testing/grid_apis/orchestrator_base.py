from zeroos.orchestrator import client as apiclient
from api_testing.grid_apis import JWT
from testconfig import config

class GridPyclientBase(object):
    def __init__(self):
        self.config = config['main']
        self.api_base_url = self.config['api_base_url']
        self.api_client = apiclient.APIClient(self.api_base_url)
        self.api_client.set_auth_header("Bearer %s" % JWT)