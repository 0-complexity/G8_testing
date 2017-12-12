import unittest, random, uuid
from ....utils.utils import BasicACLTest
from nose_parameterized import parameterized
from JumpScale.portal.portal.PortalClient2 import ApiError
from JumpScale.baselib.http_client.HttpClient import HTTPError
import time
import threading
import os

class MachineTests(BasicACLTest):
    def setUp(self):
        super(MachineTests, self).setUp()
        self.default_setup()

    def test001_check_machines_networking(self):
        """ OVC-038
        *Test case for checking machines networking*

        **Test Scenario:**

        #. Create cloudspace CS1, should succeed.
        #. Create cloudspace CS2, should succeed.
        #. Create VM1 in cloudspace CS1.
        #. Create VM2 and VM3 in cloudspace CS2.
        #. From VM1 ping google, should succeed.
        #. From VM1 ping VM3, should fail.
        #. From VM2 ping VM3, should succeed.
        """

        self.lg('Create cloudspace CS1, should succeed')
        cloudspace_1_id = self.cloudspace_id

        self.lg('Create cloudspace CS2, should succeed')
        cloudspace_2_id = self.cloudapi_cloudspace_create(
            self.account_id,
            self.location,
            self.account_owner
        )

        self.lg('Create VM1 in cloudspace CS1')
        machine_1_id = self.cloudapi_create_machine(cloudspace_id=cloudspace_1_id)
        machine_1_ipaddress = self.wait_for_machine_to_get_ip(machine_1_id)
        self.assertTrue(machine_1_ipaddress)

        self.lg('Create VM2 in cloudspace CS2')
        machine_2_id = self.cloudapi_create_machine(cloudspace_id=cloudspace_2_id)
        machine_2_ipaddress = self.wait_for_machine_to_get_ip(machine_2_id)
        self.assertTrue(machine_2_ipaddress)

        self.lg('Create VM3 in cloudspace CS2')
        machine_3_id = self.cloudapi_create_machine(cloudspace_id=cloudspace_2_id)
        machine_3_ipaddress = self.wait_for_machine_to_get_ip(machine_3_id)
        self.assertTrue(machine_3_ipaddress)

        machine_1_connection = self.get_vm_connection(machine_1_id, wait_vm_ip=False)

        self.lg('From VM1 ping google, should succeed')
        response = machine_1_connection.run('ping -w3 8.8.8.8')
        self.assertIn(', 0% packet loss', response)

        self.lg('From VM1 ping VM3 or VM2, should fail')
        if machine_1_ipaddress == machine_2_ipaddress:
            target_ip = machine_3_ipaddress
        else:
            target_ip = machine_2_ipaddress

        with self.assertRaises(SystemExit):
            cmd = 'ping -w3 {}'.format(target_ip)
            response = machine_1_connection.run(cmd)
            self.assertIn(', 100% packet loss', response)

        machine_2_connection = self.get_vm_connection(machine_2_id, wait_vm_ip=False)

        self.lg('From VM2 ping VM3, should succeed')
        cmd = 'ping -w3 {}'.format(machine_3_ipaddress)
        response = machine_2_connection.run(cmd)
        self.assertIn(', 0% packet loss', response)


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

    def test003_check_connectivity_through_external_network(self):
        """ OVC-042
        *Test case for checking machine connectivity through external network*

        **Test Scenario:**

        #. Create a cloudspace CS1, should succeed
        #. Create VM1
        #. Attach VM1 to an external network, should succeed
        #. Assign IP to VM1's external netowrk interface, should succeed.
        #. Check if you can ping VM1 from outside, should succeed
        #. Check that you can connect to vm with new ip ,should succeed.

        """
        self.lg('%s STARTED' % self._testID)

        self.lg("Create VM1,should succeed.")
        vm1_id = self.cloudapi_create_machine(cloudspace_id=self.cloudspace_id)

        self.lg("Attach VM1 to an external network, should succeed")
        reponse = self.api.cloudbroker.machine.attachExternalNetwork(machineId=vm1_id)
        self.assertTrue(reponse)

        self.lg("Assign IP to VM1's external netowrk interface, should succeed.")
        vm1_nics = self.api.cloudapi.machines.get(machineId=vm1_id)["interfaces"]
        vm1_nic = [x for x in vm1_nics if "externalnetworkId" in x["params"]][0]
        self.assertTrue(vm1_nic)
        vm1_ext_ip = vm1_nic["ipAddress"]
        vm1_conn = self.get_vm_connection(vm1_id)
        vm1_conn.sudo("ip a a %s dev eth1"%vm1_ext_ip)
        vm1_conn.sudo("nohup bash -c 'ip l s dev eth1 up </dev/null >/dev/null 2>&1 & '")

        self.lg("Check if you can ping VM1 from outside, should succeed")
        vm1_ext_ip = vm1_ext_ip[:vm1_ext_ip.find('/')]
        response = os.system("ping -c 1 %s"%vm1_ext_ip)
        self.assertFalse(response)

        self.lg("Check that you can connect to vm with new ip ,should succeed.")
        ssh_client = self.get_vm_public_ssh_client(vm1_id)
        ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command("ls /")
        self.assertIn('bin', ssh_stdout.read())


    def test004_migrate_vm_in_middle_of_writing_file(self):
        """ OVC-039
        *Test case for checking data integrity after migrating vm in the middle of writing a file*

        **Test Scenario:**

        #. Create a cloudspace CS1, should succeed
        #. Create VM1, should succeed
        #. Write a big file FS1 on VM1
        #. Migrate VM1 in the middle of writing a file, should succeed
        #. Check if the file has been written correctly after vm live migration
        """
        self.lg('%s STARTED' % self._testID)

        self.lg("Create VM1,should succeed.")
        vm1_id = self.cloudapi_create_machine(cloudspace_id=self.cloudspace_id)

        self.lg('Write a big file FS1 on VM1')
        current_stackId = self.api.cloudbroker.machine.get(machineId=vm1_id)["stackId"]
        second_node = self.get_running_stackId(current_stackId)
        if not second_node:
            self.skipTest('[*] No running nodes ')
        vm1_conn = self.get_vm_connection(vm1_id)
        cmd = "yes 'Some text' | head -n 200000000 > largefile.txt"
        t = threading.Thread(target=vm1_conn.run, args=(cmd, ))
        t.start()
        time.sleep(7)

        self.lg("Migrate VM1 to another node, should succeed.")
        self.api.cloudbroker.machine.moveToDifferentComputeNode(machineId=vm1_id, reason="test",
                                                                targetStackId=second_node, force=False)
        vm1 = self.api.cloudbroker.machine.get(machineId=vm1_id)
        self.assertEqual(vm1["stackId"], second_node)

        self.lg("Make sure that VM1 is running.")
        self.assertEqual(vm1['status'], 'RUNNING')
        t.join()
        vm1_conn = self.get_vm_connection(vm1_id)
        self.assertIn('bin', vm1_conn.run('ls /'))

        self.lg('Check if the file has been written correctly after vm live migration')
        hash_val = vm1_conn.run('md5sum largefile.txt | cut -d " " -f 1')
        self.assertEqual(hash_val, 'cd96e05cf2a42e587c78544d19145a7e')

        self.lg('%s ENDED' % self._testID)


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
        self.lg('%s STARTED' % self._testID)

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

        self.lg('%s ENDED' % self._testID)

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
        with self.assertRaises(HTTPError) as e:
            self.api.cloudapi.machines.attachDisk(machineId=VM2_id, diskId=disk_id)

        self.lg('- expected error raised %s' % e.exception.status_code)
        self.assertEqual(e.exception.status_code, 400)

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
        with self.assertRaises(HTTPError) as e:
            self.api.cloudapi.machines.detachDisk(machineId=VM1_id, diskId=bd_id)

        self.lg('- expected error raised %s' % e.exception.status_code)
        self.assertEqual(e.exception.status_code, 400)

        self.lg('Stop VM1')
        self.api.cloudapi.machines.stop(machineId=VM1_id)
        self.assertEqual(self.api.cloudapi.machines.get(machineId=VM1_id)['status'], 'HALTED')

        self.lg("Detach VM1's boot disk again, should succeed")
        response = self.api.cloudapi.machines.detachDisk(machineId=VM1_id, diskId=bd_id)
        self.assertTrue(response)
        self.assertFalse(self.api.cloudapi.machines.get(machineId=VM1_id)['disks'])

        self.lg("Start VM1, should fail")
        with self.assertRaises(HTTPError) as e:
            self.api.cloudapi.machines.start(machineId=VM1_id)

        self.lg('- expected error raised %s' % e.exception.status_code)
        self.assertEqual(e.exception.status_code, 400)

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

    def test011_restart_vm_after_migration(self):
        """ OVC_037
        *Test case for checking VM status after restarting it after migration*

        **Test Scenario:**

        #. Create a cloudspace CS1, should succeed.
        #. Create VM1,should succeed.
        #. Migrate VM1 to another node, should succeed.
        #. Make sure that VM1 is running.
        #. Restart VM1 and make sure it is still running.

        """
        self.lg('%s STARTED' % self._testID)

        self.lg("Create VM1,should succeed.")
        vm1_id = self.cloudapi_create_machine(cloudspace_id=self.cloudspace_id)
        self.assertTrue(vm1_id)
        current_stackId = self.api.cloudbroker.machine.get(machineId=vm1_id)["stackId"]

        self.lg("Migrate VM1 to another node, should succeed.")
        second_node = self.get_running_stackId(current_stackId)
        if not second_node:
            self.skipTest('[*] Not enough running nodes ')
        self.api.cloudbroker.machine.moveToDifferentComputeNode(machineId=vm1_id, reason="test",
                                                                targetStackId=second_node, force=True)
        self.assertEqual(self.api.cloudbroker.machine.get(machineId=vm1_id)["stackId"], second_node)

        self.lg("Make sure that VM1 is running.")
        self.assertEqual(self.api.cloudapi.machines.get(machineId=vm1_id)['status'], 'RUNNING')
        vm1_conn = self.get_vm_connection(vm1_id)
        self.assertIn('bin', vm1_conn.run('ls /'))

        self.lg("Restart VM1 and make sure it is still running.")
        self.api.cloudapi.machines.reset(machineId=vm1_id)
        time.sleep(2)
        self.assertEqual(self.api.cloudapi.machines.get(machineId=vm1_id)['status'], 'RUNNING')
        vm1_conn = self.get_vm_connection(vm1_id)
        self.assertIn('bin', vm1_conn.run('ls /'))

        self.lg('%s ENDED' % self._testID)

    def test012_check_cloned_vm(self):
        """ OVC-029
        *Test case for checking cloned VM ip, portforwards and credentials*
        **Test Scenario:**
        #. Create (VM1), should succeed.
        #. Create portforward to ssh port for (VM1).
        #. Take a snapshot (SS0) for (VM1).
        #. Write file (F1) on (VM1).
        #. Stop (VM1), should succeed.
        #. Clone VM1 as (VM2_C), should succeed.
        #. Start (VM1), should succeed
        #. Make sure VM2_C got a new ip.
        #. Make sure no portforwards have been created.
        #. Check that file (F1) exists.
        #. Rollback (VM2_C) to snapshot (SS1), should fail.
        """
        self.lg('%s STARTED' % self._testID)

        self.lg('Create (VM1), should succeed')
        machineId = self.cloudapi_create_machine(self.cloudspace_id)
        machine_1_ipaddress = self.wait_for_machine_to_get_ip(machineId)
        self.assertTrue(machine_1_ipaddress)

        self.lg('Create portforward to ssh port for (VM1)')
        self.get_vm_ssh_publicport(machineId, wait_vm_ip=False)

        self.lg('Take a snapshot (SS0) for (VM1)')
        snapshotId = self.api.cloudapi.machines.snapshot(machineId=machineId, name='test-snapshot')
        snapshotEpoch = self.api.cloudapi.machines.listSnapshots(machineId=machineId)[0]['epoch']

        self.lg('Write file to (VM1)')
        machine_1_connection = self.get_vm_connection(machineId, wait_vm_ip=False)
        machine_1_connection.run('touch helloWorld.txt')

        self.lg('Stop (VM1), should succeed')
        self.api.cloudapi.machines.stop(machineId=machineId)

        self.lg('Clone VM1 as (VM2_C), should succeed')
        cloned_vm_id = self.api.cloudapi.machines.clone(machineId=machineId, name='test')
        cloned_machine_ipaddress = self.wait_for_machine_to_get_ip(cloned_vm_id)
        self.assertTrue(cloned_machine_ipaddress)

        self.lg('Start (VM1), should succeed')
        self.api.cloudapi.machines.start(machineId=machineId)

        self.lg("Make sure VM2_C got a new ip")
        self.assertNotEqual(machine_1_ipaddress, cloned_machine_ipaddress)

        self.lg("Make sure no portforwards have been created")
        portforwarding = self.api.cloudapi.portforwarding.list(cloudspaceId=self.cloudspace_id, machineId=cloned_vm_id)
        self.assertEqual(portforwarding, [])

        self.lg('Check that file (F1) exists')
        cloned_machine_connection = self.get_vm_connection(cloned_vm_id, wait_vm_ip=False)
        response = cloned_machine_connection.run('ls | grep helloWorld.txt')
        self.assertIn('helloWorld.txt', response)

        self.lg('Rollback (VM2_C) to snapshot (SS1), shoud fail')
        snapshots = self.api.cloudapi.machines.listSnapshots(machineId=cloned_vm_id)
        self.assertEqual(snapshots, [])

        with self.assertRaises(HTTPError) as e:
             self.api.cloudapi.machines.rollbackSnapshot(machineId=cloned_vm_id, epoch=snapshotEpoch)

        self.lg('%s ENDED' % self._testID)

    def test014_check_disk_iops_limit(self):
        """ OVC-046
        *Test case for checking cloned VM ip, portforwards and credentials*
        **Test Scenario:**
        #. Create virtual machine (VM1), should succeed.
        #. Attach data disk (DD1) to VM1 and set MaxIOPS to iops1.
        #. Run fio on DD1, iops should be less than iops1.
        #. Change DD1's MaxIOPS limit to iops2 which is double iops1.
        #. Run fio on DD1 again, iops should be between iops1 and iops2.
        """
        self.lg('%s STARTED' % self._testID)

        def get_iops(vm_connection, run_name):
            fio_cmd = "fio --ioengine=libaio --group_reporting --direct=1 --filename=/dev/vdb "\
                      "--runtime=30 --readwrite=rw --rwmixwrite=5 --size=500M --name=test{0} "\
                      "--output={0}".format(run_name)
            vm1_conn.sudo(fio_cmd)
            out1 = vm1_conn.sudo("cat %s | grep -o 'iops=[0-9]\{1,\}' | cut -d '=' -f 2" % run_name)
            iops_list = out1.split('\r\n')
            return iops_list

        self.lg("Create virtual machine (VM1), should succeed.")
        images = self.api.cloudapi.images.list()
        image_id = [i['id'] for i in images if 'Ubuntu' in i['name']]
        if not image_id:
            self.skipTest('No Ubuntu image found')
        vm1_id = self.cloudapi_create_machine(self.cloudspace_id, image_id=image_id[0])
        vm1_ip = self.wait_for_machine_to_get_ip(vm1_id)
        self.assertTrue(vm1_ip)

        self.lg("Attach data disk (DD1) to VM1 and set MaxIOPS to iops1.")
        maxiops = 500
        disk_id = self.create_disk(self.account_id, maxiops=maxiops)
        response = self.api.cloudapi.machines.attachDisk(machineId=vm1_id, diskId=disk_id)
        self.assertTrue(response)

        self.lg("Run fio on DD1, iops should be less than iops1.")
        vm1_conn = self.get_vm_connection(vm1_id, wait_vm_ip=False)
        vm1_conn.sudo('apt-get update')
        vm1_conn.sudo('apt-get install fio -y')
        iops_list = get_iops(vm1_conn, 'b1')
        self.assertFalse([True for i in iops_list if int(i) > maxiops])

        self.lg("Change DD1's MaxIOPS limit to iops2 which is double iops1.")
        response = self.api.cloudapi.disks.limitIO(diskId=disk_id, iops=2 * maxiops)
        self.assertTrue(response)

        self.lg("Run fio on DD1 again, iops should be between iops1 and iops2.")
        iops_list = get_iops(vm1_conn, 'b2')
        self.assertTrue([True for i in iops_list if maxiops < int(i) < 2 * maxiops])

        self.lg('%s ENDED' % self._testID)
