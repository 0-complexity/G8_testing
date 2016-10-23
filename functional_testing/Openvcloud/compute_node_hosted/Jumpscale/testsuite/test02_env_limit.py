# coding=utf-8
import uuid
import time
import unittest

from ..utils.utils import BasicACLTest


class EnvironmentLimitTest(BaseTest):
    def test001_environment_cloudspaces_limit(self):
        """ JS-001
        *Test case for environment cloudspaces limit.*

        **Test Scenario:**

        #. step1
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