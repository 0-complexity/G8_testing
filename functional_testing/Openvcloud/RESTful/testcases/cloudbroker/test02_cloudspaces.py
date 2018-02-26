from testcases import *
from nose_parameterized import parameterized


class cloudspace(TestcasesBase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self):
        super().setUp()
        self.lg.info(" [*] Create account")
        self.user = self.whoami
        self.account, self.response = self.api.cloudbroker.account.create(self.user)
        self.assertEqual(self.response.status_code, 200)

        self.lg.info(" [*] Create cloudspace.")
        self.api.cloudbroker.cloudspace.create(accountId=self.account, location=self.location(),
                                                access=self.user)

    def tearDown(self):
        super().tearDown()

    def test001_addExtraIP(self):
        """ OVC-000
        *Test case for adding user to account with read access.*

        **Test Scenario:**
        #. Create Cloudspace [cs1].
        #. Add wrong IP, should fail.
        #. Add Extra IP on cloudspace[cs1], should succeed.
        #. Check thar IP added to cloudspace [CS1], should succeed.
        """
        pass

    @parameterized.expand(['read', 'write', 'admin'])
    def test002_add_user_to_cloudspace(self, accesstype):
        """ OVC-000
        *Test case for adding user to cloudspace with different accesstypes.*

        **Test Scenario:**

        #. Create two users [u1],[u2].
        #. Create cloudspace [cs1] for user[U1] and get cloudspace with user[u1],should succeed.
        #. Try get cloudspace[cs1] with user[U2], should fail.
        #. Add user[U2] to the cloudspace[cs1]with access[accesstype], should succeed.
        #. If accesstype read [R], should succeed to get cloudspace[cs1] with user[u2]
                                  , should fail to update cloudspace[cs1] name or delete it.
        #. If accesstype write [RCX], should succeed to get cloudspace[cs1] and update its name
                                  , should fail to delete cloudspace[cs1].
        #. If accesstype admin [ARCXDU], should succeed to get , update and  delete cloudspace[cs1].
        """
        pass

    def test003_applyConfig_to_cloudspace(self):
        """ OVC-000
        *Test case for applying vfw rules  to cloudspace. *

        **Test Scenario:**

        #. Create cloudspace [CS1].
        #. Apply vfw rules to [CS1] with applyconfig api,should succeed.
        #. Check that vfw rules added to [CS1], should succeed.

        """
        pass

    def test004_delete_user_from_cloudspace(self):
        """ OVC-000
        *Test case for deleting user from cloudspace. *

        **Test Scenario:**
        #. Create user[U1] .
        #. Create cloudspace [CS1].
        #. Delete non-exist user from [CS1], should fail.
        #. Delete the last admin user from [CS1], should fail.
        #. Add user[U1] to [CS1] with admin access, should succeed.
        #. Delete the main user from [CS1], should succeed. 

        """
        pass

    def test005_enable_disable_fireWall(self):
        """ OVC-000
        *Test case  for testing enable and disable virtual firewall*

        **Test Scenario:**

        #. create a cloud space
        #. deploy VFW to  the created cloudspace
        #. stop the Virtual fire wall, should succeed,
        #. start the virtual fire wall, should succeed.
        """
        pass

    def test006_create_cloudspace_with_different_options(self):
        """ OVC-000
        *Test case for testing creating account wuth different options .*

        **Test Scenario:**

        #. Create account[C1] with certain limits and max_IPs equal 1, should succeed.
        #. Create cloudspace[CS1] with passing negative values in the account's limitation, should fail.
        #. Create cloudspace[CS2] with non-exist user, should fail.
        #. Create cloudspace [CS3] that exceeds account's max_cores, should fail
        #. Create cloudspace [CS4] that exceeds account's max_memory, should fail
        #. Create cloudspace [CS5] that exceeds account's max_vdisks, should fail
        #. Create cloudspace [CS6] that exceeds account's max_IPs, should fail
        #. Create cloudspace [CS7] that doesn't exceed account's limits, should succeed.
        #. Create another cloudspace [CS8] that doesn't exceed account's limits , should fail as max_IPs equal 1.
        
        """
        pass
