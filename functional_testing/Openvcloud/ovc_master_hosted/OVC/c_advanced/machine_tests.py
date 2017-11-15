import unittest
from ....utils.utils import BasicACLTest


@unittest.skip('Not Implemented')
class MachineTests(BasicACLTest):

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
        """ OVC-000
        *Test case for checking network data integrity through VMS*

        **Test Scenario:**

        #. Create a cloudspace CS1, should succeed
        #. Create VM1 and VM2 inside CS1, should succeed
        #. create a file F1 inside VM1
        #. From VM1 send F1 to VM2, should succeed
        #. Check that F1 has been sent to vm2 without data loss
        """

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

    def test004_migrate_vm_in_middle_of writing_file(self):
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

    def test005_cheching_vm_specs_after_rebooting(self):
        """ OVC-000
        *Test case for checking VM's ip and credentials after rebooting*

        **Test Scenario:**

        #. Create a cloudspace CS1, should succeed
        #. Create virtual machine VM1 with windows image
        #. Reboot VM1, should succeed
        #. Check if VM1's ip is the same as before rebooting.
        #. Check if VM1's credentials are the same as well
        """

    def test006_attach_same_disk_to_two_vms(self):
        """ OVC-000
        *Test case for attaching same disk to two different vms*

        **Test Scenario:**

        #. Create disk DS1.
        #. Create cloudspace CS1.
        #. Create VM1 and VM2 on CS1.
        #. Attach DS1 to VM1, should succeed.
        #. Attach DS1 to VM2, should fail.
        #. Delete disk after detaching it, should succeed
        """
        # Note: try this scenario for data and boot disks

    def test007_detach_boot_from_running_machine(self):
        """ OVC-000
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

    def test008_swap_vms_boot_disks(self):
        """ OVC-000
        * Test case for swapping vms boot disks.

        **Test Scenario:**

        #. Create virtual machines (VM1) and (VM2).
        #. Stop VM1 and VM2, should succeed.
        #. Detach VM1's boot disk (BD1) and VM2's boot disk (BD2).
        #. Attach BD1 to VM2, should succeed.
        #. Start VM2 and make sure it is working.
        #. Attach BD2 to VM1, should succeed.
        #. Start VM1 and make sure it is working.
        """

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
        """ OVC-000
        *Test case for checking VM status after restarting it after migration*

        **Test Scenario:**

        #. Create a cloudspace CS1, should succeed.
        #. Create VM1.
        #. Migrate VM1 to another node, should succeed.
        #. Make sure that VM1 is running.
        #. Restart VM1 and make sure it is still running.
        """

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
