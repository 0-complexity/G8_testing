# coding=utf-8
import random
import unittest
from ....utils.utils import BasicACLTest
from JumpScale.portal.portal.PortalClient2 import ApiError
from JumpScale.baselib.http_client.HttpClient import HTTPError


class CloudspaceTests(BasicACLTest):

    def setUp(self):
        super(CloudspaceTests, self).setUp()
        self.default_setup()

    def test001_validate_deleted_cloudspace_with_running_machines(self):
        """ OVC-020
        *Test case for validate deleted cloudspace with running machines get destroyed.*

        **Test Scenario:**

        #. Create 3+ vm's possible with different images on new cloudspace, should succeed
        #. Cloudspace status should be DEPLOYED, should succeed
        #. Try to delete the cloudspace with delete, should fail with 409 conflict
        #. Delete the cloudspace with destroy, should succeed
        #. Try list user's cloud spaces, should return empty list, should succeed
        """
        self.lg('%s STARTED' % self._testID)

        self.lg("1- Create 3+ vm's possible with different images on new cloudspace, "
                "should succeed")
        cloudspace_id = self.cloudapi_cloudspace_create(self.account_id,
                                                        self.location,
                                                        self.account_owner)

        images = self.api.cloudapi.images.list()
        for image in images:
            image_name = image['name']
            self.lg('- using image [%s]' % image_name)
            size = random.choice(self.api.cloudapi.sizes.list(cloudspaceId=cloudspace_id))
            self.lg('- using image [%s] with memory size [%s]' % (image_name, size['memory']))
            if 'Windows' in image_name:
                   while True:
                       disksize = random.choice(size['disks'])
                       if disksize > 25:
                            break
            else:
                disksize = random.choice(size['disks'])
            self.lg('- using image [%s] with memory size [%s] with disk '
                    '[%s]' % (image_name, size['memory'], disksize))
            machine_id = self.cloudapi_create_machine(cloudspace_id=cloudspace_id,
                                                      size_id=size['id'],
                                                      image_id=image['id'],
                                                      disksize=disksize)

        self.lg("2- Cloudspace status should be DEPLOYED, should succeed")
        self.wait_for_status(status='DEPLOYED', func=self.api.cloudapi.cloudspaces.get,
                             timeout=60, cloudspaceId=cloudspace_id)

        self.lg('3- Try to delete the cloudspace with delete, should fail with 409 conflict')
        try:
            self.api.cloudapi.cloudspaces.delete(cloudspaceId=cloudspace_id)
        except (HTTPError, ApiError) as e:
            self.lg('- expected error raised %s' % e.message)
            self.assertEqual(e.status_code, 409)

        self.lg('4- Delete the cloudspace with destroy, should succeed')
        self.api.cloudbroker.cloudspace.destroy(accountId= self.account_id,
                                                cloudspaceId=cloudspace_id,
                                                reason='test')
        self.wait_for_status('DESTROYED', self.api.cloudapi.cloudspaces.get,
                             cloudspaceId=cloudspace_id)

        self.lg("5- Try list user's cloud spaces, should return empty list, should succeed")
        self.assertFalse(self.api.cloudapi.machines.list(cloudspaceId=cloudspace_id))

        self.lg('%s ENDED' % self._testID)

    @unittest.skip('https://github.com/0-complexity/openvcloud/issues/942 943')
    def test002_add_remove_AllowedSize_to_cloudspace(self):
        """ OVC-027
        *Test case for adding and removing  allowed size to a cloudspace.*

        **Test Scenario:**
        #. Create new cloudspace CS1.
        #. Get list of available sizes in location, should succeed.
        #. Add random size to CS1, should succeed.
        #. Check if the size has been added successfully to CS1.
        #. Remove this size from CS1, should succeed.
        #. check if the size has been removed successfully from CS1.
        #. Remove this size again, should fail.
        """

        self.lg('1- Get list of available sizes in location, should succeed.')
        location_sizes = self.api.cloudapi.sizes.list(location=self.location)
        selected_size = random.choice(location_sizes)

        self.lg('2- Add random size to CS1, should succeed')
        self.api.cloudapi.cloudspaces.addAllowedSize(cloudspaceId=self.cloudspace_id, sizeId=selected_size['id'])

        self.lg('3- Check if the size has been added successfully to CS1')
        cloudspace_sizes = self.api.cloudapi.sizes.list(location=self.location, cloudspaceId=self.cloudspace_id)
        self.assertIn(selected_size, cloudspace_sizes)

        self.lg('4- Remove this size from CS1, should succeed')
        self.api.cloudapi.cloudspaces.removeAllowedSize(cloudspaceId=self.cloudspace_id, sizeId=selected_size['id'])

        self.lg('5- check if the size has been removed successfully from CS1')
        cloudspace_sizes = self.api.cloudapi.sizes.list(location=self.location, cloudspaceId=self.cloudspace_id)
        self.assertNotIn(selected_size, cloudspace_sizes)

        self.lg('6- Remove this size again, should fail')
        with self.assertRaises(ApiError):
            self.api.cloudapi.cloudspaces.removeAllowedSize(cloudspaceId=self.cloudspace_id, sizeId=selected_size['id'])

    def test003_executeRouterOSScript(self):
        """ OVC-040
        *Test case for test execute script in routeros.*

        **Test Scenario:**
        #. Create new cloudspace (CS1).
        #. Create virtual machine (VM1).
        #. Execute script on routeros of CS1 to create portforward (PF1), should succeed.
        #. Connect to VM1 through PF1 , should succeed.
        """
        self.lg('%s STARTED' % self._testID)

        self.lg('Create virtual machine (VM1)')
        vm_id = self.cloudapi_create_machine(cloudspace_id=self.cloudspace_id)

        self.lg('Execute script on routeros of CS1 to create portforward (PF1), should succeed')
        vm = self.api.cloudapi.machines.get(machineId=vm_id)
        cs_ip = self.api.cloudapi.cloudspaces.get(cloudspaceId=vm['cloudspaceid'])['publicipaddress']
        vm_ip = self.wait_for_machine_to_get_ip(vm_id)
        pb_port = random.randint(50000, 60000)
        script = '/ip firewall nat add chain=dstnat action=dst-nat to-addresses=%s to-ports=22 protocol=tcp dst-address=%s dst-port=%s comment=cloudbroker' % (vm_ip, cs_ip, pb_port)
        self.api.cloudapi.cloudspaces.executeRouterOSScript(self.cloudspace_id, script=script)

        self.lg('Connect to VM1 through PF1 , should succeed')
        vm1_conn = self.get_vm_connection(vm_id, pb_port=pb_port)
        self.assertIn('bin', vm1_conn.run('ls /'))

        self.lg('%s ENDED' % self._testID)

    @unittest.skip('https://github.com/0-complexity/openvcloud/issues/1039')
    def test004_disable_cloudspace(self):
        """ OVC-04x
        *Test case for test disable cloudspace.*

        **Test Scenario:**
        #. Create new cloudspace (CS1).
        #. Create virtual machine (VM1).
        #. Disable cloudspace (CS1), should succeed.
        #. Check virtual machine (VM1) status, should be halted.
        #. Create user without Admin access.
        #. Authenticate (U1), should succeed.
        #. Add user (U1) to cloudsapce (CS1), should succeed.
        #. Try to start virtual machine (VM1) using user (U1), should fail.
        #. Enable cloudspace (CS1), should succeed.
        #. Try to start virtual machine (VM1) using user (U1), should succeed.
        #. Disable cloudspace (CS1) again, should succeed.
        #. Delete cloudspace (CS1) should succeed.
        """

        self.lg('Create virtual machine (VM1)')
        machineId = self.cloudapi_create_machine(self.cloudspace_id) 
        self.wait_for_status('RUNNING', self.api.cloudapi.machines.get, machineId=machineId)

        self.lg('Disable cloudspace (CS1), should succeed')
        self.assertTrue(self.api.cloudapi.cloudspaces.disable(cloudspaceId=self.cloudspace_id, reason='test'))

        self.lg('Check virtual machine (VM1) status, should be halted')
        machine_info = self.api.cloudapi.machines.get(machineId=machineId)
        self.assertEqual(machine_info['status'], 'HALTED')

        self.lg('Create user (U1) without Admin access')
        user = self.cloudbroker_user_create()

        self.lg("Authenticate (U1), should succeed")
        user_api = self.get_authenticated_user_api(user)

        self.lg('Add user (U1) to cloudsapce (CS1), should succeed')
        self.add_user_to_cloudspace(self.cloudspace_id, user, 'ACDRUX')

        self.lg('Try to start virtual machine (VM1), should fail')
        with self.assertRaises(ApiError) as e:
            user_api.cloudapi.machines.start(machineId=machineId)
        
        self.lg('Enable cloudspace (CS1), should succeed')
        self.assertTrue(self.api.cloudapi.cloudspaces.enable(cloudspaceId=self.cloudspace_id, reason='test'))

        self.lg('Try to start virtual machine (VM1) using user (U1), should succeed')
        self.assertTrue(self.api.cloudapi.machines.start(machineId=machineId))

        self.lg('Disable cloudspace (CS1) again, should succeed')
        self.assertTrue(self.api.cloudapi.cloudspaces.disable(cloudspaceId=self.cloudspace_id, reason='test'))

        self.lg('Delete cloudspace (CS1) should succeed')
        self.api.cloudapi.machines.delete(machineId=machineId)
