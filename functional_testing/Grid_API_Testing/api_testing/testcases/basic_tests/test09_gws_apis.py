from api_testing.testcases.testcases_base import TestcasesBase
from api_testing.grid_apis.orchestrator_client.bridges_apis import BridgesAPI
from api_testing.grid_apis.orchestrator_client.containers_apis import ContainersAPI
from api_testing.grid_apis.orchestrator_client.gateways_apis import GatewayAPI
from api_testing.utiles.core0_client import Client
from random import randint


class TestGatewayAPICreation(TestcasesBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bridges_apis = BridgesAPI()
        self.containers_apis = ContainersAPI()
        self.gateways_apis = GatewayAPI()

    def setUp(self):
        super().setUp()
        self.nodeid = self.get_random_node()
        self.lg.info('Get random nodeid : %s' % str(self.nodeid))
        core0_ip = [x['ip'] for x in self.nodes if x['id'] == self.nodeid]
        self.assertNotEqual(core0_ip, [])
        self.core0_client = Client(core0_ip[0], password=self.jwt)
        self.core0_client.create_ovs_container()

    def tearDown(self):
        self.lg.info('Delete all node {} gateways'.format(self.nodeid))
        response = self.gateways_apis.list_nodes_gateways(self.nodeid)
        for gw in response.json():
            self.gateways_apis.delete_nodes_gateway(self.nodeid, gw['name'])
        super().tearDown()

    def test004_create_gateway_with_vlan_vlan_container(self):
        """ GAT-xxx
        **Test Scenario:**

        #. Get random node (N0), should succeed.
        #. Create gateway with vlan and vlan as nics on node (N0), should succeed.
        #. Bind a new container to vlan(1).
        #. Bind a new container to vlan(2).
        #. Make sure that those two containers can ping each others.
        """
        pass

    def test005_create_gateway_with_vxlan_vxlan_container(self):
        """ GAT-xxx
        **Test Scenario:**

        #. Get random node (N0), should succeed.
        #. Create gateway with vxlan and vxlan as nics on node (N0), should succeed.
        #. Bind a new container to vxlan(1).
        #. Bind a new container to vxlan(2).
        #. Make sure that those two containers can ping each others.
        """
        pass

    def test006_create_gateway_with_vlan_vlan_vm(self):
        """ GAT-xxx
        **Test Scenario:**

        #. Get random node (N0), should succeed.
        #. Create gateway with vlan and vlan as nics on node (N0), should succeed.
        #. Bind a new vm to vlan(1).
        #. Bind a new vm to vlan(2).
        #. Make sure that those two containers can ping each others.
        """
        pass

    def test007_create_gateway_with_vxlan_vxlan_vm(self):
        """ GAT-xxx
        **Test Scenario:**

        #. Get random node (N0), should succeed.
        #. Create gateway with vxlan and vxlan as nics on node (N0), should succeed.
        #. Bind a new vm to vxlan(1).
        #. Bind a new vm to vxlan(2).
        #. Make sure that those two containers can ping each others.
        """
        pass

    def test008_create_gateway_with_bridge_vlan_container(self):
        """ GAT-xxx
        **Test Scenario:**

        #. Get random node (N0), should succeed.
        #. Create gateway with bridge and vlan as nics on node (N0), should succeed.
        #. Bind a new container to vlan(1).
        #. Verify that this container has public access.
        """
        pass

    def test010_create_gateway_with_bridge_vxlan_container(self):
        """ GAT-xxx
        **Test Scenario:**

        #. Get random node (N0), should succeed.
        #. Create gateway with bridge and vlan as nics on node (N0), should succeed.
        #. Bind a new container to vxlan(1).
        #. Verify that this container has public access.
        """
        pass

    def test011_create_gateway_with_bridge_vlan_vm(self):
        """ GAT-xxx
        **Test Scenario:**

        #. Get random node (N0), should succeed.
        #. Create gateway with bridge and vlan as nics on node (N0), should succeed.
        #. Bind a new vm to vlan(1).
        #. Verify that this container has public access.
        """
        pass

    def test012_create_gateway_with_bridge_vxlan_vm(self):
        """ GAT-xxx
        **Test Scenario:**

        #. Get random node (N0), should succeed.
        #. Create gateway with bridge and vlan as nics on node (N0), should succeed.
        #. Bind a new vm to vxlan(1).
        #. Verify that this vm has public access.
        """
        pass

    def test013_create_gateway_dhcpserver(self):
        """ GAT-xxx
        **Test Scenario:**

        #. Get random node (N0), should succeed.
        #. Create gateway with bridge and vlan as nics on node (N0), should succeed.
        #. Specify a dhcpserver for container and vm in this GW
        #. Create a container and vm to match the dhcpserver specs
        #. Verify that container and vm ips are matching with the dhcpserver specs.
        """
        pass

    def test014_create_gateway_httpproxy(self):
        """ GAT-xxx
        **Test Scenario:**

        #. Get random node (N0), should succeed.
        #. Create gateway with bridge and vlan as nics and httpproxy with two containers on node (N0), should succeed.
        #. Create two containers to for test the httpproxy's configuration
        #. Verify that the httprxoy's configuration is working right
        """
        pass

    def test015_create_gateway_portforwards(self):
        """ GAT-xxx
        **Test Scenario:**

        #. Get random node (N0), should succeed.
        #. Create gateway with bridge and vlan as nics should succeed.
        #. Set a portforward form srcip:80 to destination:80
        #. Create one container as a destination host
        #. Start any service in this container
        #. Using core0_client try to request this service and make sure that u can reach the container
        """
        pass

    def test016_create_two_gateways_zerotierbridge(self):
        """ GAT-xxx
        **Test Scenario:**

        #. Get random node (N0), should succeed.
        #. Create two containers and link them with zerotier bridge.
        #. Verify that each containers' hosts can reach each others.
        """
        pass


class TestGatewayAPIUpdate(TestcasesBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bridges_apis = BridgesAPI()
        self.containers_apis = ContainersAPI()
        self.gateways_apis = GatewayAPI()

    def setUp(self):
        super().setUp()
        self.nodeid = self.get_random_node()
        self.lg.info('Get random nodeid : %s' % str(self.nodeid))
        core0_ip = [x['ip'] for x in self.nodes if x['id'] == self.nodeid]
        self.assertNotEqual(core0_ip, [])
        self.core0_client = Client(core0_ip[0])
        self.gw_name = self.random_string()
        self.gw_domain = self.random_string()

        self.public_vlan_id = randint(1, 4094)
        self.private_vxlan_id = randint(1, 100000)

        self.body = {
            "name": self.gw_name,
            "domain": self.gw_domain,
            "nics": [
                {
                    "name": "public",
                    "type": "vlan",
                    "id": self.public_vlan_id,
                    "config": {
                        "cidr": "192.168.1.10/24",
                        "gateway": "192.168.1.1"
                    }
                },

                {
                    "name": "private",
                    "type": "vxlan",
                    "id": self.private_vxlan_id,
                    "config": {
                        "cidr": "192.168.2.20/24"
                    }
                }
            ],
            "portforwards": [],
            "httpproxies": [],
            "dhcpserver": []
        }
        self.core0_client.create_ovs_container()
        response = self.gateways_apis.post_nodes_gateway(self.nodeid, self.body)
        self.assertEqual(response.status_code, 201)

    def tearDown(self):
        self.lg.info('Delete all node {} gateways'.format(self.nodeid))
        response = self.gateways_apis.list_nodes_gateways(self.nodeid)
        for gw in response.json():
            self.gateways_apis.delete_nodes_gateway(self.nodeid, gw['name'])
        super().tearDown()

    def test001_list_gateways(self):
        """ GAT-098
        **Test Scenario:**

        #. Get random node (N0), should succeed.
        #. Create gateway (GW0) on node (N0), should succeed.
        #. List all node (N0) gateways, (GW0) should be listed.
        """
        self.lg.info('List node (N0) gateways, (GW0) should be listed')
        response = self.gateways_apis.list_nodes_gateways(self.nodeid)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.gw_name, [x['name'] for x in response.json()])

    def test002_get_gateway_info(self):
        """ GAT-099
        **Test Scenario:**

        #. Get random node (N0), should succeed.
        #. Create gateway (GW0) on node (N0), should succeed.
        #. Get gateway (GW0) info, should succeed.
        """
        response = self.gateways_apis.get_nodes_gateway(self.nodeid, self.gw_name)
        self.assertEqual(response.status_code, 200)

    def test003_delete_gateway(self):
        """ GAT-100
        **Test Scenario:**

        #. Get random node (N0), should succeed.
        #. Create gateway (GW0) on node (N0), should succeed.
        #. Delete gateway (GW0), should succeed.
        #. List node (N0) gateways, (GW0) should not be listed.
        """

        self.lg.info('Delete gateway (GW0), should succeed')
        response = self.gateways_apis.delete_nodes_gateway(self.nodeid, self.gw_name)
        self.assertEqual(response.status_code, 204)

        self.lg.info('List node (N0) gateways, (GW0) should not be listed')
        response = self.gateways_apis.list_nodes_gateways(self.nodeid)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.gw_name, [x['name'] for x in response.json()])

    def test004_stop_gw(self):
        """ GAT-xxx
        **Test Scenario:**

        #. Stop the running gatway
        #. Verify its status
        """
        pass

    def test004_start_gw(self):
        """ GAT-xxx
        **Test Scenario:**

        #. Stop the running gatway and make sure that its status has been changed
        #. Start the gatway
        #. Verify its status
        """
        pass

    def test004_update_gw_nics_config(self):
        """ GAT-xxx
        **Test Scenario:**

        #. Use put method to update the nics config for the gw
        #. List the gw and make sure that its nics config have been updated
        """

    def test004_update_gw_portforwards_config(self):
        """ GAT-xxx
        **Test Scenario:**

        #. Use put method to update the portforwards config for the gw
        #. List the gw and make sure that its portforwards config have been updated
        """

    def test004_update_gw_dhcpserver_config(self):
        """ GAT-xxx
        **Test Scenario:**

        #. Use put method to update the dhcpserver config for the gw
        #. List the gw and make sure that its dhcpserver config have been updated
        """

    def test004_update_gw_httpproxies_config(self):
        """ GAT-xxx
        **Test Scenario:**

        #. Use put method to update the dhcpserver config for the gw
        #. List the gw and make sure that its dhcpserver config have been updated
        """

    def test_create_new_portforward(self):
        """ GAT-xxx
        **Test Scenario:**

        #. Create new portforward table using firewall/forwards api
        #. Verify it is working right
        """

    def test_list_portforward(self):
        """ GAT-xxx
        **Test Scenario:**

        #. Create new portforward table using firewall/forwards api
        #. List portfowards table
        #. Verify it has the right configuration
        """

    def test_delete_portforward(self):
        """ GAT-xxx
        **Test Scenario:**

        #. Create new portforward table using firewall/forwards api
        #. List portfowards table
        #. Delete this portforward config
        #. List portforwards
        #. Verify that it has been deleted
        """

    def test_add_dhcp_host(self):
        """ GAT-xxx
        **Test Scenario:**

        #. Add new dhcp host to an interface
        #. List dhcp hosts
        #. Verify that is the list has the config
        """

    def test_delete_dhcp_host(self):
        """ GAT-xxx
        **Test Scenario:**

        #. Add new dhcp host to an interface
        #. List dhcp hosts
        #. Delete one host form the dhcp
        #. List dhcp hosts
        #. Verify that the dhcp has been updated
        """


    def test_create_new_httpproxy(self):
        """ GAT-xxx
        **Test Scenario:**

        #. Create new httpproxy
        #. List httpproxy config
        #. Verify that is the list has the config
        """

    def test_delete_httpproxyid(self):
        """ GAT-xxx
        **Test Scenario:**

        #. Create new httpproxy
        #. List httpproxy config
        #. Delete httpproxy id
        #. List dhcp hosts
        #. Verify that the dhcp has been updated
        """
