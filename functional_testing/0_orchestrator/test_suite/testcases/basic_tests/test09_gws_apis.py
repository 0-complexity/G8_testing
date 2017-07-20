import random, time
from testcases.testcases_base import TestcasesBase
import unittest


class TestGatewayAPICreation(TestcasesBase):
    def setUp(self):
        super().setUp()
        self.core0_client.create_ovs_container()
        self.flist = 'https://hub.gig.tech/gig-official-apps/ubuntu1604.flist'
        self.container_body = {"name": self.rand_str(),
                               "hostname": self.rand_str(),
                               "flist": self.flist}

    def tearDown(self):
        self.lg.info(' [*] Delete all created {} gateways'.format(self.nodeid))
        for gw in self.gateways_api.createdGw:
            self.gateways_api.delete_nodes_gateway(gw['node'], gw['name'])

        self.lg.info(' [*] TearDown:delete all created container ')
        for container in self.containers_api.createdcontainer:
            self.containers_api.delete_containers_containerid(container['node'],
                                                              container['name'])

        self.lg.info(' [*] TearDown:delete all created bridges ')
        for bridge in self.bridges_api.createdbridges:
            self.bridges_api.delete_nodes_bridges_bridgeid(bridge['node'],
                                                           bridge['name'])
        super().tearDown()

    def create_vm(self, nics):
        response = self.storageclusters_api.get_storageclusters()
        self.assertEqual(response.status_code, 200)
        storageclusters = response.json()
        if storageclusters:
            storagecluster = storageclusters[-1]
        else:
            free_disks = self.core0_client.getFreeDisks()
            if free_disks == []:
                self.skipTest(' [*] no free disks to create storagecluster.')
            self.lg.info(' [*] Deploy new storage cluster (SC0).')
            response, data = self.storageclusters_api.post_storageclusters(node_id=self.nodeid)
            self.assertEqual(response.status_code, 201)
            storagecluster = data['label']

        self.lg.info(' [*] Create new vdisk.')
        response, data = self.vdisks_api.post_vdisks(storagecluster=storagecluster, size=15, blocksize=4096,
                                                     type='boot',
                                                     templatevdisk="ardb://hub.gig.tech:16379/template:ubuntu-1604")

        boot_disk = data['id']

        self.lg.info(' [*] Create virtual machine (VM0) on node (N0)')
        disks = [{"vdiskid": boot_disk, "maxIOps": 2000}]
        response, data = self.vms_api.post_nodes_vms(node_id=self.nodeid, memory=1024, cpu=1, nics=nics, disks=disks)
        self.assertEqual(response.status_code, 201)
        return data

    def test001_create_gateway_with_Xlan_Xlan_container(self):
        """ GAT-123
        **Test Scenario:**

        #. Get random node (N0), should succeed.
        #. Create gateway with Xlan and Xlan as nics on node (N0), should succeed.
        #. Bind a new container to Xlan(1).
        #. Bind a new container to Xlan(2).
        #. Make sure that those two containers can ping each others.
        """
        self.lg.info(' [*] Create gateway with vlan and vlan as nics on node (N0), should succeed')
        nics_type = [{
            'type': random.choice['vlan', 'vxlan'],
            'gateway': True,
            'dhcp': False,
            'bridge_name': ''

        },
            {
                'type': random.choice['vlan', 'vxlan'],
                'gateway': False,
                'dhcp': False,
                'bridge_name': ''

            },
            {
                'type': random.choice['vlan', 'vxlan'],
                'gateway': False,
                'dhcp': False,
                'bridge_name': ''

            }
        ]

        nics = self.get_gateway_nic(nics_types=nics_type)
        response, data = self.gateways_api.post_nodes_gateway(self.nodeid, nics=nics)
        self.assertEqual(response.status_code, 201)

        self.lg.info(' [*] Bind a new container to vlan(1)')
        nics_container = [{'type': nics[1]['type'],
                           'id': nics[1]['id'],
                           'config': {'dhcp': False,
                                      'gateway': nics[1]['config']['cidr'][-3],
                                      'cidr': nics[1]['config']['cidr'][-4] + '10/24'}
                           }]
        uid = self.core0_client.client.container.create(self.flist, nics=nics_container).get().data
        container_1 = self.core0_client.client.container.client(int(uid))

        self.lg.info(' [*] Bind a new container to vlan(2)')
        nics_container = [{'type': nics[2]['type'],
                           'id': nics[2]['id'],
                           'config': {'dhcp': False,
                                      'gateway': nics[2]['config']['cidr'][-3],
                                      'cidr': nics[2]['config']['cidr'][-4] + '10/24'}
                           }]
        uid = self.core0_client.client.container.create(self.flist, nics=nics_container).get().data
        container_2 = self.core0_client.client.container.client(int(uid))

        self.lg.info(' [*] Make sure that those two containers can ping each others')
        response = container_1.bash('ping -w5 %s' % nics[2]['config']['cidr'][-4] + '10').get()
        self.assertEqual(response.state, 'SUCCESS')
        response = container_2.bash('ping -w5 %s' % nics[1]['config']['cidr'][-4] + '10').get()
        self.assertEqual(response.state, 'SUCCESS')

    @unittest.skip('testcase untested')
    def test003_create_gateway_with_vlan_vlan_vm(self):
        """ GAT-125
        **Test Scenario:**

        #. Get random node (N0), should succeed.
        #. Create gateway with vlan and vlan as nics on node (N0), should succeed.
        #. Bind a new vm to vlan(1).
        #. Bind a new vm to vlan(2).
        #. Make sure that those two containers can ping each others.
        """
        vm1_mac_addr = self.randomMAC()
        vm2_mac_addr = self.randomMAC()
        test_container_mac_addr = self.randomMAC()

        body = {
            "name": "vm_gw_2",
            "domain": "vm_gw_2",
            "nics": [
                {
                    "name": "public",
                    "type": "vlan",
                    "id": "0",
                    "config": {
                        "cidr": "192.168.10.1/24",
                        "gateway": "192.168.10.2"
                    }
                },
                {
                    "name": "private_1",
                    "type": "vlan",
                    "id": "1",
                    "config": {
                        "cidr": "192.168.20.1/24"
                    },
                    "dhcpserver": {
                        "nameservers": [
                            "8.8.8.8"
                        ],
                        "hosts": [
                            {
                                "macaddress": test_container_mac_addr,
                                "hostname": "test-container",
                                "ipaddress": "192.168.20.5"
                            },
                            {
                                "macaddress": vm1_mac_addr,
                                "hostname": "vm1",
                                "ipaddress": "192.168.20.2"
                            }
                        ]
                    }
                },
                {
                    "name": "private_2",
                    "type": "vlan",
                    "id": "2",
                    "config": {
                        "cidr": "192.168.30.1/24"
                    },
                    "dhcpserver": {
                        "nameservers": [
                            "8.8.8.8"
                        ],
                        "hosts": [
                            {
                                "macaddress": test_container_mac_addr,
                                "hostname": "test-container",
                                "ipaddress": "192.168.30.5"
                            },
                            {
                                "macaddress": vm2_mac_addr,
                                "hostname": "vm2",
                                "ipaddress": "192.168.30.2"
                            }
                        ]
                    }
                }
            ]
        }

        nics = [{'id': '1', 'type': 'vlan', 'macaddress': vm1_mac_addr}]
        vm1 = self.create_vm(nics=nics)

        nics = [{'id': '2', 'type': 'vlan', 'macaddress': vm2_mac_addr}]
        vm2 = self.create_vm(nics=nics)

        self.lg.info(' [*] create test container')

        nics = [{'type': 'vlan', 'id': "1", 'config': {'dhcp': True}, 'hwaddr': test_container_mac_addr},
                {'type': 'vlan', 'id': "2", 'config': {'dhcp': True}, 'hwaddr': test_container_mac_addr}]

        uid = self.core0_client.client.container.create(self.flist, nics=nics).get()
        test_container = self.core0_client.client.container.client(uid)

        test_container.bash('apt install ssh -y; apt install sshpass -y')
        sleep(60)

        response = test_container_client.bash('ssh gig@192.168.20.2 -oStrictHostKeyChecking=no ping 192.168.30.2').get()
        self.assertEqual(response.state, 'SUCCESS')

        response = test_container_client.bash('ssh gig@192.168.30.2 -oStrictHostKeyChecking=no ping 192.168.20.2').get()
        self.assertEqual(response.state, 'SUCCESS')

    @unittest.skip('testcase untested')
    def test004_create_gateway_with_vxlan_vxlan_vm(self):
        """ GAT-126
        **Test Scenario:**

        #. Get random node (N0), should succeed.
        #. Create gateway with vxlan and vxlan as nics on node (N0), should succeed.
        #. Bind a new vm to vxlan(1).
        #. Bind a new vm to vxlan(2).
        #. Make sure that those two containers can ping each others.
        """
        vm1_mac_addr = self.randomMAC()
        vm2_mac_addr = self.randomMAC()
        test_container_mac_addr = self.randomMAC()

        body = {
            "name": "vm_gw_2",
            "domain": "vm_gw_2",
            "nics": [
                {
                    "name": "public",
                    "type": "vlan",
                    "id": "0",
                    "config": {
                        "cidr": "192.168.10.1/24",
                        "gateway": "192.168.10.2"
                    }
                },
                {
                    "name": "private_1",
                    "type": "vxlan",
                    "id": "1",
                    "config": {
                        "cidr": "192.168.20.1/24"
                    },
                    "dhcpserver": {
                        "nameservers": [
                            "8.8.8.8"
                        ],
                        "hosts": [
                            {
                                "macaddress": test_container_mac_addr,
                                "hostname": "test-container",
                                "ipaddress": "192.168.20.5"
                            },
                            {
                                "macaddress": vm1_mac_addr,
                                "hostname": "vm1",
                                "ipaddress": "192.168.20.2"
                            }
                        ]
                    }
                },
                {
                    "name": "private_2",
                    "type": "vxlan",
                    "id": "2",
                    "config": {
                        "cidr": "192.168.30.1/24"
                    },
                    "dhcpserver": {
                        "nameservers": [
                            "8.8.8.8"
                        ],
                        "hosts": [
                            {
                                "macaddress": test_container_mac_addr,
                                "hostname": "test-container",
                                "ipaddress": "192.168.30.5"
                            },
                            {
                                "macaddress": vm2_mac_addr,
                                "hostname": "vm2",
                                "ipaddress": "192.168.30.2"
                            }
                        ]
                    }
                }
            ]
        }

        nics = [{'id': '1', 'type': 'vxlan', 'macaddress': vm1_mac_addr}]
        vm1 = self.create_vm(nics=nics)

        nics = [{'id': '2', 'type': 'vxlan', 'macaddress': vm2_mac_addr}]
        vm2 = self.create_vm(nics=nics)

        self.lg.info(' [*] create test container')

        nics = [{'type': 'vxlan', 'id': "1", 'config': {'dhcp': True}, 'hwaddr': test_container_mac_addr},
                {'type': 'vxlan', 'id': "2", 'config': {'dhcp': True}, 'hwaddr': test_container_mac_addr}]

        uid = self.core0_client.client.container.create(self.flist, nics=nics).get()
        test_container = self.core0_client.client.container.client(uid)

        test_container.bash('apt install ssh -y; apt install sshpass -y')
        sleep(60)

        response = test_container_client.bash('ssh gig@192.168.20.2 -oStrictHostKeyChecking=no ping 192.168.30.2').get()
        self.assertEqual(response.state, 'SUCCESS')

        response = test_container_client.bash('ssh gig@192.168.30.2 -oStrictHostKeyChecking=no ping 192.168.20.2').get()
        self.assertEqual(response.state, 'SUCCESS')

    def test005_create_gateway_with_bridge_Xlan_container(self):
        """ GAT-127
        **Test Scenario:**

        #. Get random node (N0), should succeed.
        #. Create gateway with bridge and Xlan as nics on node (N0), should succeed.
        #. Bind a new container to Xlan(1).
        #. Verify that this container has public access.
        """
        self.lg.info(' [*] Create bridge (B1) on node (N0), should succeed with 201')
        response, data = self.bridges_api.post_nodes_bridges(self.nodeid, networkMode='static', nat=True)
        self.assertEqual(response.status_code, 201, response.content)
        time.sleep(3)

        nics_type = [{
            'type': 'bridge',
            'gateway': True,
            'dhcp': False,
            'bridge_name': data['name']

        },
            {
                'type': random.choice['vlan', 'vxlan'],
                'gateway': False,
                'dhcp': True,
                'bridge_name': ''

            }
        ]

        nics = self.get_gateway_nic(nics_types=nics_type)
        response, data = self.gateways_api.post_nodes_gateway(self.nodeid, nics=nics)
        self.assertEqual(response.status_code, 201)

        self.lg.info(' [*] Create container')
        self.core0_client.create_ovs_container()
        nics_container = [{"type": nics[1]['type'],
                           "id": nics[1]['id'],
                           "hwaddr": nics[1]['dhcpserver']['hosts'][0]['macaddress'],
                           "config": {"dhcp": True}}]

        response, data = self.containers_api.post_containers(self.nodeid, nics=nics_container)
        self.assertEqual(response.status_code, 201, " [*] Can't create container.")
        container = self.core0_client.get_container_client(data['name'])
        self.assertTrue(container)
        response = container.bash('ping -c 5 google.com').get()
        self.assertEqual(response.state, 'SUCCESS')
        self.assertNotIn("unreachable", response.stdout)

    @unittest.skip('testcase untested')
    def test007_create_gateway_with_bridge_vlan_vm(self):
        """ GAT-129
        **Test Scenario:**

        #. Get random node (N0), should succeed.
        #. Create gateway with bridge and vlan as nics on node (N0), should succeed.
        #. Bind a new vm to vlan(1).
        #. Verify that this vm has public access.
        """
        vm1_mac_addr = self.randomMAC()
        vm2_mac_addr = self.randomMAC()
        test_container_mac_addr = self.randomMAC()

        body = {
            "name": "vm_gw_2",
            "domain": "vm_gw_2",
            "nics": [
                {
                    "name": "public",
                    "type": "vlan",
                    "id": "0",
                    "config": {
                        "cidr": "192.168.10.1/24",
                        "gateway": "192.168.10.2"
                    }
                },
                {
                    "name": "private_1",
                    "type": "vlan",
                    "id": "1",
                    "config": {
                        "cidr": "192.168.20.1/24"
                    },
                    "dhcpserver": {
                        "nameservers": [
                            "8.8.8.8"
                        ],
                        "hosts": [
                            {
                                "macaddress": test_container_mac_addr,
                                "hostname": "test-container",
                                "ipaddress": "192.168.20.5"
                            },
                            {
                                "macaddress": vm1_mac_addr,
                                "hostname": "vm1",
                                "ipaddress": "192.168.20.2"
                            }
                        ]
                    }
                }
            ]
        }

        nics = [{'id': '1', 'type': 'vlan', 'macaddress': vm1_mac_addr}]
        vm1 = self.create_vm(nics=nics)

        self.lg.info(' [*] create test container')
        nics = [{'type': 'vlan', 'id': "1", 'config': {'dhcp': True}, 'hwaddr': test_container_mac_addr}]
        uid = self.core0_client.client.container.create(self.flist, nics=nics).get()
        test_container = self.core0_client.client.container.client(uid)

        test_container.bash('apt install ssh -y; apt install sshpass -y')
        sleep(60)

        response = test_container_client.bash('ssh gig@192.168.20.2 -oStrictHostKeyChecking=no ping -w3 8.8.8.8').get()
        self.assertEqual(response.state, 'SUCCESS')

    @unittest.skip('testcase untested')
    def test008_create_gateway_with_bridge_vxlan_vm(self):
        """ GAT-130
        **Test Scenario:**

        #. Get random node (N0), should succeed.
        #. Create gateway with bridge and vlan as nics on node (N0), should succeed.
        #. Bind a new vm to vxlan(1).
        #. Verify that this vm has public access.
        """
        vm1_mac_addr = self.randomMAC()
        vm2_mac_addr = self.randomMAC()
        test_container_mac_addr = self.randomMAC()

        body = {
            "name": "vm_gw_2",
            "domain": "vm_gw_2",
            "nics": [
                {
                    "name": "public",
                    "type": "vxlan",
                    "id": "0",
                    "config": {
                        "cidr": "192.168.10.1/24",
                        "gateway": "192.168.10.2"
                    }
                },
                {
                    "name": "private_1",
                    "type": "vxlan",
                    "id": "1",
                    "config": {
                        "cidr": "192.168.20.1/24"
                    },
                    "dhcpserver": {
                        "nameservers": [
                            "8.8.8.8"
                        ],
                        "hosts": [
                            {
                                "macaddress": test_container_mac_addr,
                                "hostname": "test-container",
                                "ipaddress": "192.168.20.5"
                            },
                            {
                                "macaddress": vm1_mac_addr,
                                "hostname": "vm1",
                                "ipaddress": "192.168.20.2"
                            }
                        ]
                    }
                }
            ]
        }

        nics = [{'id': '1', 'type': 'vxlan', 'macaddress': vm1_mac_addr}]
        vm1 = self.create_vm(nics=nics)

        self.lg.info(' [*] create test container')
        nics = [{'type': 'vxlan', 'id': "1", 'config': {'dhcp': True}, 'hwaddr': test_container_mac_addr}]
        uid = self.core0_client.client.container.create(self.flist, nics=nics).get()
        test_container = self.core0_client.client.container.client(uid)

        test_container.bash('apt install ssh -y; apt install sshpass -y')
        sleep(60)

        response = test_container_client.bash('ssh gig@192.168.20.2 -oStrictHostKeyChecking=no ping -w3 8.8.8.8').get()
        self.assertEqual(response.state, 'SUCCESS')

    def test009_create_gateway_dhcpserver(self):
        """ GAT-131
        **Test Scenario:**

        #. Get random node (N0), should succeed.
        #. Create gateway with bridge and xlan as nics on node (N0), should succeed.
        #. Specify a dhcpserver for container and vm in this GW
        #. Create a container and vm to match the dhcpserver specs
        #. Verify that container and vm ips are matching with the dhcpserver specs.
        """
        self.lg.info(' [*] Create bridge (B1) on node (N0), should succeed with 201')
        response, data = self.bridges_api.post_nodes_bridges(self.nodeid, networkMode='static', nat=True)
        self.assertEqual(response.status_code, 201, response.content)
        time.sleep(3)

        nics_type = [{
            'type': 'bridge',
            'gateway': True,
            'dhcp': False,
            'bridge_name': data['name']

        },
            {
                'type': random.choice(['vlan', 'vxlan']),
                'gateway': False,
                'dhcp': True,
                'bridge_name': ''

            }
        ]
        nics = self.get_gateway_nic(nics_types=nics_type)
        response, data = self.gateways_api.post_nodes_gateway(node_id=self.nodeid, nics=nics)
        self.assertEqual(response.status_code, 201, response.content)

        nics_container = [{
            'type': 'vlan',
            'id': nics[1]['id'],
            'hwaddr': nics[1]['dhcpserver'][0]['macaddress'],
            'config': {'dhcp': True}
        }]

        uid = self.core0_client.client.container.create(self.flist, nics=nics_container).get().data
        container_1 = self.core0_client.client.container.client(int(uid))
        container_1_nics = container_1.info.nic()
        interface = [x for x in container_1_nics if x['name'] == 'eth0']
        self.assertNotEqual(interface, [])
        self.assertIn(nics[1]['dhcpserver'][0]['ipaddress'], [x['addr'][:-3] for x in interface[0]['addrs']])
        self.assertEqual(nics[1]['dhcpserver'][0]['macaddress'], interface[0]['hardwareaddr'])

    def test010_create_gateway_httpproxy(self):
        """ GAT-132
        **Test Scenario:**

        #. Get random node (N0), should succeed.
        #. Create gateway with bridge and vlan as nics and httpproxy with two containers on node (N0), should succeed.
        #. Create two containers to for test the httpproxy's configuration
        #. Verify that the httprxoy's configuration is working right
        """
        self.lg.info(' [*] Create bridge (B1) on node (N0), should succeed with 201')
        response, data = self.bridges_api.post_nodes_bridges(self.nodeid, networkMode='static', nat=True)
        self.assertEqual(response.status_code, 201, response.content)
        time.sleep(3)

        nics_type = [{
            'type': 'bridge',
            'gateway': True,
            'dhcp': False,
            'bridge_name': data['name']

        },
            {
                'type': random.choice(['vlan', 'vxlan']),
                'gateway': False,
                'dhcp': True,
                'bridge_name': ''

            }
        ]
        nics = self.get_gateway_nic(nics_types=nics_type)
        httpproxies = [
            {
                "host": "container1",
                "destinations": ['http://{}:1000'.format(nics[1]['config']['cidr'][-4] + '10/24')],
                "types": ['http', 'https']
            },
            {
                "host": "container2",
                "destinations": ['http://{}:2000'.format(nics[1]['config']['cidr'][-4] + '20/24')],
                "types": ['http', 'https']
            }
        ]

        response, data = self.gateways_api.post_nodes_gateway(node_id=self.nodeid, nics=nics, httpproxies=httpproxies)
        self.assertEqual(response.status_code, 201, response.content)

        nics = [{'type': nics_type[1]['type'],
                 'id': nics['1']['id'],
                 'config': {'dhcp': False,
                            'gateway': nics[1]['config']['cidr'][-3],
                            'cidr': nics[1]['config']['cidr'][-4] + '10/24'}}]
        uid = self.core0_client.client.container.create(self.flist, nics=nics).get().data
        container_1 = self.core0_client.client.container.client(int(uid))

        nics = [{'type': nics_type[1]['type'],
                 'id': nics[1]['id'],
                 'config': {'dhcp': False,
                            'gateway': nics[1]['config']['cidr'][-3],
                            'cidr': nics[1]['config']['cidr'][-4] + '20/24'}}]
        uid = self.core0_client.client.container.create(self.flist, nics=nics).get().data
        container_2 = self.core0_client.client.container.client(int(uid))

        self.lg.info('Make sure that those two containers can ping each others')
        container_1.bash('python3 -m http.server 1000')
        container_2.bash('python3 -m http.server 2000')

        time.sleep(2)

        response = container_1.bash(
            'python3 -c "from urllib.request import urlopen; urlopen(\'{}\')"'.format('container2')).get()
        self.assertEqual(response.state, 'SUCCESS')

        response = container_2.bash(
            'python3 -c "from urllib.request import urlopen; urlopen(\'{}\')"'.format('container1')).get()
        self.assertEqual(response.state, 'SUCCESS')

    def test011_create_gateway_portforwards(self):
        """ GAT-133
        **Test Scenario:**

        #. Get random node (N0), should succeed.
        #. Create bridge(B0) , should succeed.
        #. Create gateway with bridge and vlan as nics should succeed.
        #. Set a portforward form srcip:80 to destination:80
        #. Create one container as a destination host
        #. Start any service in this container
        #. Using core0_client try to request this service and make sure that u can reach the container

        """
        self.lg.info(' [*] Create bridge (B1) on node (N0), should succeed with 201')
        response, data = self.bridges_api.post_nodes_bridges(self.nodeid, networkMode='static', nat=True)
        self.assertEqual(response.status_code, 201, response.content)
        time.sleep(3)
        
        self.lg.info(" [*] Create gateway with bridge and vlan as nics should succeed.")
        self.lg.info(" [*]  & Set a portforward form srcip:80 to destination:80")
        nics_type = [{
            'type': 'bridge',
            'gateway': True,
            'dhcp': False,
            'bridge_name': data['name']

        },
            {
                'type': random.choice(['vlan', 'vxlan']),
                'gateway': False,
                'dhcp': True,
                'bridge_name': ''

            }
        ]
        nics = self.get_gateway_nic(nics_types=nics_type)
        C_hw = self.randomMAC()
        portforwards = [
                {
                    "srcport": 80,
                    "srcip": nics[0]['config']['cidr'][-3],
                    "dstport": 80,
                    "dstip": nics[1]['dhcpserver']['hosts']['ipaddress'],
                    "protocols": [
                        "tcp"
                    ]
                }
            ]

        response, data = self.gateways_api.post_nodes_gateway(node_id=self.nodeid, nics=nics, portforwards=portforwards)
        self.assertEqual(response.status_code, 201, response.content)

        self.lg.info(' [*] Create container')
        self.core0_client.create_ovs_container()
        nics_container = [{"type": nics[1]['type'],
                           "id": nics[1]['id'],
                           "hwaddr": nics[1]['dhcpserver']['hosts'][0]['macaddress'],
                           "config": {"dhcp": True}}]

        response, data = self.containers_api.post_containers(self.nodeid, nics=nics_container)
        self.assertEqual(response.status_code, 201, " [*] Can't create container.")
        container = self.core0_client.get_container_client(data['name'])
        self.assertTrue(container)

        self.lg.info(" [*] Start any service in this container")
        file_name = self.rand_str()
        response = container.bash("mkdir {0} && cd {0}&& touch {0}.text ".format(file_name)).get()
        self.assertEqual(response.state, "SUCCESS")

        container.bash("cd %s &&  python3 -m http.server %s & " % (file_name, 80))
        time.sleep(3)

        self.lg.info(" [*] Using core0_client try to request this service and make sure that u can reach the container")
        response = container.bash("netstat -nlapt | grep %s" % 80).get()
        self.assertEqual(response.state, 'SUCCESS')
        url = ' http://{0}:{1}/{2}.text'.format(nics[0]['config']['cidr'][-3], 80, file_name)

        response = self.core0_client.client.bash('wget %s' % url).get()
        self.assertEqual(response.state, "SUCCESS")

        response = self.core0_client.client.bash('ls | grep %s.text' % file_name).get()
        self.assertEqual(response.state, "SUCCESS")

        response = self.core0_client.client.bash('rm %s.text' % file_name).get()
        self.assertEqual(response.state, "SUCCESS")

    def test012_create_two_gateways_zerotierbridge(self):
        """ GAT-134
        **Test Scenario:**

        #. Get random node (N0), should succeed.
        #. Create bridge(B0) with true nat, should succeed.
        #. Create zerotier network.
        #. Create two Gws (Gw1)(Gw2) and link them with zerotier bridge.
        #. Create (C1),(C2) containers for each Gw .
        #. Verify that each created 'GW containers' hosts can reach each others.

        """
        self.lg.info(" [*]  Create bridge(B0) with true nat, should succeed. ")
        B0_name = self.rand_str()
        B0_ip = "192.168.5.1"
        body = {"name": B0_name,
                "hwaddr": self.randomMAC(),
                "networkMode": "static",
                "nat": True,
                "setting": {"cidr": "%s/24" % B0_ip}
                }
        response = self.bridges_api.post_nodes_bridges(self.nodeid, body)
        self.assertEqual(response.status_code, 201, response.content)

        self.lg.info(" [*] Create zerotier network.")
        nwid = self.create_zerotier_network()

        self.lg.info(" [*]  Create two Gws and link them with zerotier bridge.")
        vlan1_id, vlan2_id = random.sample(range(1, 4096), 2)
        gw_domain = self.random_string()

        Gw1_name = self.rand_str()
        vlan1_cidr = "202.200.2.1/24"
        C1_ip = "202.200.2.2"
        C1_HW = self.randomMAC()
        Gw1_body = {
            "name": Gw1_name,
            "domain": gw_domain,
            "nics": [
                {
                    "name": 'public',
                    "type": 'bridge',
                    "id": B0_name,
                    "config": {"cidr": "192.168.5.2/24", "gateway": B0_ip}
                },
                {
                    "name": "vlan_1",
                    "type": "vlan",
                    "id": str(vlan1_id),
                    "config": {"cidr": vlan1_cidr},
                    "dhcpserver": {
                        "nameservers": [
                            "8.8.8.8"
                        ],
                        "hosts": [
                            {
                                "hostname": "test",
                                "macaddress": C1_HW,
                                "ipaddress": C1_ip
                            }
                        ]
                    },
                    "zerotierbridge": {"id": nwid, "token": self.zerotier_token}
                }
            ]
        }
        response = self.gateways_api.post_nodes_gateway(self.nodeid, Gw1_body)
        self.assertEqual(response.status_code, 201, response.content)

        C2_HW = self.randomMAC()
        Gw2_name = self.rand_str()
        vlan2_cidr = "202.200.2.3/24"
        C2_ip = "202.200.2.4"
        Gw2_body = {
            "name": Gw2_name,
            "domain": gw_domain,
            "nics": [
                {
                    "name": 'public',
                    "type": 'bridge',
                    "id": B0_name,
                    "config": {"cidr": '192.168.5.3/24', "gateway": B0_ip}
                },
                {
                    "name": 'vlan_2',
                    "type": 'vlan',
                    "id": str(vlan2_id),
                    "config": {"cidr": vlan2_cidr},
                    "dhcpserver": {
                        "nameservers": [
                            "8.8.8.8"
                        ],
                        "hosts": [
                            {
                                "hostname": "test",
                                "macaddress": C2_HW,
                                "ipaddress": C2_ip
                            }
                        ]
                    },
                    "zerotierbridge": {"id": nwid, "token": self.zerotier_token}
                }
            ]
        }

        response = self.gateways_api.post_nodes_gateway(self.nodeid, Gw2_body)
        self.assertEqual(response.status_code, 201)

        self.lg.info(" [*]  create (c1),(c2) containers for each Gw. ")
        C1_name = self.rand_str()
        C1_nics = [{'type': 'vlan', 'id': str(vlan1_id), "hwaddr": C1_HW, 'config': {"dhcp": True}}]
        self.container_body["nics"] = C1_nics
        self.container_body["name"] = C1_name
        response = self.containers_api.post_containers(self.nodeid, self.container_body)
        self.assertEqual(response.status_code, 201)
        C1_client = self.core0_client.get_container_client(C1_name)

        C2_name = self.rand_str()
        C2_nics = [{'type': 'vlan', 'id': str(vlan2_id), "hwaddr": C2_HW, 'config': {"dhcp": True}}]
        self.container_body["nics"] = C2_nics
        self.container_body["name"] = C2_name
        response = self.containers_api.post_containers(self.nodeid, self.container_body)
        self.assertEqual(response.status_code, 201)

        C1_client = self.core0_client.get_container_client(C1_name)
        C2_client = self.core0_client.get_container_client(C2_name)
        self.assertTrue(C1_client)
        self.assertTrue(C2_client)

        response = C1_client.bash('ping -c 5 %s' % C2_ip).get()
        self.assertEqual(response.state, 'SUCCESS')
        self.assertNotIn("unreachable", response.stdout)

        response = C2_client.bash('ping -c 5 %s' % C1_ip).get()
        self.assertEqual(response.state, 'SUCCESS')
        self.assertNotIn("unreachable", response.stdout)


class TestGatewayAPIUpdate(TestcasesBase):
    def setUp(self):
        super().setUp()
        self.gw_name = self.random_string()
        self.gw_domain = self.random_string()

        self.public_vlan_id = str(random.randint(1, 4094))
        self.private_vxlan_id = str(random.randint(1, 100000))

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
                    },
                    "dhcpserver": {
                        "nameservers": ["8.8.8.8"],
                        "hosts": [
                            {
                                "hostname": "aaaa",
                                "macaddress": "00:00:00:00:00:00",
                                "ipaddress": "192.168.2.10"
                            }
                        ]
                    }
                }
            ]
        }

        self.core0_client.create_ovs_container()
        response = self.gateways_api.post_nodes_gateway(self.nodeid, self.body)
        self.assertEqual(response.status_code, 201)

    def tearDown(self):
        self.lg.info(' [*] Delete all node {} gateways'.format(self.nodeid))
        response = self.gateways_api.list_nodes_gateways(self.nodeid)
        self.assertEqual(response.status_code, 200)
        for gw in response.json():
            self.gateways_api.delete_nodes_gateway(self.nodeid, gw['name'])
        super().tearDown()

    def test001_list_gateways(self):
        """ GAT-098
        **Test Scenario:**

        #. Get random node (N0), should succeed.
        #. Create gateway (GW0) on node (N0), should succeed.
        #. List all node (N0) gateways, (GW0) should be listed.
        """
        self.lg.info(' [*] List node (N0) gateways, (GW0) should be listed')
        response = self.gateways_api.list_nodes_gateways(self.nodeid)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.gw_name, [x['name'] for x in response.json()])

    def test002_get_gateway_info(self):
        """ GAT-099
        **Test Scenario:**

        #. Get random node (N0), should succeed.
        #. Create gateway (GW0) on node (N0), should succeed.
        #. Get gateway (GW0) info, should succeed.
        """
        response = self.gateways_api.get_nodes_gateway(self.nodeid, self.gw_name)
        self.assertEqual(response.status_code, 200)

    def test003_delete_gateway(self):
        """ GAT-100
        **Test Scenario:**

        #. Get random node (N0), should succeed.
        #. Create gateway (GW0) on node (N0), should succeed.
        #. Delete gateway (GW0), should succeed.
        #. List node (N0) gateways, (GW0) should not be listed.
        """

        self.lg.info(' [*] Delete gateway (GW0), should succeed')
        response = self.gateways_api.delete_nodes_gateway(self.nodeid, self.gw_name)
        self.assertEqual(response.status_code, 204)

        self.lg.info(' [*] List node (N0) gateways, (GW0) should not be listed')
        response = self.gateways_api.list_nodes_gateways(self.nodeid)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.gw_name, [x['name'] for x in response.json()])

    def test004_stop_gw(self):
        """ GAT-135
        **Test Scenario:**

        #. Stop the running gatway
        #. Verify its status
        """
        response = self.containers_api.get_containers(nodeid=self.nodeid)
        for container in response.json():
            if self.gw_name == container['name']:
                self.assertEqual(container['status'], 'running')

        response = self.gateways_api.post_nodes_gateway_stop(nodeid=self.nodeid, gwname=self.gw_name)
        self.assertEqual(response.status_code, 204, response.content)

        response = self.containers_api.get_containers(nodeid=self.nodeid)
        for container in response.json():
            if self.gw_name == container['name']:
                self.assertEqual(container['status'], 'halted')

        response = self.gateways_api.post_nodes_gateway_start(nodeid=self.nodeid, gwname=self.gw_name)
        self.assertEqual(response.status_code, 204, response.content)

    def test005_start_gw(self):
        """ GAT-136
        **Test Scenario:**

        #. Stop the running gateway and make sure that its status has been changed
        #. Start the gateway
        #. Verify its status
        """
        response = self.gateways_api.post_nodes_gateway_stop(nodeid=self.nodeid, gwname=self.gw_name)
        self.assertEqual(response.status_code, 204, response.content)

        response = self.containers_api.get_containers(nodeid=self.nodeid)
        for container in response.json():
            if self.gw_name == container['name']:
                self.assertEqual(container['status'], 'halted')

        response = self.gateways_api.post_nodes_gateway_start(nodeid=self.nodeid, gwname=self.gw_name)
        self.assertEqual(response.status_code, 204, response.content)

        response = self.containers_api.get_containers(nodeid=self.nodeid)
        for container in response.json():
            if self.gw_name == container['name']:
                self.assertEqual(container['status'], 'running')

    def test006_update_gw_nics_config(self):
        """ GAT-137
        **Test Scenario:**

        #. Use put method to update the nics config for the gw
        #. List the gw and make sure that its nics config have been updated
        """
        self.body['nics'] = [{
            "name": "public",
            "type": "vlan",
            "id": self.public_vlan_id,
            "config": {
                "cidr": "192.168.10.10/24",
                "gateway": "192.168.10.1"
            }
        },
            {
                "name": "private",
                "type": "vxlan",
                "id": self.private_vxlan_id,
                "config": {
                    "cidr": "192.168.20.2/24"
                }
            }]

        del self.body['name']

        self.lg.info(' [*] Use put method to update the nics config for the gw')
        response = self.gateways_api.update_nodes_gateway(self.nodeid, self.gw_name, self.body)
        self.assertEqual(response.status_code, 204)

        self.lg.info(' [*] List the gw and make sure that its nics config have been updated')
        response = self.gateways_api.get_nodes_gateway(self.nodeid, self.gw_name)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.body['nics'], response.json()['nics'])

    def test007_update_gw_portforwards_config(self):
        """ GAT-138
        **Test Scenario:**

        #. Use put method to update the portforwards config for the gw
        #. List the gw and make sure that its portforwards config have been updated
        """
        self.body['portforwards'] = [
            {
                "protocols": ['udp', 'tcp'],
                "srcport": random.randint(100, 1000),
                "srcip": "192.168.1.1",
                "dstport": random.randint(100, 1000),
                "dstip": "192.168.2.100"
            }
        ]

        del self.body['name']

        self.lg.info(' [*] Use put method to update the portforwards config for the gw')
        response = self.gateways_api.update_nodes_gateway(self.nodeid, self.gw_name, self.body)
        self.assertEqual(response.status_code, 204)

        self.lg.info(' [*] List the gw and make sure that its portforwards config have been updated')
        response = self.gateways_api.get_nodes_gateway(self.nodeid, self.gw_name)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.body['portforwards'], response.json()['portforwards'])

    def test008_update_gw_dhcpserver_config(self):
        """ GAT-139
        **Test Scenario:**

        #. Use put method to update the dhcpserver config for the gw
        #. List the gw and make sure that its dhcpserver config have been updated
        """
        self.body['nics'][1]['dhcpserver'] = {
            "nameservers": ["8.8.8.8"],
            "hosts": [
                {
                    "macaddress": self.randomMAC(),
                    "hostname": self.random_string(),
                    "ipaddress": "192.168.2.100"
                }
            ]
        }

        del self.body['name']

        self.lg.info(' [*] Use put method to update the dhcpserver config for the gw')
        response = self.gateways_api.update_nodes_gateway(self.nodeid, self.gw_name, self.body)
        self.assertEqual(response.status_code, 204, response.content)

        self.lg.info(' [*] List the gw and make sure that its dhcpserver config have been updated')
        response = self.gateways_api.get_nodes_gateway(self.nodeid, self.gw_name)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.body['nics'][1]['dhcpserver'], response.json()['nics'][1]['dhcpserver'])

    def test009_update_gw_httpproxies_config(self):
        """ GAT-140
        **Test Scenario:**

        #. Use put method to update the dhcpserver config for the gw
        #. List the gw and make sure that its httpproxies config have been updated
        """
        self.body['httpproxies'] = [
            {
                "host": self.random_string(),
                "destinations": ["192.168.200.10:1101"],
                "types": ['https', 'http']
            }
        ]

        del self.body['name']

        self.lg.info(' [*] Use put method to update the dhcpserver config for the gw')
        response = self.gateways_api.update_nodes_gateway(self.nodeid, self.gw_name, self.body)
        self.assertEqual(response.status_code, 204)

        self.lg.info(' [*] List the gw and make sure that its dhcpserver config have been updated')
        response = self.gateways_api.get_nodes_gateway(self.nodeid, self.gw_name)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.body['httpproxies'], response.json()['httpproxies'])

    def test010_create_list_portforward(self):
        """ GAT-114
        **Test Scenario:**

        #. Create new portforward table using firewall/forwards api
        #. Verify it is working right
        """
        body = {
            "protocols": ['udp', 'tcp'],
            "srcport": random.randint(1, 2000),
            "srcip": "192.168.1.1",
            "dstport": random.randint(1, 2000),
            "dstip": "192.168.2.5"
        }

        self.lg.info(' [*] Create new portforward table using firewall/forwards api')
        response = self.gateways_api.post_nodes_gateway_forwards(self.nodeid, self.gw_name, body)
        self.assertEqual(response.status_code, 201, response.content)

        self.lg.info(' [*] Verify it is working right')
        response = self.gateways_api.list_nodes_gateway_forwards(self.nodeid, self.gw_name)
        self.assertEqual(response.status_code, 200)
        self.assertIn(body, response.json())

    def test012_delete_portforward(self):
        """ GAT-115
        **Test Scenario:**

        #. Create new portforward table using firewall/forwards api
        #. List portfowards table
        #. Delete this portforward config
        #. List portforwards and verify that it has been deleted
        """
        body = {
            "protocols": ['udp', 'tcp'],
            "srcport": random.randint(1, 2000),
            "srcip": "192.168.1.1",
            "dstport": random.randint(1, 2000),
            "dstip": "192.168.2.5"
        }

        self.lg.info(' [*] Create new portforward table using firewall/forwards api')
        response = self.gateways_api.post_nodes_gateway_forwards(self.nodeid, self.gw_name, body)
        self.assertEqual(response.status_code, 201, response.content)

        self.lg.info(' [*] List portfowards table')
        response = self.gateways_api.list_nodes_gateway_forwards(self.nodeid, self.gw_name)
        self.assertEqual(response.status_code, 200)
        self.assertIn(body, response.json())

        self.lg.info(' [*] Delete this portforward config')
        forwardid = '{}:{}'.format(body['srcip'], body['srcport'])
        response = self.gateways_api.delete_nodes_gateway_forward(self.nodeid, self.gw_name, forwardid)
        self.assertEqual(response.status_code, 204)

        self.lg.info(' [*] List portfowards table')
        response = self.gateways_api.list_nodes_gateway_forwards(self.nodeid, self.gw_name)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(body, response.json())

    def test013_add_dhcp_host(self):
        """ GAT-116
        **Test Scenario:**
        #. Add new dhcp host to an interface
        #. List dhcp hosts
        #. Verify that is the list has the config
        """
        self.lg.info(' [*] Add new dhcp host to an interface')
        interface = 'private'
        hostname = self.random_string()
        macaddress = self.randomMAC()
        ipaddress = '192.168.2.3'
        body = {
            "hostname": hostname,
            "macaddress": macaddress,
            "ipaddress": ipaddress
        }

        response = self.gateways_api.post_nodes_gateway_dhcp_host(self.nodeid, self.gw_name, interface, body)
        self.assertEqual(response.status_code, 204)

        self.lg.info(' [*] List dhcp hosts')
        response = self.gateways_api.list_nodes_gateway_dhcp_hosts(self.nodeid, self.gw_name, interface)
        self.assertEqual(response.status_code, 200)

        self.lg.info(' [*] Verify that is the list has the config')
        dhcp_host = [x for x in response.json() if x['hostname'] == hostname]
        self.assertNotEqual(dhcp_host, [])
        for key in body.keys():
            self.assertTrue(body[key], dhcp_host[0][key])

    def test014_delete_dhcp_host(self):
        """ GAT-117
        **Test Scenario:**
        #. Add new dhcp host to an interface
        #. List dhcp hosts
        #. Delete one host form the dhcp
        #. List dhcp hosts
        #. Verify that the dhcp has been updated
        """
        self.lg.info(' [*] Add new dhcp host to an interface')
        interface = 'private'
        hostname = self.random_string()
        macaddress = self.randomMAC()
        ipaddress = '192.168.2.3'
        body = {
            "hostname": hostname,
            "macaddress": macaddress,
            "ipaddress": ipaddress
        }

        response = self.gateways_api.post_nodes_gateway_dhcp_host(self.nodeid, self.gw_name, interface, body)
        self.assertEqual(response.status_code, 204)

        self.lg.info(' [*]  Delete one host form the dhcp')
        response = self.gateways_api.delete_nodes_gateway_dhcp_host(self.nodeid, self.gw_name, interface,
                                                                    macaddress.replace(':', ''))
        self.assertEqual(response.status_code, 204)

        self.lg.info(' [*] List dhcp hosts')
        response = self.gateways_api.list_nodes_gateway_dhcp_hosts(self.nodeid, self.gw_name, interface)
        self.assertEqual(response.status_code, 200)

        self.lg.info(' [*] Verify that the dhcp has been updated')
        dhcp_host = [x for x in response.json() if x['hostname'] == hostname]
        self.assertEqual(dhcp_host, [])

    def test015_create_new_httpproxy(self):
        """ GAT-118
        **Test Scenario:**
        #. Create new httpproxy
        #. List httpproxy config
        #. Verify that is the list has the config
        """

        self.lg.info(' [*] Add new httpproxy host to an interface')
        body = {
            "host": self.random_string(),
            "destinations": ['http://192.168.2.200:500'],
            "types": ['http', 'https']
        }

        response = self.gateways_api.post_nodes_gateway_httpproxy(self.nodeid, self.gw_name, body)
        self.assertEqual(response.status_code, 201)

        self.lg.info(' [*] List dhcp httpproxy')
        response = self.gateways_api.list_nodes_gateway_httpproxies(self.nodeid, self.gw_name)
        self.assertEqual(response.status_code, 200)

        self.lg.info(' [*] Verify that is the list has the config')
        httpproxy_host = [x for x in response.json() if x['host'] == body['host']]
        self.assertNotEqual(httpproxy_host, [])
        for key in body.keys():
            self.assertTrue(body[key], httpproxy_host[0][key])

    def test016_delete_httpproxyid(self):
        """ GAT-119
        **Test Scenario:**
        #. Create new httpproxy
        #. Delete httpproxy id
        #. List dhcp hosts
        #. Verify that the dhcp has been updated
        """
        self.lg.info(' [*] Create new httpproxy')
        body = {
            "host": self.random_string(),
            "destinations": ['http://192.168.2.200:500'],
            "types": ['http', 'https']
        }

        response = self.gateways_api.post_nodes_gateway_httpproxy(self.nodeid, self.gw_name, body)
        self.assertEqual(response.status_code, 201)

        self.lg.info(' [*] Delete httpproxy id')
        proxyid = body['host']
        response = self.gateways_api.delete_nodes_gateway_httpproxy(self.nodeid, self.gw_name, proxyid)
        self.assertEqual(response.status_code, 204)

        self.lg.info(' [*] List httpproxies')
        response = self.gateways_api.list_nodes_gateway_httpproxies(self.nodeid, self.gw_name)
        self.assertEqual(response.status_code, 200)

        self.lg.info(' [*] Verify that the httpproxies has been updated')
        httpproxy_host = [x for x in response.json() if x['host'] == body['host']]
        self.assertEqual(httpproxy_host, [])
