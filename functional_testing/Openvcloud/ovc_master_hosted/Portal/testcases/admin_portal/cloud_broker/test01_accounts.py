import unittest
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.framework import Framework
import time


class AccountsTests(Framework):
    def setUp(self):
        super(AccountsTests, self).setUp()
        self.Login.Login(username=self.admin_username, password=self.admin_password)
        self.lg('Create new username, user:%s password:%s' % (self.username, self.password))

    @unittest.skip('bug# 496')
    def test01_edit_account(self):
        """ PRTL-023
        *Test case to make sure that edit actions on accounts are working as expected*

        **Test Scenario:**
        #. create user
        #. create account.
        #. search for it and verify it should succeed
        #. edit account parameters and verify it should succeed
        """
        self.Users.create_new_user(self.username, self.password, self.email, self.group)
        self.lg('create new account %s' % self.account)
        self.Accounts.create_new_account(self.account, self.username)
        self.Accounts.open_account_page(self.account)
        self.assertTrue(self.Accounts.account_edit_all_items(self.account))

    @unittest.skip("bug# 431 and 496")
    def test02_disable_enable_account(self):
        """ PRTL-024
        *Test case to make sure that enable/disable actions on accounts are working as expected*

        **Test Scenario:**
        #. create user
        #. create account.
        #. search for it and verify it should succeed
        #. disable account and verify it should succeed
        #. enable account and verify it should succeed
        """
        self.Users.create_new_user(self.username, self.password, self.email, self.group)
        self.lg('create new account %s' % self.account)
        self.Accounts.create_new_account(self.account, self.username)
        self.Accounts.open_account_page(self.account)
        self.assertTrue(self.Accounts.account_disable(self.account))
        self.assertTrue(self.Accounts.account_edit_all_items(self.account))
        self.assertTrue(self.Accounts.account_enable(self.account))
        self.assertTrue(self.Accounts.account_edit_all_items(self.account))

    def test03_add_account_with_decimal_limitations(self):
        """ PRTL-026
        *Test case to make sure that creating account with decimal limitations working as expected*

        **Test Scenario:**
        #. create user
        #. create account with decimal limitations.
        #. search for it and verify it should succeed
        """
        self.Users.create_new_user(self.username, self.password, self.email, self.group)
        self.lg('%s STARTED' % self._testID)
        self.lg('create new account %s with decimal limitations' % self.account)
        max_memory = '3.5'
        self.Accounts.create_new_account(self.account, self.username, max_memory=max_memory)
        self.Accounts.open_account_page(self.account)
        account_maxmemory = self.get_text("account_page_maxmemory")
        self.assertTrue(account_maxmemory.startswith(max_memory), "Account max memory is [%s]"
                                                                  " and expected is [%s]" % (
                        account_maxmemory, max_memory))
        self.lg('%s ENDED' % self._testID)

    def test04_account_page_paging_table(self):
        """ PRTL-030
        *Test case to make sure that paging and sorting of accounts page are working as expected*

        **Test Scenario:**
        #. go to accounts page.
        #. get number of accounts
        #. try paging from the available page numbers and verify it should succeed
        """
        self.lg('%s STARTED' % self._testID)
        self.Accounts.get_it()
        self.assertTrue(self.Accounts.is_at())

        account_paging_options = [25, 50, 100, 10]
        account_info = self.Accounts.get_table_info()
        account_number_max_number = int(account_info[(account_info.index('f') + 2):(account_info.index('entries') - 1)])

        for account_paging_option in account_paging_options:
            self.select('account selector', account_paging_option)
            time.sleep(5)
            account_info_ = self.Accounts.get_table_info()
            account_number_max_number_ = int(account_info_[account_info_.index('f') + 2:account_info_.index('en') - 1])
            account_avaliable_ = int(account_info_[(account_info_.index('to') + 3):(account_info_.index('of') - 1)])
            self.assertEqual(account_number_max_number, account_number_max_number_)
            if account_number_max_number > account_paging_option:
                self.assertEqual(account_avaliable_, account_paging_option)
            else:
                self.assertLess(account_avaliable_, account_paging_option)

    def test05_account_page_table_paging_buttons(self):
        """ PRTL-031
        *Test case to make sure that paging and sorting of accounts page are working as expected*

        **Test Scenario:**
        #. go to accounts page.
        #. get number of accounts
        #. try paging from start/previous/next/last and verify it should succeed
        """
        self.lg('%s STARTED' % self._testID)
        self.Accounts.get_it()
        self.assertTrue(self.Accounts.is_at())

        account_max_number = self.Accounts.get_account_max_number()
        pagination = self.get_list_items('pagination')

        for _ in range((len(pagination) - 3)):
            account_start_number = self.Accounts.get_account_start_number()
            account_end_number = self.Accounts.get_account_end_number()
            previous_button, next_button = self.Accounts.get_previous_next_button()

            next_button.click()
            time.sleep(1)

            account_start_number_ = self.Accounts.get_account_start_number()
            account_end_number_ = self.Accounts.get_account_end_number()

            self.assertEqual(account_start_number_, account_start_number + 10)
            if account_end_number_ < account_max_number:
                self.assertEqual(account_end_number_, account_end_number + 10)
            else:
                self.assertEqual(account_end_number_, account_max_number)

    @unittest.skip("BUG# 509")
    def test06_account_page_table_sorting(self):
        """ PRTL-032
        *Test case to make sure that paging and sorting of accounts page are working as expected*

        **Test Scenario:**
        #. go to accounts page.
        #. get number of accounts
        #. sorting of all fields of accounts table, should be working as expected
        """
        self.lg('%s STARTED' % self._testID)
        self.Accounts.get_it()
        self.assertTrue(self.Accounts.is_at())

        table_head_elements = self.get_table_head_elements()
        self.assertNotEqual(table_head_elements, False)

        for element in table_head_elements:
            current_column = element.text
            element.click()
            time.sleep(3)
            column_before = self.Accounts.get_account_table_data().get(current_column)
            element.click()
            column_after = self.Accounts.get_account_table_data().get(current_column)
            self.assertEqual(len(column_before), len(column_after),
                             'The length of account table is changing according to sorting by ID')
            for temp in range(len(column_before)):
                self.assertEqual(column_before[temp], column_after[(len(column_after) - temp - 1)])
            self.lg('pass %s column' % current_column)