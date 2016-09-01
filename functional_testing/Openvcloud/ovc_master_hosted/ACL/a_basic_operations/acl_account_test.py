# coding=utf-8
import uuid
import time
import unittest

from ....utils.utils import BasicACLTest
from JumpScale.portal.portal.PortalClient2 import ApiError


class ACLACCOUNT(BasicACLTest):
    def setUp(self):
        super(ACLACCOUNT, self).setUp()
        self.acl_setup()


class Read(ACLACCOUNT):
    def test003_account_get_with_readonly_user(self):
        """ ACL-3
        *Test case for account get api with user has read only access.*

        **Test Scenario:**

        #. create account for user1, get account with user1
        #. try get account1 with user2, should fail '403 Forbidden'
        #. add user1 to the account created by user2
        #. get account2 with user1, should succeed
        #. delete user2 account, get account2 with user1, should fail '404 Not Found'
        """
        self.lg('%s STARTED' % self._testID)

        self.lg('1- get account with user1')
        user1_account = self.account_owner_api.cloudapi.accounts.get(accountId=self.account_id)
        self.assertEqual(user1_account['id'], self.account_id)

        self.lg('2- try get account1 with user2')
        try:
            self.user_api.cloudapi.accounts.get(accountId=self.account_id)
        except ApiError as e:
            self.lg('- expected error raised %s' % e.message)
            self.assertEqual(e.message, '403 Forbidden')

        self.lg('3- add user2 to the account created by user1')
        self.api.cloudapi.accounts.addUser(accountId=self.account_id,
                                           userId=self.user,
                                           accesstype='R')

        self.lg('4- get account with user2')
        user2_account = self.user_api.cloudapi.accounts.get(accountId=self.account_id)
        self.assertEqual(user2_account['id'], self.account_id)

        self.lg('5- delete user1 account: %s' % self.account_id)
        self.api.cloudbroker.account.delete(accountId=self.account_id, reason='testing')
        self.wait_for_status('DESTROYED', self.api.cloudapi.accounts.get,
                             accountId=self.account_id)
        self.CLEANUP['accountId'].remove(self.account_id)

        self.lg('6- get account with user1')
        try:
            self.user_api.cloudapi.accounts.get(accountId=self.account_id)
        except ApiError as e:
            self.lg('- expected error raised %s' % e.message)
            self.assertEqual(e.message, '404 Not Found')

        self.lg('%s ENDED' % self._testID)

    def test004_account_list_with_readonly_user(self):
        """ ACL-4
        *Test case for account list api with user has read only access.*

        **Test Scenario:**

        #. list account with user1
        #. list account with user2
        #. add user2 to the account created by user1 with read access.
        #. list accounts with user2, should have one account
        #. delete the account, list accounts with user2, should be zero account again
        """
        self.lg('%s STARTED' % self._testID)

        self.lg('1- list accounts with user1')
        user1_accounts = self.account_owner_api.cloudapi.accounts.list()
        self.assertEqual(len(user1_accounts),
                         1,
                         'user1 should have only one account')
        self.assertEqual(user1_accounts[0]['id'], self.account_id)

        self.lg('2- list accounts with user2')
        user2_accounts = self.user_api.cloudapi.accounts.list()
        self.assertEqual(len(user2_accounts),
                         0,
                         'user2 should not have any account')

        self.lg('3- add user2 to the account created by user1 with read access')
        self.api.cloudapi.accounts.addUser(accountId=self.account_id,
                                           userId=self.user,
                                           accesstype='R')

        self.lg('4- list accounts with user2')
        user1_accounts = self.user_api.cloudapi.accounts.list()
        self.assertEqual(len(user1_accounts),
                         1,
                         'user2 should have access to one account')
        self.assertEqual(user1_accounts[0]['id'], self.account_id)

        self.lg('5- delete account: %s' % self.account_id)
        self.api.cloudbroker.account.delete(accountId=self.account_id, reason='testing')
        self.wait_for_status('DESTROYED', self.api.cloudapi.accounts.get,
                             accountId=self.account_id)

        self.CLEANUP['accountId'].remove(self.account_id)

        self.lg('6- list accounts with user2')
        user1_accounts = self.user_api.cloudapi.accounts.list()
        self.assertEqual(len(user1_accounts),
                         0,
                         'user2 should not have any account again')

        self.lg('%s ENDED' % self._testID)


class Write(ACLACCOUNT):
    def test003_cloudspace_create(self):
        """ ACL-9
        *Test case for cloudspace_create api with user has write access.*

        **Test Scenario:**

        #. create cloudspace with user1
        #. try to create cloudspace on this account using user2 api, should fail '403 Forbidden'
        #. add user2  with write access to the account created by user1
        #. create cloudspace on the account with user2, should succeed
        #. delete the account, create cloudspace with user2, should fail '404 Not Found'
        #. create cloudspace with user1, should fail with '404 Not Found'
        """
        self.lg('%s STARTED' % self._testID)
        self._cloudspaces = []
        self.lg('1- create cloudspace with user1')
        self.cloudspaceId1 = self.cloudapi_cloudspace_create(account_id=self.account_id,
                                                             location=self.location,
                                                             access=self.account_owner,
                                                             api=self.account_owner_api)
        self._cloudspaces.append(self.cloudspaceId1)
        cloudspace1 = self.account_owner_api.cloudapi.cloudspaces.get(cloudspaceId=self.cloudspaceId1)
        self.assertEqual(cloudspace1['id'], self.cloudspaceId1)

        self.lg('2- try to create cloudspace on this account using user2 api')
        try:
            self.cloudapi_cloudspace_create(account_id=self.account_id,
                                            location=self.location,
                                            access=self.user,
                                            api=self.user_api)
        except ApiError as e:
            self.lg('- expected error raised %s' % e.message)
            self.assertEqual(e.message, '403 Forbidden')

        self.lg('3- add user2  with write access to the account created by user1')
        self.api.cloudapi.accounts.addUser(accountId=self.account_id,
                                           userId=self.user,
                                           accesstype='RCX')

        self.lg('4- create cloudspace on the account with user2, should succeed')
        newcloudspaceId = self.cloudapi_cloudspace_create(account_id=self.account_id,
                                                          location=self.location,
                                                          access=self.user,
                                                          api=self.user_api)
        self._cloudspaces.append(newcloudspaceId)

        newcloudspace = self.user_api.cloudapi.cloudspaces.get(cloudspaceId=newcloudspaceId)
        self.assertEqual(newcloudspace['id'], newcloudspaceId)

        self.lg('5- delete the account: %s' % self.account_id)
        self.api.cloudbroker.account.delete(accountId=self.account_id, reason='testing')
        self.wait_for_status('DESTROYED', self.api.cloudapi.accounts.get,
                             accountId=self.account_id)
        self.CLEANUP['accountId'].remove(self.account_id)

        self.lg('6- create cloudspace with user2, should fail "404 Not Found"')
        try:
            self.cloudapi_cloudspace_create(account_id=self.account_id,
                                            location=self.location,
                                            access=self.user,
                                            api=self.user_api)
        except ApiError as e:
            self.assertEqual(e.message, '404 Not Found')
            self.lg('- expected error raised %s' % e.message)

        self.lg('7- create cloudspace with user1, should fail "404 Not Found"')
        try:
            self.cloudapi_cloudspace_create(account_id=self.account_id,
                                            location=self.location,
                                            access=self.account_owner,
                                            api=self.account_owner_api)
        except ApiError as e:
            self.assertEqual(e.message, '404 Not Found')
            self.lg('- expected error raised %s' % e.message)

        self.lg('%s ENDED' % self._testID)

    @unittest.skip("https://github.com/0-complexity/openvcloud/issues/353")
    def test004_machine_createTemplate(self):
        """ ACL-10
        *Test case for machine_createTemplate api with user has write access.*

        **Test Scenario:**

        #. create cloudspace and machine with user1
        #. use created machine1 to create machineTemplate with user1
        #. try to use created machine1 to create machineTemplate with user2, should fail '403 Forbidden'
        #. add user2 to the account created by user1 with write access.
        #. use created machine1 to create machineTemplate with user2, should succeed
        #. delete user1 account, create machineTemplate with user1, should fail '404 Not Found'
        """
        self.lg('%s STARTED' % self._testID)
        self._cloudspaces = []
        self.lg('1- create cloudspace and machine with user1')
        self.cloudspaceId1 = self.cloudapi_cloudspace_create(account_id=self.account_id,
                                                             location=self.location,
                                                             access=self.account_owner,
                                                             api=self.account_owner_api)
        self._cloudspaces.append(self.cloudspaceId1)
        self._machines = []
        machineId1 = self.cloudapi_create_machine(cloudspace_id=self.cloudspaceId1,
                                                  api=self.account_owner_api)
        self._machines.append(machineId1)
        basename1 = self.account_owner_api.cloudapi.images.list(cloudspaceId=self.cloudspaceId1)[0]['name']

        self.lg('2- use created machine1 to create machineTemplate with user1')
        self.assertTrue(self.account_owner_api.cloudapi.machines.createTemplate(machineId=machineId1,
                                                                                templatename=str(uuid.uuid4()).replace(
                                                                                    '-', '')[0:10],
                                                                                basename=basename1))

        self.lg('3- try to use created machine1 to create machineTemplate with user2')
        try:
            self.user_api.cloudapi.machines.createTemplate(machineId=machineId1,
                                                           templatename=str(uuid.uuid4()).replace('-', '')[0:10],
                                                           basename=basename1)
        except ApiError as e:
            self.lg('- expected error raised %s' % e.message)
            self.assertEqual(e.message, '403 Forbidden')

        self.lg('4- add user2 to the account created by user1')
        self.api.cloudapi.accounts.addUser(accountId=self.account_id,
                                           userId=self.user,
                                           accesstype='RCX')

        self.lg('5- use created machine1 to create machineTemplate with user2')
        self.assertTrue(self.user_api.cloudapi.machines.createTemplate(machineId=machineId1,
                                                                       templatename=str(uuid.uuid4()).replace('-', '')[
                                                                                    0:10],
                                                                       basename=basename1))
        #To Do: this step create template take time and we should wait until the image created so we can delete the account in the next step.
        time.sleep(30)
        self.lg('6- delete user1 account: %s' % self.account_id)
        self.api.cloudbroker.account.delete(accountId=self.account_id, reason='testing')
        self.wait_for_status('DESTROYED', self.api.cloudapi.accounts.get,
                             accountId=self.account_id)
        self.CLEANUP['accountId'].remove(self.account_id)

        self.lg('- use created machine1 to create machineTemplate with user1')
        try:
            self.user_api.cloudapi.machines.createTemplate(machineId=machineId1,
                                                           templatename=str(uuid.uuid4()).replace('-', '')[0:10],
                                                           basename=basename1)
        except ApiError as e:
            self.lg('- expected error raised %s' % e.message)
            self.assertEqual(e.message, '404 Not Found')

        self.lg('%s ENDED' % self._testID)


class Admin(ACLACCOUNT):
    def test003_account_add_update_delete_User(self):
        """ ACL-13
        *Test case for add/update/delete api with user has admin access.*

        **Test Scenario:**

        #. add user2 to the account created by user1 as admin
        #. get account with user2
        #. create user3
        #. add user3 to the account created by user2 with read access, should succeed
        #. update account and add user3, should succeed
        #. delete user3 from the account, should succeed
        #. delete user2 from the account
        #. get account with user2, should fail '403 Forbidden'
        #. delete account, should succeed
        #. delete admin user from the account, should succeed
        """
        self.lg('%s STARTED' % self._testID)

        self.lg('1- add user2 to the account created by user1 as admin')
        self.api.cloudapi.accounts.addUser(accountId=self.account_id,
                                           userId=self.user,
                                           accesstype='ARCXDU')

        self.lg('2- get account with user2')
        user2_account = self.user_api.cloudapi.accounts.get(accountId=self.account_id)
        self.assertEqual(user2_account['id'], self.account_id)

        self.lg('3- create user3')
        self.user3 = self.cloudbroker_user_create()

        self.lg('4- add user3 to the account created by user2 with read access')
        self.user_api.cloudapi.accounts.addUser(accountId=self.account_id,
                                                userId=self.user3,
                                                accesstype='R')

        self.lg('5- update account and add user3')
        self.user_api.cloudapi.accounts.update(accountId=self.account_id,
                                               name=self.user3)

        self.lg('6- delete user3 from the account: %s with user2' % self.account_id)
        self.user_api.cloudapi.accounts.deleteUser(accountId=self.account_id,
                                                   userId=self.user3)

        self.lg('7- delete user2 from the account: %s with user2' % self.account_id)
        self.user_api.cloudapi.accounts.deleteUser(accountId=self.account_id,
                                                   userId=self.user)

        self.lg('8- get account with user2')
        try:
            self.user_api.cloudapi.accounts.get(accountId=self.account_id)
        except ApiError as e:
            self.lg('- expected error raised %s' % e.message)
            self.assertEqual(e.message, '403 Forbidden')

        self.lg('9- delete account, should succeed')
        self.api.cloudbroker.account.delete(accountId=self.account_id, reason='test')
        self.wait_for_status('DESTROYED', self.api.cloudapi.accounts.get,
                             accountId=self.account_id)
        account = self.api.cloudapi.accounts.get(accountId=self.account_id)
        self.assertEqual('DESTROYED', account['status'])
        self.CLEANUP['accountId'].remove(self.account_id)

        self.lg('10- delete admin user from the account, should succeed')
        status = self.api.cloudbroker.user.delete(username=self.account_owner)
        self.assertEqual(True, status)
        self.CLEANUP['username'].remove(self.account_owner)

        self.lg('%s ENDED' % self._testID)