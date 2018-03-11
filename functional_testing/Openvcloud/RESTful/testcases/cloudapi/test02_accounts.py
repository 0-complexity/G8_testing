import random, time
from testcases import *
from nose_parameterized import parameterized
from framework.api.client import Client

class PermissionsTests(TestcasesBase):
    def setUp(self):
        super().setUp()
        self.log.info('Create users (U2) with admin access')
        self.admin_api, self.admin = self.api.authenticate_user(groups=['admin'])

        self.log.info('Create users (U3) with user access')
        self.user_api, self.user = self.api.authenticate_user(groups=['user']) 

        self.CLEANUP['users'].extend([self.admin, self.user])

        self.log.info('Create Account (A1) using user (U1)')
        self.account_id = self.api.create_account()
        self.assertTrue(self.account_id)

        self.CLEANUP['accounts'].append(self.account_id)
    
    @parameterized.expand([('admin', 200), ('user', 403)])
    def test01_get_account(self, role, status_code):
        """ OVC-001
        """
        api = self.admin_api if role == 'admin' else self.user_api
        response = api.cloudapi.accounts.get(accountId=self.account_id)
        self.assertEqual(response.status_code, status_code, response.content)

    @parameterized.expand([('admin', 200), ('user', 403)])
    def test02_update_account(self, role, status_code):
        """ OVC-002
        """
        api = self.admin_api if role == 'admin' else self.user_api
        response = api.cloudapi.accounts.update(accountId=self.account_id)
        self.assertEqual(response.status_code, status_code, response.content)

    @parameterized.expand([('admin', 200), ('user', 403)])
    def test03_add_user(self, role, status_code):
        """ OVC-003
        """
        userId, userPassword = self.api.create_user()
        self.CLEANUP['users'].append(userId)
        
        api = self.admin_api if role == 'admin' else self.user_api
        response = api.cloudapi.accounts.addUser(accountId=self.account_id, userId=userId)
        self.assertEqual(response.status_code, status_code, response.content)

    @parameterized.expand([('admin', 200), ('user', 403)])
    def test04_update_user(self, role, status_code):
        """ OVC-004
        """
        userId, userPassword = self.api.create_user()
        self.CLEANUP['users'].append(userId)
        self.api.cloudapi.accounts.addUser(accountId=self.account_id, userId=userId)
        
        api = self.admin_api if role == 'admin' else self.user_api
        data, response = api.cloudapi.accounts.updateUser(accountId=self.account_id, userId=userId)
        self.assertEqual(response.status_code, status_code, response.content)

    @parameterized.expand([('admin', 200), ('user', 403)])
    def test05_delete_user(self, role, status_code):
        """ OVC-005
        """
        userId, userPassword = self.api.create_user()
        self.CLEANUP['users'].append(userId)
        self.api.cloudapi.accounts.addUser(accountId=self.account_id, userId=userId)
        
        api = self.admin_api if role == 'admin' else self.user_api
        response = api.cloudapi.accounts.deleteUser(accountId=self.account_id, userId=userId)
        self.assertEqual(response.status_code, status_code, response.content)

    @parameterized.expand([('admin', 200), ('user', 403)])
    def test06_get_consumed_cloud_units(self, role, status_code):
        """ OVC-006
        """        
        api = self.admin_api if role == 'admin' else self.user_api
        response = api.cloudapi.accounts.getConsumedCloudUnits(accountId=self.account_id)
        self.assertEqual(response.status_code, status_code, response.content)

    @parameterized.expand([('admin', 200), ('user', 403)])
    def test07_get_consumed_cloud_units_by_type(self, role, status_code):
        """ OVC-007
        """        
        api = self.admin_api if role == 'admin' else self.user_api
        response = api.cloudapi.accounts.getConsumedCloudUnitsByType(accountId=self.account_id)
        self.assertEqual(response.status_code, status_code, response.content)

    @parameterized.expand([('admin', 200), ('user', 403)])
    def test08_get_consumption(self, role, status_code):
        """ OVC-008
        """        
        now = time.time()
        delta = 60 * 60 * 3
        start = now - delta        
        end = now + delta
        
        api = self.admin_api if role == 'admin' else self.user_api
        response = api.cloudapi.accounts.getConsumption(accountId=self.account_id, start=start, end=end)
        self.assertEqual(response.status_code, status_code, response.content)

