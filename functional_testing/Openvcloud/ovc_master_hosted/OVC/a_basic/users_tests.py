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

        #. Create [User1] with admin access.
        #. Authenticate [User1] with POST /cloudapi/users/authenticate API,should return session key[user1_key] .
        #. Use [User1_key] to list accounts for [User1], should succeed.
        #. Use [User1_key] to update [User1] password, should succeed.
        #. Check that password of user1 reset successfully.

        """

    def test002_get_user_info(self):
        """ OVC-000
        * Test case for check get user information.*

        **Test Scenario:**

        #. Create [User1] with admin access and Email [user1_email].
        #. Get [User1] info with /cloudapi/users/get Api, should succeed.
        #. Check that [User1] info has right Email[user1_email], should succeed.
        #. Set data for [User1] with /cloudapi/users/setData API, Should succeed.
        #. Check that this data added to [ user1] info ,should succeed.

        """

    def test003_check_matching_users(self):
        """ OVC-000
        * Test case for check get matching usernames.

        **Test Scenario:**

        #. Create user1 with random name [user1].
        #. Create user2 with name which user1 name part of it .
        #. Use user1 name to get Matching usernames with /cloudapi/users/getMatchingUsernames Api,sould succeed.
        #. Check that Userr1 and User2 in matching list, should succeed.

        """

    def test004_password_reset(self):
        """ OVC-000
        * Test case for check password reset.

        **Test Scenario:**

        #. Create user1 with Email[user1_email].
        #. Send ResetPasswordLink to [User1_email] with cloudapi/users/sendResetPasswordLink API,should succeed.
        #. Check validation of received ResetPassword token with /cloudapi/users/getResetPasswordInformation API,should succeed.
        #. Use received  ResetPassword token to  reset password, should succeed.
        #. Check that password of user1 reset successfully.


        """

    def test005_create_users_with_same_specs(self):
        """ OVC-000
        * Test case for check creation of more than one user with same specs .

        **Test Scenario:**

        #. Create user1,sould succeed .
        #. Create User2 with same name as user1, should fail .
        #. Create User3 with same Email as User1 , should fail .

        """
