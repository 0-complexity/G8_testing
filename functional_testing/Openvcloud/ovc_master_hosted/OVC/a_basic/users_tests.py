import unittest
from ....utils.utils import BasicACLTest
import uuid
import random
from JumpScale.baselib.http_client.HttpClient import HTTPError


class UsersBasicTests(BasicACLTest):

    def setUp(self):
        super(UsersBasicTests, self).setUp()
        self.acl_setup()

    def test001_authenticate_user(self):
        """ OVC-031
        * Test case for check user authentication and passsword update. *

        **Test Scenario:**

        #. Create user (U1) with admin access.
        #. Authenticate U1 with POST /cloudapi/users/authenticate API,should return session key[user1_key] .
        #. Use U1's key to list the accounts for U1, should succeed.
        #. Use U1's key to update U1's password, should succeed.
        #. Check that user1's password has been reset successfully.
        #. Use U1's key again to list the accounts for U1, should succeed.

        """
        self.lg('%s STARTED' % self._testID)

        self.lg('- create user1 with admin access ')
        old_password = str(uuid.uuid4()).replace('-', '')[0:10]
        user1 = self.cloudbroker_user_create(group='admin', password=old_password )

        self.lg("- Authenticate U1 with POST /cloudapi/users/authenticate API,should return session key[user1_key] .")
        user1_key = self.get_authenticated_user_api(username=user1,password=old_password)
        self.assertTrue(user1_key)

        self.lg("- Use U1's key to update U1's password, should succeed.")
        new_password = str(uuid.uuid4()).replace('-', '')[0:10]
        response = user1_key.cloudapi.users.updatePassword(oldPassword=old_password,newPassword=new_password)
        self.assertIn("Your password has been changed.",response)

        self.lg("Check that user1's password has been reset successfully.")
        user1_key = self.get_authenticated_user_api(username=user1,password=new_password)
        self.assertTrue(user1_key)
        self.lg("- Use U1's key again to list the accounts for U1, should succeed.")
        accounts_list = user1_key.cloudapi.accounts.list()

        self.lg('acountlist %s' % accounts_list)
        self.assertEqual(accounts_list,[])

    @unittest.skip("https://github.com/0-complexity/openvcloud/issues/952")
    def test002_get_user_info(self):
        """ OVC-032
        * Test case for check get user information.*

        **Test Scenario:**

        #. Create user (U1) with admin access and Email.
        #. Get U1 info with /cloudapi/users/get Api, should succeed.
        #. Check that U1's info is right, should succeed.
        #. Set data for U1 with /cloudapi/users/setData API, Should succeed.
        #. Check that this data has been added to U1 info ,should succeed.

        """
        self.lg('%s STARTED' % self._testID)
        self.lg('- Create user (U1) with admin access and Email ')
        user1 = self.cloudbroker_user_create(group='admin' )
        user1_email = "%s@example.com"%user1

        self.lg("- Authenticate U1 ,sould succeed .")
        user1_key = self.get_authenticated_user_api(user1)
        self.assertTrue(user1_key)

        self.lg("- Get U1 info with /cloudapi/users/get Api, should succeed")
        response = user1_key.cloudapi.users.get(username=user1)
        self.assertIn(user1_email, response["emailaddresses"])

        self.lg("- Set data for U1 with /cloudapi/users/setData API, Should succeed.")
        data = str(uuid.uuid4()).replace('-', '')[0:10]
        response = user1_key.cloudapi.users.setData(data=data)
        self.assertTrue(response)

        self.lg(' Check that this data has been added to U1 info ,should succeed.')
        response = user1_key.cloudapi.users.get(user1)
        self.assertIn(data, response["data"])

    def test003_check_matching_users(self):
        """ OVC-033
        * Test case for check get matching usernames.

        **Test Scenario:**

        #. Create user1 with random name user1.
        #. Create user2 with name in which user1 name is part of it .
        #. Use user1 name to get matching usernames with /cloudapi/users/getMatchingUsernames Api,sould succeed.
        #. Check that userr1 ,user2   in matching list, should succeed.
        #. Delete user1 and user2 and make sure that they can't be listed.
        """
        self.lg('%s STARTED' % self._testID)

        self.lg('- Create user1 with random name . ')
        user1_name = str(uuid.uuid4()).replace('-', '')[0:10]
        self.cloudbroker_user_create(username=user1_name)

        self.lg("- Authenticate U1 ,sould succeed .")
        user1_key = self.get_authenticated_user_api(user1_name)
        self.assertTrue(user1_key)

        self.lg("- Create user2 with name in which user1 name is part of it")
        user2_name = "match%s"%user1_name
        self.cloudbroker_user_create(username=user2_name)

        self.lg("- Use user1 name to get matching usernames with /cloudapi/users/getMatchingUsernames Api,sould succeed.")
        limit = random.randint(3, 20)
        matching_users_names = self.api.cloudapi.users.getMatchingUsernames(usernameregex=user1_name, limit=limit)

        self.lg("- Check that user2 and user1  in matching list, should succeed.")
        self.assertTrue([x for x in matching_users_names if x["username"]==user2_name ])
        self.assertTrue([x for x in matching_users_names if x["username"]==user1_name ])

        self.lg("- Delete user1 and user2 and make sure that they can't be listed.")
        self.api.cloudbroker.user.delete(username=user1_name)
        self.api.cloudbroker.user.delete(username=user2_name)

        self.CLEANUP['username'].remove(user1_name)
        self.CLEANUP['username'].remove(user2_name)

        matching_users_names = self.api.cloudapi.users.getMatchingUsernames(usernameregex = user2_name)
        self.assertFalse([x for x in matching_users_names if x["username"]==user2_name ])
        self.assertFalse([x for x in matching_users_names if x["username"]==user1_name ])

    @unittest.skip('Not Implemented')
    def test004_password_reset(self):
        """ OVC-000
        * Test case for check password reset.

        **Test Scenario:**

        #. Create user1 with Email (E1).
        #. Send ResetPasswordLink to E1 with cloudapi/users/sendResetPasswordLink API,should succeed.
        #. Check validation of received ResetPassword token with /cloudapi/users/getResetPasswordInformation API,should succeed.
        #. Use received  ResetPassword token to  reset password, should succeed.
        #. Check that password of user1 has been reset successfully.


        """

    def test005_create_users_with_same_specs(self):
        """ OVC-034
        * Test case for check creation of more than one user with same specs .

        **Test Scenario:**

        #. Create user1,sould succeed .
        #. Create User2 with same name as user1, should fail .
        #. Create User3 with same Email as User1 , should fail .

        """

        self.lg('- Create user1 with random name user1. ')
        user1_name = self.cloudbroker_user_create()
        user1_emailaddress = "%s@example.com"%user1_name

        self.lg("- Create User2 with same name as user1, should fail")
        user2_emailaddress = "%s@example.com"%(str(uuid.uuid4()).replace('-', '')[0:10])
        try:
            self.api.cloudbroker.user.create(username=user1_name, emailaddress=user2_emailaddress,
                                                password=user1_name,groups=[])

        except HTTPError as e:
            self.lg('- expected error raised %s' % e.status_code)
            self.assertEqual(e.status_code, 409)

        self.lg("Create User3 with same Email as User1 , should fail . ")

        username3 = str(uuid.uuid4()).replace('-', '')[0:10]
        try:
            self.api.cloudbroker.user.create(username=username3, emailaddress=user1_emailaddress,
                                               password=user1_name, groups=[])

        except HTTPError as e:
            self.lg('- expected error raised %s' % e.status_code)
            self.assertEqual(e.status_code, 409)
