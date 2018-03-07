from testcases import *
from nose_parameterized import parameterized
import random , unittest

class cloudspace(TestcasesBase):

    def setUp(self):
        super().setUp()
        self.log.info(" [*] Create account")
        self.user = self.whoami
        self.account, response = self.api.cloudbroker.account.create(self.user)
        self.assertEqual(response.status_code, 200)
        self.accountId = response.json()
        self.CLEANUP["accounts"].append(self.accountId)


        self.log.info(" [*] Create cloudspace.")
        self.cloudspace, response = self.api.cloudbroker.cloudspace.create(accountId=self.accountId, location=self.location,
                                                access=self.user)
        self.assertEqual(response.status_code, 200)       
        self.cloudspaceId = response.json()

    @parameterized.expand([('R',200,403,403),
                           ('RCX',200,403,200),
                            ('ARCXDU',200,200,200)
                            ])
    def test001_add_user_to_cloudspace(self,accesstype,get_code,update_code, vm_code):
        """ OVC-000
        *Test case for adding user to cloudspace with different accesstypes.*

        **Test Scenario:**
   
        #. Create user [u1].
        #. Create cloudspace[CS1] for main user and get this cloudspace  with main user,should succeed.
        #. Try to get cloudspace[CS1] with user[U1], should fail. 
        #. Add user[U1] to [CS1] with access[accesstype], should succeed.
        #. If accesstype read [R], should succeed to get cloudspace[CS1] with user[U1]
                                 , should fail to update or create  VM on it .
        #. If accesstype write [RCX], should succeed to get cloudspace[CS1] and create VM on it .
                                    , should fail to update cloudspace[CS1] name. 
        #. If accesstype admin [ARCXDU], should succeed to get , update [CS1] name and  create VM  on it. 

        """

        self.log.info("Create user [u1].")
        user_data,response = self.api.cloudbroker.user.create(groups=["user"])
        self.CLEANUP['users'].append(user_data["username"])

        self.log.info("Create cloudspace[CS1] for main user and get this cloudspace  with main user,should succeed.")
        response= self.api.cloudapi.cloudspaces.get(self.cloudspaceId)
        self.assertEqual(response.status_code,200)

        self.log.info("Try to get cloudspace[CS1] with user[U1], should fail.")
        self.user_api.system.usermanager.authenticate(user_data["username"], user_data["password"])
        response= self.user_api.cloudapi.cloudspaces.get(self.cloudspaceId)
        self.assertEqual(response.status_code,403)       

        self.log.info("Add user[U1] to [CS1] with access[accesstype], should succeed.")
        data, response = self.api.cloudbroker.cloudspace.addUser(username=user_data["username"], cloudspaceId=self.cloudspaceId,accesstype=accesstype)
        self.assertEqual(response.status_code, 200)

        self.log.info("Check that user get the right % access on cs "%accesstype)
        self.user_api.system.usermanager.authenticate(user_data["username"], user_data["password"])
        response=self.user_api.cloudapi.cloudspaces.get(self.cloudspaceId)
        self.assertEqual(response.status_code,get_code)

        data,response = self.user_api.cloudapi.machines.create(self.cloudspaceId)
        self.assertEqual(response.status_code,vm_code)

        data,response=self.user_api.cloudapi.cloudspaces.update(cloudspaceId=self.cloudspaceId)
        self.assertEqual(response.status_code, update_code)


    def test002_delete_non_exist_user_from_cloudspace(self):
        """ OVC-000
        *Test case for deleting non-exist user from cloudspace. *

        **Test Scenario:**
        #. Create cloudspace [CS1].
        #. Delete non-exist user from [CS1], should fail.
        """
        fake_user=self.utils.random_string()
        response = self.api.cloudbroker.cloudspace.deleteUser(cloudspaceId=self.cloudspaceId, username=fake_user)
        self.assertEqual(response.status_code, 404)


    def test003_delete_user_from_cloudspace(self):
        """ OVC-000
        *Test case for deleting user from cloudspace. *

        **Test Scenario:**
        #. Create user[U1] .
        #. Create cloudspace [CS1].
        #. Delete user from [CS1], should succeed. 
        #. Delete user[U1] again from [CS1] , should fail.
        """

        self.log.info("Delete  user from [CS1], should succeed.")
 
        response = self.api.cloudbroker.cloudspace.deleteUser(cloudspaceId=self.cloudspaceId, username=self.user)
        self.assertEqual(response.status_code, 200)

        self.log.info("Delete  user[U1]  again from [CS1], should fail .")
 
        response = self.api.cloudbroker.cloudspace.deleteUser(cloudspaceId=self.cloudspaceId, username=self.user)
        self.assertEqual(response.status_code, 404)

    def test004_start_stop_non_exist_fireWall(self):
        """ OVC-000
        *Test case  for testing enable and disable virtual firewall*

        **Test Scenario:**

        #. create a cloud space
        #. deploy VFW to  the created cloudspace.
        #. stop the Virtual fire wall, should succeed,
        #. start the virtual fire wall, should succeed.
        """
        fake_cloudspaceId = random.randint(3000,5000)

        response = self.api.cloudbroker.cloudspace.deployVFW(fake_cloudspaceId)
        self.assertEqual(response.status_code, 404)

        response = self.api.cloudbroker.cloudspace.startVFW(fake_cloudspaceId)
        self.assertEqual(response.status_code, 404)

        response = self.api.cloudbroker.cloudspace.stopVFW(fake_cloudspaceId)
        self.assertEqual(response.status_code, 404)


    def test005_enable_disable_fireWall(self):
        """ OVC-000
        *Test case  for testing enable and disable virtual firewall*

        **Test Scenario:**

        #. create a cloud space
        #. deploy VFW to  the created cloudspace
        #. stop the Virtual fire wall, should succeed,
        #. start the virtual fire wall, should succeed.
        """

        response = self.api.cloudbroker.cloudspace.deployVFW(self.cloudspaceId)
        self.assertEqual(response.status_code, 200)

        response = self.api.cloudbroker.cloudspace.startVFW(self.cloudspaceId)
        self.assertEqual(response.status_code, 200)

        response = self.api.cloudbroker.cloudspace.stopVFW(self.cloudspaceId)
        self.assertEqual(response.status_code, 200)       

    def test006_create_cloudspace_with_nonexist_user(self):
        """ OVC-000
        *Test case for testing creating account wuth different options .*

        **Test Scenario:*
        #. Create cloudspace[CS] with non-exist user, should fail.
        """
        fake_user = self.utils.random_string()
        data, response = self.api.cloudbroker.cloudspace.create(accountId=self.accountId, location=self.location,
                                                access=fake_user)
        self.assertEqual(response.status_code, 404)       

    @parameterized.expand([("Negative values", -1, 400),
                           ("Positive values", 1, 200)])    
    def test007_create_cloudspace_with_different_options(self, type, factor, return_code):
        """ OVC-000
        *Test case for testing creating cloudspace with different options .*

        **Test Scenario:**

        #. Create account with passing negative values in the account's limitation, should fail.
        #. Create account with certain limits, should succeed.
        """

        self.log.info("Create account with passing %s values in the cloudspace's limitation." % type)
        cloudspace_limitation = {"maxMemoryCapacity": random.randint(2, 1000) * factor,
                               "maxVDiskCapacity": random.randint(2, 1000) * factor,
                               "maxCPUCapacity": random.randint(2, 1000) * factor,
                               "maxNetworkPeerTransfer": random.randint(2, 1000) * factor,
                               "maxNumPublicIP": random.randint(2, 1000) * factor}
        data, response = self.api.cloudbroker.cloudspace.create(accountId=self.accountId, location=self.location,access=self.user, **cloudspace_limitation)
        self.assertEqual(response.status_code, return_code, "A resource limit should be a positive number or -1 (unlimited).")


    @unittest.skip("https://github.com/0-complexity/openvcloud/issues/1435")
    def test008_create_cloudspace_with_limitations(self):
        """ OVC-000
        *Test case for testing creating account wuth different options .*

        **Test Scenario:**

        #. Create account[C1] with certain limits and max_IPs equal 1, should succeed.
        #. Create cloudspace [CS2] that exceeds one of account limitations , should fail.
        #. Create cloudspace [CS3] that doesn't exceed account's limits, should succeed.
        #. Create another cloudspace [CS4] that doesn't exceed account's limits , should fail as max_IPs equal 1.
        
        """
        self.log.info("Create account[C1] with certain limits and max_IPs equal 1, should succeed.")
        account_limitation = {"maxMemoryCapacity": random.randint(2, 1000) ,
                               "maxVDiskCapacity": random.randint(2, 1000) ,
                               "maxNetworkPeerTransfer": random.randint(2, 1000) ,
                               "maxNumPublicIP": 1}        
        data, account = self.api.cloudbroker.account.create(username=self.user, **account_limitation)
        self.assertEqual(account.status_code, 200)
        self.CLEANUP['accounts'].append(account.json())

        self.log.info("Create cloudspace [CS2] that exceeds one of account limitations , should fail")
        cloudspacelimit = random.choice(list(account_limitation))
        cloudspace_limitation = {cloudspacelimit: account_limitation[cloudspacelimit]+1}
        data, response = self.api.cloudbroker.cloudspace.create(accountId=account.json(), location=self.location,access=self.user, **cloudspace_limitation)
        self.assertEqual(response.status_code, 400)

        self.log.info(" Create cloudspace [CS3] that doesn't exceed account's limits, should succeed. ")
        data, response = self.api.cloudbroker.cloudspace.create(accountId=account.json(), location=self.location,access=self.user)
        self.assertEqual(response.status_code, 200)

        self.log.info("Create another cloudspace [CS4] that doesn't exceed account's limits , should fail as max_IPs equal 1.")
        data, response = self.api.cloudbroker.cloudspace.create(accountId=account.json(), location=self.location,access=self.user)

        self.assertEqual(response.status_code, 200)       