from testcases import *
from nose_parameterized import parameterized
import random
#from framework.api.client import Client


class Test(TestcasesBase):

    def setUp(self):
        super().setUp()
        self.user="{}@itsyouonline".format(self.whoami) 
        self.account,self.response=self.api.cloudbroker.accounts.create(self.user)
        self.assertEqual(self.response.status_code, 200)


    def tearDown(self):
        super().tearDown()

    # def test001_create_account_with_different_options(self):
    #     """ OVC-000
    #     *Test case for testing creating account wuth different options .*

    #     **Test Scenario:**

    #     #. Create account with passing negative values in the account's limitation, should fail.
    #     #. Create account with certain limits, should succeed.
    #     #. Create account with non-exist user, should fail.

    #     """ 
    #     self.lg.info("Create account with passing negative values in the account's limitation, should fail.")
    #     accounts_limitation={"maxMemoryCapacity":  random.randint(2,1000)*-1,
    #                          "maxVDiskCapacity": random.randint(2,1000)*-1,
    #                          "maxCPUCapacity":  random.randint(2,1000)*-1,
    #                          "maxNetworkPeerTransfer":  random.randint(2,1000)*-1,
    #                          "maxNumPublicIP":  random.randint(2,1000)*-1  }       
    #     data,response = self.api.cloudbroker.accounts.create(username=self.user, **accounts_limitation)
    #     self.assertEqual(response.status_code, 400,"A resource limit should be a positive number or -1 (unlimited).")

    #     self.lg.info("Create account with certain limits, should succeed.")
    #     accounts_limitation={"maxMemoryCapacity":  random.randint(2,1000),
    #                          "maxVDiskCapacity": random.randint(2,1000),
    #                          "maxCPUCapacity":  random.randint(2,1000),
    #                          "maxNetworkPeerTransfer":  random.randint(2,1000),
    #                          "maxNumPublicIP":  random.randint(2,1000) }          
    #     data,response = self.api.cloudbroker.accounts.create(username=self.user, **accounts_limitation)
    #     self.assertEqual(response.status_code, 200)

    #     self.lg.info(" Create account with non-exist user, should fail.")
    #     fake_user = self.utils.random_string()
    #     data,response = self.api.cloudbroker.accounts.create(username=fake_user)
    #     self.assertEqual(response.status_code, 400,"Email address is required for new users.")    
        


    @parameterized.expand([('R',200,401,401),
                           ('RCX',200,401,401),
                            ('ARCXDU',200,200,401)
                            ])
    def test002_add_user_to_account(self,accesstype,get_code,update_code,delete_code):
        """ OVC-000
        *Test case for adding user to account with different accesstypes.*

        **Test Scenario:**
   
        #. Create user [u1].
        #. Create account[C1] for main user and get this account  with main user,should succeed.
        #. Add user[U1] to [C1]with access[accesstype], should succeed.
        #. If accesstype read [R], should succeed to get account[C1] with user[U1]
                                  , should fail to update account[C1] name or delete it.
        #. If accesstype write [RCX], should succeed to get account[C1] and update its name
                                  , should fail to delete account[C1].
        #. If accesstype admin [ARCXDU], should succeed to get , update and  delete account [C1].
        """

        self.lg.info("Create user [u1].")
        user_data,response = self.api.cloudbroker.user.create(groups=["user"])

        self.lg.info("Create account[C1] for main user and get this account  with  user,should succeed.")
        auth_key = self.api.system.usermanager.authenticate(user_data["username"], user_data["password"])
        self.user_api.set_auth_header('authkey {}'.format(auth_key.json()))
        response= self.user_api.cloudapi.accounts.get(self.response.json())
        self.assertEqual(response.status_code,200)

        self.lg.info("Add user[U1] to [C1]with access[accesstype], should succeed.")
        import ipdb;ipdb.set_trace()
        data, response = self.api.cloudbroker.accounts.addUser(username=user_data["username"], accountId=self.response.json(),accesstype=accesstype)
        self.assertEqual(response.status_code, 200)

        response=self.user_api.cloudapi.accounts.get(self.response.json())
        self.assertEqual(response.status_code,get_code)

        data, response=self.user_api.cloudbroker.accounts.update(accountId=self.response.json())
        self.assertEqual(response.status_code, update_code)

        response=self.user_api.cloudbroker.accounts.delete(self.response.json())
        self.assertEqual(response.status_code,delete_code)

      
    def test03_delete_account(self):
        """ OVC-000
        *Test case for deleting account.*

        **Test Scenario:**

        #. Create account [C1] .
        #. Delete account [C1], should succeed.
        #. Try to get [C1], should fail.
        #. Delete account [C1] again, should fail.
        """
        self.lg.info("Delete account [C1], should succeed.")
        response = self.api.cloudbroker.accounts.delete(self.response.json())
        self.assertEqual(response.status_code, 200)

        self.lg.info("Try to get [C1], should fail.")
        response= self.api.cloudapi.accounts.get(self.response.json())
        self.assertEqual(self.response.status_code, 404)

        self.lg.info("Delete account [C1] again, should fail.")
        response = self.api.cloudbroker.accounts.delete(self.response.json())
        self.assertEqual(response.status_code, 404)

    def test004_delete_accounts(self):
        """ OVC-000
        *Test case for deleting multiple accounts.*

        **Test Scenario:**

        #. Create accounts [C1],[C2] , [C3] and [C4], should succeed .
        #. Delete account [C1], should succeed.
        #. Delete accounts [C1], [C2], should fail.
        #. Delete [C2] and [C3] accounts using delete acoounts api, should succeed. 
        #. Check that the four acounts deleted ,should succeed.
        """
        accounts=[self.response.json()]
        for _ in range(2):
            data,response=self.api.cloudbroker.accounts.create(self.user)
            accounts.append(response.json())
        
        response= self.api.cloudbroker.accounts.delete(accounts[0])
        self.assertEqual(response.status_code, 200)
        
        response= self.api.cloudbroker.accounts.deleteAccounts([accounts[0],accounts[1]])
        self.assertEqual(response.status_code, 404)

        response= self.api.cloudbroker.accounts.deleteAccounts([accounts[2],accounts[3]])
        self.assertEqual(response.status_code, 200)

        for accountID in accounts:
            response = self.api.cloudapi.accounts.get(accountID)
            self.assertEqual(response.status_code, 404)
       

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
        self.lg.info("Disable non-exist account, should fail.")

        response= self.api.cloudbroker.accounts.delete(self.response.json())
        self.assertEqual(response.status_code, 200)

        response= self.api.cloudbroker.accounts.disable(self.response.json())
        self.assertEqual(response.status_code, 404)

        response= self.api.cloudbroker.accounts.enable(self.response.json())
        self.assertEqual(response.status_code, 404)

        data,response=self.api.cloudbroker.accounts.create(self.user)
        response= self.api.cloudbroker.accounts.disable(response.json())
        self.assertEqual(response.status_code, 200)    

        location = self.utils.get_location()
        data,response = self.api.cloudbroker.cloudspaces.create(accountId=response.json(), location=location, access=self.user)
        self.assertTrue

    def test006_Update_account(self):
        """ OVC-000
        *Test case for Update account .*

        **Test Scenario:**       
        #. Update name of non-exist account [C1],should fail.
        #. Create account [C1].
        #. Update account [C1] name, should succeed.
        #. Check that account name updated, should succeed.
         
        """
        random_account= random.randint(3000,5000)

        self.lg.info("update non-exist account, should fail.")      
        data, response= self.api.cloudbroker.accounts.update(random_account)
        self.assertEqual(response.status_code, 404)
        
        response= self.api.cloudbroker.accounts.delete(self.response.json())
        self.assertEqual(response.status_code, 200)

        data, response= self.api.cloudbroker.accounts.update(self.response.json())
        self.assertEqual(response.status_code, 404)

        self.lg.info("Create account [C1].")
        data,response=self.api.cloudbroker.accounts.create(self.user)
        accountId = response.json()
    
        self.lg.info(" Update account [C1] name, should succeed.")
        data,response= self.api.cloudbroker.accounts.update(accountId)
        self.assertEqual(response.status_code, 200)    

        self.lg.info("Check that account name updated, should succeed.")
        response = self.api.cloudapi.accounts.get(accountId)
        self.assertEqual(data["name"], response.json()["name"])