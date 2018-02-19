from testcases import *
from nose_parameterized import parameterized


class Test(TestcasesBase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self):
        super().setUp()   
        
    def tearDown(self):
        super().tearDown()

    def test001_create_account_with_different_options(self):
       """ OVC-000
        *Test case for testing creating account wuth different options .*

        **Test Scenario:**

        #. Create account with passing negative values in the account's limitation, should fail.
        #. Create account with certain limits, should succeed.
        #. Create account with non-exist user, should fail.

        """        
    @parameterized.expand(['read', 'write','admin'])
    def test002_add_user_to_account(self):
        """ OVC-000
        *Test case for adding user to account with different accesstypes.*

        **Test Scenario:**
   
        #. Create two users [u1],[u2].
        #. Create account[C1] for user[U1] and get this account  with user[u1],should succeed.
        #. Try get account[C1] with user[U2], should fail.
        #. Add user[U2] to [C1]with access[accesstype], should succeed.
        #. If accesstype read [R], should succeed to get account[C1] with user[u2]
                                  , should fail to update account[C1] name or delete it.
        #. If accesstype write [RCX], should succeed to get account[C1] and update its name
                                  , should fail to delete account[C1].
        #. If accesstype admin [ARCXDU], should succeed to get , update and  delete account [C1].
        """
        pass

    def test03_delete_account(self):
        """ OVC-000
        *Test case for deleting account.*

        **Test Scenario:**

        #. Create account [C1] .
        #. Delete non-exist account, should fail. 
        #. Delete account [C1], should succeed.
        #. Try to get [C1], should fail.
        """
        pass

    def test004_delete_accounts(self):
        """ OVC-000
        *Test case for deleting multiple accounts.*

        **Test Scenario:**

        #. Create accounts [C1],[C2] and [C3] .
        #. Delete [C1],[C2] and [C3] acoounts using delete acoounts api, should succeed. 
        #. Check that the three acounts deleted ,should succeed.
        """
        pass

    def test005_account_disable_and_enable(self):
        """ OVC-000
        *Test case for disable and enable account .*

        **Test Scenario:**
        #. Disable non-exist account, should fail.
        #. Enable non-exist account, should fail.
        #. Create account [C1].
        #. Disable account [C1], should succeed.
        #. Try to create cloudspace on [C1], should fail.
        #. Disable non-exist account, should fail.
        #. Enable account [C1], should succeed.
        #. Try to create cloudspace on [C1], should succeed.

        """
        pass

    def test006_Update_account(self):
        """ OVC-000
        *Test case for Update account .*

        **Test Scenario:**       
        #. Update name of non-exist account [C1],should fail.
        #. Create account [C1].
        #. Update account [C1] name, should succeed.
        #. Check that account name updated, should succeed.
         
        """
        pass
