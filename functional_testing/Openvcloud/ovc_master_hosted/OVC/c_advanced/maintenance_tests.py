import unittest
from ....utils.utils import BasicACLTest
from nose_parameterized import parameterized
from JumpScale.portal.portal.PortalClient2 import ApiError
from JumpScale.baselib.http_client.HttpClient import HTTPError
import time



class MaintenanceTests(BasicACLTest):
    def setUp(self):
        super(MaintenanceTests, self).setUp()
        self.default_setup()
        self.stackId = self.get_running_stackId()
        if not self.stackId:
            self.skipTest('[*] No running nodes ')
        self.gridId = self.get_node_gid(self.stackId)

    def tearDown(self):
        super(MaintenanceTests, self).tearDown()
        self.lg('Enable CPU1, should succeed')
        self.api.cloudbroker.computenode.enable(id=self.stackId, gid=self.gridId, message='test')
        self.assertTrue(self.wait_for_stack_status(self.stackId, 'ENABLED'))

    def wait_till_vm_move(self, vm_id, stackId, timeout=60):
        """
        :stackId: stackId that the vm will move from.
        """
        for _ in xrange(timeout):
            time.sleep(1)
            vm = self.api.cloudbroker.machine.get(machineId=vm_id)
            if vm['stackId'] != stackId:
                break
            else:
                continue
        self.assertNotEqual(vm["stackId"], stackId, "vm didn't move to another stack")
        self.assertEqual(vm["status"], "RUNNING", "vm is not running")


    def test001_check_vm_ext_net_migration(self):
        """ OVC-052
        *Test case for checking vm migration in which it is attached to external network*

        **Test Scenario:**

        #. Create cloudspace (CS1), should succeed.
        #. Create a vm (VM1), should succeed.
        #. Attach VM1 to an external network.
        #. Get VM1's cpu-node (CPU1) and put it in maintenance (option "move vms"), should succeed.
        #. Make sure VM1 has been moved to another cpu-node.
        #. Try to move VM1 back to CPU1, should fail.
        #. Enable CPU1, should succeed.
        """
        self.lg('%s STARTED' % self._testID)

        self.lg('Create a vm (VM1), should succeed.')
        vm_id = self.cloudbroker_create_machine(self.cloudspace_id, stackId=self.stackId)

        self.lg('Attach VM1 to an external network.')
        response = self.api.cloudbroker.machine.attachExternalNetwork(machineId=vm_id)
        self.assertTrue(response)

        self.lg("Get VM1's cpu-node (CPU1) and put it in maintenance (option (move vms)), should succeed.")
        self.lg('Put node in maintenance with migrate all vms, should succeed')
        self.api.cloudbroker.computenode.maintenance(id=self.stackId, gid=self.gridId, vmaction='move', message='test')

        self.lg('Make sure VM1 has been moved to another cpu-node.')
        self.wait_till_vm_move(vm_id, self.stackId)
        self.assertTrue(self.wait_for_stack_status(self.stackId, 'MAINTENANCE'))

        self.lg('Try to move VM1 back to CPU1, should fail.')
        with self.assertRaises(HTTPError) as e:
            self.api.cloudbroker.machine.moveToDifferentComputeNode(machineId=vm_id, reason="test",
                                                                        targetStackId=self.stackId, force=False)
        self.lg('- expected error raised %s' % e.exception.status_code)
        self.assertEqual(e.exception.status_code, 400)

        self.lg('%s ENDED' % self._testID)
