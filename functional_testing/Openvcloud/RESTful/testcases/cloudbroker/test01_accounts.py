from testcases import *
from nose_parameterized import parameterized
import random

class Test(TestcasesBase):

    def setUp(self):
        super().setUp()
        self.user="{}@itsyouonline".format(self.whoami) 
        self.account,response=self.api.cloudbroker.accounts.create(self.user)
        self.assertEqual(response.status_code, 200)


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
        self.lg.info("Create account with passing negative values in the account's limitation, should fail.")
        accounts_limitation={"maxMemoryCapacity":  random.randint(2,1000)*-1,
                             "maxVDiskCapacity": random.randint(2,1000)*-1,
                             "maxCPUCapacity":  random.randint(2,1000)*-1,
                             "maxNetworkPeerTransfer":  random.randint(2,1000)*-1,
                             "maxNumPublicIP":  random.randint(2,1000)*-1  }       
        data,response = self.api.cloudbroker.accounts.create(username=self.user, **accounts_limitation)
        self.assertEqual(response.status_code, 400,"A resource limit should be a positive number or -1 (unlimited).")
        
        self.lg.info("Create account with certain limits, should succeed.")
        accounts_limitation={"maxMemoryCapacity":  random.randint(2,1000),
                             "maxVDiskCapacity": random.randint(2,1000),
                             "maxCPUCapacity":  random.randint(2,1000),
                             "maxNetworkPeerTransfer":  random.randint(2,1000),
                             "maxNumPublicIP":  random.randint(2,1000) }          
        data,response = self.api.cloudbroker.accounts.create(username=self.user, **accounts_limitation)
        self.assertEqual(response.status_code, 200)

        self.lg.info(" Create account with non-exist user, should fail.")
        fake_user = self.utils.random_string()
        data,response = self.api.cloudbroker.accounts.create(username=fake_user)
        self.assertEqual(response.status_code, 400,"Email address is required for new users.")    
        

    @parameterized.expand(['read', 'write','admin'])
    def test002_add_user_to_account(self,accesstype):
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

        #. Create accounts [C1],[C2] and [C3], should succeed .
        #. Delete accounts [C1], and non-exist account, should fail.
        #. Delete [C2] and [C3] acoounts using delete acoounts api, should succeed. 
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
