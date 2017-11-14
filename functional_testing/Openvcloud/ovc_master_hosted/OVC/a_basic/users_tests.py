import unittest
from ....utils.utils import BasicACLTest


@unittest.skip('Not Implemented')
class UsersBasicTests(BasicACLTest):

    def setUp(self):
        super(UsersBasicTests, self).setUp()
        self.acl_setup()

    def test001_authenticate_user(self):
        """ OVC-000
        * Test case for check user authentication and passsword update. *

        **Test Scenario:**

        #. Create user (U1) with admin access.
        #. Authenticate U1 with POST /cloudapi/users/authenticate API,should return session key[user1_key] .
        #. Use U1's key to list accounts for U1, should succeed.
        #. Use U1's key to update U1's password, should succeed.
        #. Check that user1's password has been reset successfully.

        """

    def test002_get_user_info(self):
        """ OVC-000
        * Test case for check get user information.*

        **Test Scenario:**

        #. Create user (U1) with admin access and Email.
        #. Get U1 info with /cloudapi/users/get Api, should succeed.
        #. Check that U1's info is right, should succeed.
        #. Set data for U1 with /cloudapi/users/setData API, Should succeed.
        #. Check that this data has been added to U1 info ,should succeed.

        """

    def test003_check_matching_users(self):
        """ OVC-000
        * Test case for check get matching usernames.

        **Test Scenario:**

        #. Create user1 with random name user1.
        #. Create user2 with name in which user1 name is part of it .
        #. Use user1 name to get matching usernames with /cloudapi/users/getMatchingUsernames Api,sould succeed.
        #. Check that userr1 and user2 in matching list, should succeed.

        """

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
        """ OVC-000
        * Test case for check creation of more than one user with same specs .

        **Test Scenario:**

        #. Create user1,sould succeed .
        #. Create User2 with same name as user1, should fail .
        #. Create User3 with same Email as User1 , should fail .

        """
