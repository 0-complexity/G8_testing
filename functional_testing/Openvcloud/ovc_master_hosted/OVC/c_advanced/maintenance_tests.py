import unittest
from ....utils.utils import BasicACLTest, VMClient
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

    def wait_till_vm_move(self, vm_id, stackId, status="RUNNING", timeout=30):
        """
        stackId: stackId that the vm will move from.
        status: status that need to be checked on after vm migration.
        """
        for _ in xrange(timeout):
            time.sleep(2)
            vm = self.api.cloudbroker.machine.get(machineId=vm_id)
            if vm['stackId'] != stackId:
                break
            else:
                continue
        self.assertNotEqual(vm["stackId"], stackId, "vm didn't move to another stack")
        self.assertEqual(vm["status"], status, "vm is not %s" % status)


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

    @parameterized.expand(['move', 'stop'])
    def test002_node_maintenance_migrateVMs(self, migrate_option):
        """ OVC-49
        *Test case for putting node in maintenance with action move or stop all vms.*

        **Test Scenario:**

        #. Create 3 VMs, should succeed.
        #. Leave one VM running, stop one, and pause another, should succeed.
        #. Put node in maintenance with migrate all vms, should succeed.
        #. Check if the 3 VMs have been migrated keeping their old state, should succeed.
        #. Check that the running VM is working well (option=move vms), should succeed.
        #. Enable the node back, should succeed.
        """
        self.lg('%s STARTED' % self._testID)

        self.lg('Create 2 VMs, should succeed')
        machine_1_id = self.cloudbroker_create_machine(self.cloudspace_id, stackId=self.stackId)
        machine_2_id = self.cloudbroker_create_machine(self.cloudspace_id, stackId=self.stackId)
        machine_3_id = self.cloudbroker_create_machine(self.cloudspace_id, stackId=self.stackId)

        self.lg('Leave one VM running, stop one, and pause another, should succeed.')
        stopped = self.api.cloudapi.machines.stop(machineId=machine_2_id)
        self.assertTrue(stopped)
        self.api.cloudapi.machines.pause(machineId=machine_3_id)
        self.assertEqual(self.api.cloudapi.machines.get(machineId=machine_3_id)['status'], 'PAUSED')

        self.lg('Put node in maintenance with migrate all vms, should succeed')
        self.api.cloudbroker.computenode.maintenance(id=self.stackId, gid=self.gridId, vmaction=migrate_option, message='test')

        self.lg('Check if the 3 VMs have been migrated keeping their old state, should succeed')
        if migrate_option == 'move':
            self.wait_till_vm_move(machine_1_id, self.stackId, status='RUNNING')
            self.wait_till_vm_move(machine_2_id, self.stackId, status='HALTED')
            self.wait_till_vm_move(machine_3_id, self.stackId, status='PAUSED')
            self.lg('Check that the running VM is working well, should succeed')
            machine_1_client = VMClient(machine_1_id)
            stdin, stdout, stderr = machine_1_client.execute('uname')
            self.assertIn('Linux', stdout.read())
        else:
            self.wait_for_status('HALTED', self.api.cloudapi.machines.get, timeout=30, machineId=machine_1_id)
            self.assertEqual(self.api.cloudapi.machines.get(machineId=machine_1_id)['status'], 'HALTED')
            self.wait_for_status('HALTED', self.api.cloudapi.machines.get, timeout=30, machineId=machine_2_id)
            self.assertEqual(self.api.cloudapi.machines.get(machineId=machine_2_id)['status'], 'HALTED')
            self.wait_for_status('HALTED', self.api.cloudapi.machines.get, timeout=30, machineId=machine_3_id)
            self.assertEqual(self.api.cloudapi.machines.get(machineId=machine_3_id)['status'], 'HALTED')
        self.assertTrue(self.wait_for_stack_status(self.stackId, 'MAINTENANCE'))

        self.lg('%s ENDED' % self._testID)
