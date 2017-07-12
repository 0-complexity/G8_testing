from test_suite.orchestrator_objects.orchestrator_apis.bridges_apis import BridgesAPI
from test_suite.orchestrator_objects.orchestrator_apis.containers_apis import ContainersAPI
from test_suite.orchestrator_objects.orchestrator_apis.gateways_apis import GatewayAPI
from test_suite.orchestrator_objects.orchestrator_apis.nodes_apis import NodesAPI
from test_suite.orchestrator_objects.orchestrator_apis.storageclusters_apis import Storageclusters
from test_suite.orchestrator_objects.orchestrator_apis.storagepools_apis import StoragepoolsAPI
from test_suite.orchestrator_objects.orchestrator_apis.vms_apis import VmsAPI
from test_suite.orchestrator_objects.orchestrator_apis.vdisks_apis import VDisksAPIs
from test_suite.orchestrator_objects.orchestrator_apis.zerotiers_apis import ZerotiersAPI
from zeroos.orchestrator import client
from testconfig import config


class OrchasteratorDriver:
    api_base_url = config['main']['api_base_url']
    client_id = config['main']['client_id']
    client_secret = config['main']['client_secret']
    organization = config['main']['organization']
    zerotier_token = config['zerotier_token']

    def __init__(self):
        self.JWT = self.get_jwt()
        self.orchestrator_client = client.APIClient(self.api_base_url)
        self.orchestrator_client.set_auth_header("Bearer %s" % self.JWT)

        self.bridges_api = BridgesAPI(self.orchestrator_client)
        self.container_api = ContainersAPI(self.orchestrator_client)
        self.gateway_api = GatewayAPI(self.orchestrator_client)
        self.nodes_api = NodesAPI(self.orchestrator_client)
        self.storagepools_api = StoragepoolsAPI(self.orchestrator_client)
        self.storageclusters_api = Storageclusters(self.orchestrator_client)
        self.vdisks_api = VDisksAPIs(self.orchestrator_client)
        self.vms_api = VmsAPI(self.orchestrator_client)
        self.zerotiers_api = ZerotiersAPI(self.orchestrator_client)

        self.nodes_info = self.get_node_info()

    def get_jwt(self):
        auth = client.oauth2_client_itsyouonline.Oauth2ClientItsyouonline()
        response = auth.get_access_token(self.client_id, self.client_secret,
                                         scopes=['user:memberof:%s' % self.organization],
                                         audiences=[])
        return response.content.decode('utf-8')

    def get_node_info(self):
        nodes_info = []
        response = self.node_api.get_nodes()
        for node in response.json():
            if node['status'] == 'halted':
                continue
            nodes_info.append({"id": node['id'],
                               "ip": node['ipaddress'],
                               "status": node['status']})
        return nodes_info
