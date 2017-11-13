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
