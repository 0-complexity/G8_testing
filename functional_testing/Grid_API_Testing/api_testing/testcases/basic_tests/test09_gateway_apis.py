from random import randint
import unittest, time
from api_testing.testcases.testcases_base import TestcasesBase
from api_testing.grid_apis.pyclient.bridges_apis import BridgesAPI
from api_testing.grid_apis.pyclient.containers_apis import ContainersAPI
from api_testing.grid_apis.pyclient.gateways_apis import GatewayAPI
from api_testing.utiles.core0_client import Client


class TestGatewayAPI(TestcasesBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bridges_apis = BridgesAPI()
        self.containers_apis = ContainersAPI()
        self.gateways_apis = GatewayAPI()

    def setUp(self):
        super(TestGatewayAPI, self).setUp()
        self.nodeid = self.get_random_node()
        self.lg.info('Get random nodeid : %s' % str(self.nodeid))
        pyclient_ip = [x['ip'] for x in self.nodes if x['id'] == self.nodeid]
        self.assertNotEqual(pyclient_ip, [])
        self.pyclient = Client(pyclient_ip[0])

        self.gwname = self.random_string()
        self.gwdomain = self.random_string()

        self.body = {
            "name":self.gwname,
            "domain":self.gwdomain,
            "nics":[
                {
                    'type':'default',
                    'name':'internet'
                }
            ],
            "portforwards":[],
            "httpproxies":[]
        }

        self.pyclient.create_ovs_container()
        response = self.gateways_apis.post_nodes_gateway(self.nodeid, self.body)
        self.assertEqual(response.status_code, 201)


    def tearDown(self):
        self.lg.info('Delete all node {} gateways'.format(self.nodeid))
        response = self.gateways_apis.list_nodes_gateways(self.nodeid)
        for gw in response.json():
            self.gateways_apis.delete_nodes_gateway(self.nodeid, gw['name'])

        super(TestGatewayAPI, self).tearDown()


    def test001_list_nodes_gateways(self):
        """ GAT-082
        **Test Scenario:**

        #. Get random node (N0), should succeed.
        #. Create gateway (GW0) on node (N0), should succeed.
        #. List all node (N0) gateways, (GW0) should be listed.
        """
        self.lg.info('List node (N0) gateways, (GW0) should be listed')
        response = self.gateways_apis.list_nodes_gateways(self.nodeid)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.gwname, [x['name'] for x in response.json()])


    def test002_get_gateway_info(self):
        """ GAT-083
        **Test Scenario:**

        #. Get random node (N0), should succeed.
        #. Create gateway (GW0) on node (N0), should succeed.
        #. Get gateway (GW0) info, should succeed.
        """
        response = self.gateways_apis.get_nodes_gateway(self.nodeid, self.gwname)
        self.assertEqual(response.status_code, 200)


    def test003_delete_gateway(self):
        """ GAT-084
        **Test Scenario:**

        #. Get random node (N0), should succeed.
        #. Create gateway (GW0) on node (N0), should succeed.
        #. Delete gateway (GW0), should succeed.
        #. List node (N0) gateways, (GW0) should not be listed.
        """

        self.lg.info('Delete gateway (GW0), should succeed')
        response = self.gateways_apis.delete_nodes_gateway(self.nodeid, self.gwname)
        self.assertEqual(response.status_code, 204)

        self.lg.info('List node (N0) gateways, (GW0) should not be listed')
        response = self.gateways_apis.list_nodes_gateways(self.nodeid)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.gwname, [x['name'] for x in response.json()])


    def test004_create_gateway(self):
        """ GAT-085
        **Test Scenario:**

        #. Get random node (N0), should succeed.
        #. Create gateway (GW0) on node (N0), should succeed.
        """
        pass


    def test005_update_gateway_info(self):
        """ GAT-086
        **Test Scenario:**

        #. Get random node (N0), should succeed.
        #. Create gateway (GW0) on node (N0), should succeed.
        #. Update gateway (GW0), should succeed.
        """
        pass