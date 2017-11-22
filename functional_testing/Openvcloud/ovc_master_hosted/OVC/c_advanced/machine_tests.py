import unittest, random, uuid
from ....utils.utils import BasicACLTest
from nose_parameterized import parameterized
from JumpScale.portal.portal.PortalClient2 import ApiError
from JumpScale.baselib.http_client.HttpClient import HTTPError


class MachineTests(BasicACLTest):

    def setUp(self):
        super(MachineTests, self).setUp()
        self.default_setup()

    @unittest.skip('Not Implemented')
    def test001_check_machines_networking(self):
        """ OVC-000
        *Test case for checking machines networking*

        **Test Scenario:**

        #. Create cloudspace CS1, should succeed
        #. Create cloudspace CS2, should succeed
        #. Create VM1 in CS1
        #. From VM1 ping google, should succeed
        #. Create VM2 and VM3 in CS2
        #. From VM2 ping VM3, should succeed
        #. From VM2 ping VM1, should fail
        """

    def test002_check_network_data_integrity(self):
        """ OVC-036
        *Test case for checking network data integrity through VMS*
        **Test Scenario:**
        #. Create a cloudspace CS1, should succeed.
        #. Create VM1 and VM2 inside CS1, should succeed.
        #. Create a file F1 inside VM1.
        #. From VM1 send F1 to VM2, should succeed.
        #. Check that F1 has been sent to vm2 without data loss.
        """
        self.lg('%s STARTED' % self._testID)

        self.lg('Create a cloudspace CS1, should succeed')
        self.lg('Create VM1 and VM2 inside CS1, should succeed')
        VM1_id = self.cloudapi_create_machine(cloudspace_id=self.cloudspace_id)
        VM2_id = self.cloudapi_create_machine(cloudspace_id=self.cloudspace_id)

        self.lg('create a file F1 inside VM1')
        vm1_conn = self.get_vm_connection(VM1_id)
        text = str(uuid.uuid4())[0:8]
        vm1_conn.run('echo %s >> test.txt' % text)

        self.lg('From VM1 send F1 to VM2, should succeed')
        self.send_file_from_vm_to_another(vm1_conn, VM2_id, 'test.txt')

        self.lg('Check that F1 has been sent to vm2 without data loss')
        vm2_conn = self.get_vm_connection(VM2_id)
        response = vm2_conn.run('cat test.txt')
        self.assertEqual(response, text)

        self.lg('%s ENDED' % self._testID)

    @unittest.skip('Not Implemented')
    def test003_check_connectivity_through_external_network(self):
        """ OVC-000
        *Test case for checking machine connectivity through external network*

        **Test Scenario:**

        #. Create a cloudspace CS1, should succeed
        #. Create VM1
        #. Attach VM1 to an external network, should succeed
        #. Assign IP to VM1's external netowrk interface, should succeed.
        #. Check if you can ping VM1 from outside, should succeed
        """

    @unittest.skip('Not Implemented')
    def test004_migrate_vm_in_middle_of_writing_file(self):
        """ OVC-000
        *Test case for checking data integrity after migrating vm in the middle of writing a file*

        **Test Scenario:**

        #. Create a cloudspace CS1, should succeed
        #. Create VM1
        #. Write a big file FS1 on VM1
        #. Migrate VM1 in the middle of writing a file, should succeed
        #. Check if the file has been written correctly after vm live migration
        """
        # Note: this testcase may be hard to be implemented from here.

    @parameterized.expand(['Linux', 'Windows'])
    @unittest.skip('https://github.com/0-complexity/openvcloud/issues/940')
    def test005_cheching_vm_specs_after_rebooting(self, image_type):
        """ OVC-028
        *Test case for checking VM's ip and credentials after rebooting*

        **Test Scenario:**

        #. Create virtual machine VM1 with windows image.
        #. Get machine VM1 info, should succeed.
        #. Reboot VM1, should succeed.
        #. Get machine VM1 info, should succeed.
        #. Check if VM1's ip is the same as before rebooting.
        #. Check if VM1's credentials are the same as well.
        """

        self.lg('1- Create virtual machine VM1 with {} image'.format(image_type))
        target_images = [x['id'] for x in self.api.cloudapi.images.list() if x['type'] == image_type]

        if not target_images:
            self.skipTest('No image with type {} is avalilable'.format(image_type))

        selected_image_id = random.choice(target_images)

        machineId = self.cloudapi_create_machine(self.cloudspace_id, self.account_owner_api, image_id=selected_image_id, disksize=50)

        self.lg('2- Get machine VM1 info, should succeed')
        machine_info_before_reboot = self.api.cloudapi.machines.get(machineId=machineId)

        self.lg('3- Reboot VM1, should succeed')
        self.assertTrue(self.api.cloudapi.machines.reboot(machineId=machineId))

        self.lg('4- Get machine VM1 info, should succeed')
        machine_info_after_reboot = self.api.cloudapi.machines.get(machineId=machineId)

        self.lg("5- Check if VM1's ip is the same as before rebooting")
        self.assertEqual(
            machine_info_before_reboot['interfaces'][0]['ipAddress'],
            machine_info_after_reboot['interfaces'][0]['ipAddress']
        )

        self.lg("6- Check if VM1's credentials are the same as well")
        self.assertEqual(
            machine_info_before_reboot['accounts'][0]['login'],
            machine_info_after_reboot['accounts'][0]['login']
        )

        self.assertEqual(
            machine_info_before_reboot['accounts'][0]['password'],
            machine_info_after_reboot['accounts'][0]['password']
        )

    @unittest.skip('https://github.com/0-complexity/openvcloud/issues/938 & 941')
    def test006_attach_same_disk_to_two_vms(self):
        """ OVC-024
        *Test case for attaching same disk to two different vms*

        **Test Scenario:**

        #. Create VM1 and VM2.
        #. Create disk DS1.
        #. Attach DS1 to VM1, should succeed.
        #. Attach DS1 to VM2, should fail.
        #. Detach DS1 from VM2, should fail.
        #. Delete disk after detaching it, should succeed
        """
        # Note: try this scenario for data and boot disks

        self.lg('%s STARTED' % self._testID)

        self.lg('Create VM1 and VM2')
        VM1_id = self.cloudapi_create_machine(cloudspace_id=self.cloudspace_id)
        VM2_id = self.cloudapi_create_machine(cloudspace_id=self.cloudspace_id)

        self.lg(' Create disk DS1.')
        disk_id = self.create_disk(self.account_id)
        self.assertTrue(disk_id)

        self.lg('Attach DS1 to VM1, should succeed.')
        response = self.api.cloudapi.machines.attachDisk(machineId=VM1_id, diskId=disk_id)
        self.assertTrue(response)

        self.lg('Attach DS1 to VM2, should fail.')
        try:
            self.api.cloudapi.machines.attachDisk(machineId=VM2_id, diskId=disk_id)
        except (HTTPError, ApiError) as e:
            self.lg('- expected error raised %s' % e.message)
            self.assertEqual(e.status_code, 400)

        self.lg('Delete disk after detaching it, should succeed')
        response = self.api.cloudapi.disks.delete(diskId=disk_id, detach=True)
        self.assertTrue(response)

        self.lg('%s ENDED' % self._testID)

    @unittest.skip('https://github.com/0-complexity/openvcloud/issues/969 & 937')
    def test007_detach_boot_from_running_machine(self):
        """ OVC-025
        * Test case for detaching boot disk from a running machine.

        **Test Scenario:**

        #. Create virtual machine (VM1).
        #. Detach VM1's boot disk (BD1), should fail.
        #. Stop VM1.
        #. Detach VM1's boot disk again, should succeed.
        #. Start VM1, should fail.
        #. Attach BD1 to VM1, should succeed.
        #. Start VM1 and make sure it is running.
        """
        self.lg('%s STARTED' % self._testID)

        self.lg('Create virtual machine (VM1)')
        VM1_id = self.cloudapi_create_machine(cloudspace_id=self.cloudspace_id)
        bd_id = self.api.cloudapi.machines.get(machineId=VM1_id)['disks'][0]['id']

        self.lg("Detach VM1's boot disk (BD1), should fail")
        try:
            self.api.cloudapi.machines.detachDisk(machineId=VM1_id, diskId=bd_id)
        except (HTTPError, ApiError) as e:
            self.lg('- expected error raised %s' % e.message)
            self.assertEqual(e.status_code, 400)

        self.lg('Stop VM1')
        self.api.cloudapi.machines.stop(machineId=VM1_id)
        self.assertEqual(self.api.cloudapi.machines.get(machineId=VM1_id)['status'], 'HALTED')

        self.lg("Detach VM1's boot disk again, should succeed")
        response = self.api.cloudapi.machines.detachDisk(machineId=VM1_id, diskId=bd_id)
        self.assertTrue(response)
        self.assertFalse(self.api.cloudapi.machines.get(machineId=VM1_id)['disks'])

        self.lg("Start VM1, should fail")
        try:
            self.api.cloudapi.machines.start(machineId=VM1_id)
        except (HTTPError, ApiError) as e:
            self.lg('- expected error raised %s' % e.message)
            self.assertEqual(e.status_code, 400)

        self.lg("Attach BD1 to VM1, should succeed.")
        response = self.api.cloudapi.machines.attachDisk(machineId=VM1_id, diskId=bd_id)
        self.assertTrue(response)

        self.lg('Start VM1 and make sure it is running.')
        self.api.cloudapi.machines.start(machineId=VM1_id)
        self.assertEqual(self.api.cloudapi.machines.get(machineId=VM1_id)['status'], 'RUNNING')
        vm1_conn = self.get_vm_connection(VM1_id, wait_vm_ip=False)
        self.assertIn('bin', vm1_conn.run('ls /'))

        self.lg('%s ENDED' % self._testID)

    def test008_swap_vms_boot_disks(self):
        """ OVC-035
        * Test case for swapping vms boot disks.

        **Test Scenario:**

        #. Create virtual machines (VM1) and (VM2).
        #. Stop VM1 and VM2, should succeed.
        #. Detach VM1's boot disk (BD1) and VM2's boot disk (BD2).
        #. Attach BD1 to VM2, should succeed.
        #. Attach BD2 to VM1, should succeed.
        #. Start VM1 and VM2 and make sure they are working.
        """

        self.lg('%s STARTED' % self._testID)

        self.lg('Create virtual machines (VM1) and (VM2)')
        VM1_id = self.cloudapi_create_machine(cloudspace_id=self.cloudspace_id)
        VM2_id = self.cloudapi_create_machine(cloudspace_id=self.cloudspace_id)

        self.lg('Stop VM1 and VM2, should succeed')
        self.api.cloudapi.machines.stop(machineId=VM1_id)
        self.assertEqual(self.api.cloudapi.machines.get(machineId=VM1_id)['status'], 'HALTED')
        self.api.cloudapi.machines.stop(machineId=VM2_id)
        self.assertEqual(self.api.cloudapi.machines.get(machineId=VM2_id)['status'], 'HALTED')

        self.lg("Detach VM1's boot disk (BD1) and VM2's boot disk (BD2)")
        bd1_id = self.api.cloudapi.machines.get(machineId=VM1_id)['disks'][0]['id']
        bd2_id = self.api.cloudapi.machines.get(machineId=VM2_id)['disks'][0]['id']
        response = self.api.cloudapi.machines.detachDisk(machineId=VM1_id, diskId=bd1_id)
        self.assertTrue(response)
        response = self.api.cloudapi.machines.detachDisk(machineId=VM1_id, diskId=bd2_id)
        self.assertTrue(response)

        self.lg('Attach BD1 to VM2, should succeed')
        response = self.api.cloudapi.machines.attachDisk(machineId=VM2_id, diskId=bd1_id)
        self.assertTrue(response)

        self.lg('Attach BD2 to VM1, should succeed')
        response = self.api.cloudapi.machines.attachDisk(machineId=VM1_id, diskId=bd2_id)
        self.assertTrue(response)

        self.lg('Start VM1 and VM2 and make sure they are working')
        self.api.cloudapi.machines.start(machineId=VM1_id)
        self.assertEqual(self.api.cloudapi.machines.get(machineId=VM1_id)['status'], 'RUNNING')
        self.api.cloudapi.machines.start(machineId=VM2_id)
        self.assertEqual(self.api.cloudapi.machines.get(machineId=VM2_id)['status'], 'RUNNING')
        vm2 = self.api.cloudapi.machines.get(machineId=VM2_id)
        password = vm2['accounts'][0]['password']
        login = vm2['accounts'][0]['login']
        vm1_conn = self.get_vm_connection(VM1_id, wait_vm_ip=True, password=password, login=login)
        self.assertIn('bin', vm1_conn.run('ls /'))

        self.lg('%s ENDED' % self._testID)

    @unittest.skip('Not Implemented')
    def test009_connection_bet_VM_CS_ExternalNetwork(self):
        """ OVC-000
        * Test case for connection between virtual machines, cloudspaces and externel networks.

        **Test Scenario:**

        #. Create two cloudspace (CS1) and (CS2) with external network (EN1).
        #. Create a virtual machine (VM1) on CS1, should succeed.
        #. Attach VM1 to EN1, should succeed (Not implemented yet).
        #. Assign CS1's ip to VM1 external network interface, should succeed.
        #. Ping EN1's Gateway ip, should fail.
        #. Assign CS2's ip to VM1 external network interface, should succeed.
        #. Ping EN1's Gateway ip again, should fail.
        """

    @unittest.skip('Not Implemented')
    def test010_node_maintenance_migrateVMs(self):
        """ OVC-000
        *Test case for putting node in maintenance with action migrate all vms.*

        **Test Scenario:**

        #. Create 3 VMs, should succeed.
        #. Put node in maintenance with migrate all vms, should succeed.
        #. Check that the 3 VMs have been migrated.
        #. Check that the 3 VMs are in running state.
        #. Enable the node back, should succeed.
        """

    @unittest.skip('Not Implemented')
    def test011_restart_vm_after_migration(self):
        """ OVC-000
        *Test case for checking VM status after restarting it after migration*

        **Test Scenario:**

        #. Create a cloudspace CS1, should succeed.
        #. Create VM1.
        #. Migrate VM1 to another node, should succeed.
        #. Make sure that VM1 is running.
        #. Restart VM1 and make sure it is still running.
        """

    @unittest.skip('Not Implemented')
    def test012_check_cloned_vm(self):
        """ OVC-000
        *Test case for checking cloned VM ip, portforwards and credentials*

        **Test Scenario:**

        #. Create (VM1).
        #. Clone VM1 as (VM2_C), should succeed.
        #. Make sure VM2_C got a new ip.
        #. Check that VM2 got different credentials from VM1.
        #. Make sure no portforwards have been created.
        """
