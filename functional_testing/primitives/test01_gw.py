import argparse, requests
from termcolor import colored
from js9 import j
from base_test import TestcasesBase

class Gateways(TestcasesBase):
    def setUp(self):
        super().setUp()

    def test001_create_gateway_with_passthrough_and_zerotier_vm(self):
        """ SAL-GW-000

        *Test case for deploying gateways with passthrough and zerotier networks . *

        **Test Scenario:**

        #. Create gateway with public passthrough network and private zerotier network, should succeed.
        #. Adding a new vm [vm1] to gateway private network , should succeed.
        #. Check that the vm has been join the zerotier network.
        #. Adding a new vm [vm2] to gateway private network, should succeed.
        #. Check that vm1  can ping vm2. 

        """
        self.log("Create gateway with public passthrough network and private zerotier network, should succeed.")
        self.primitive.create_gw_passthrough_zt()

        self.log("Adding a new vm t to gateway private network , should succeed.")
        source_port = 2202
        destination_port =22
        vm1_ip = self.primitive.create_ubuntu_vms_zt(source_port, destination_port)

        self.log(" Adding a new vm [vm2] to gateway private network, should succeed.")
        source_port = 2203
        destination_port =22
        vm2_ip = self.primitive.create_ubuntu_vms_zt(source_port, destination_port)

        self.log("Check that vm1  can ping vm2.")
        command = "ping -c 5 %s"%vm2_ip
        result = self.execute_command(vm1_ip, command)
        self.assertIn("5 packets transmitted", result)