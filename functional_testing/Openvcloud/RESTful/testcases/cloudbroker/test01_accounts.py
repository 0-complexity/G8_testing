from testcases import *

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

    def test001_add_user_with_read_access(self):
        """ OVC-000
        *Test case for adding user to account with read access.*

        **Test Scenario:**

        #. Create two users [u1],[u2].
        #. Create account [C1] for user[U1] and get account with user[u1],should succeed.
        #. Try get account[C1] with user[U2], should fail.
        #. Add user[U2] to the account[C1]with read access[R], should succeed.
        #. Get account[C1] with user[u2], should succeed.
        #. Update account[C1] name with user[U2], should fail'.
        #. Delete account[C1] with user [U2],should fail.
        """
        pass

    def test002_add_user_with_write_access(self):
        """ OVC-000
        *Test case for adding user to account with write access.*

        **Test Scenario:**

        #. Create two users [u1],[u2].
        #. Create account [C1] for user[U1] and get account with user[u1],should succeed.
        #. Try get account[C1] with user[U2], should fail.
        #. Add user[U2] to the account[C1]with write access[RCX], should succeed.
        #. Get account[C1] with user[u2], should succeed
        #. Update account[C1] name with user[U2], should succeed.
        #. Delete account[C1] with user [U2],should fail.    
 
        """
        pass

    def test003_add_user_with_admin_access(self):
        """ OVC-000
        *Test case for adding user to account with write access.*

        **Test Scenario:**

        #. Create two users [u1],[u2].
        #. Create account [C1] for user[U1] and get account with user[u1],should succeed.
        #. Try get account[C1] with user[U2], should fail.
        #. Add user[U2] to the account[C1]with admin access[ARCXDU], should succeed.
        #. Get account[C1] with user[u2], should succeed
        #. Update account[C1] name with user[U2], should succeed.
        #. Delete account[C1] with user [U2],should succeed.    
 
        """"
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



    