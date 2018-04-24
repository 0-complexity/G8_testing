import unittest
from nose_parameterized import parameterized
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.framework import Framework


class StorageRoutersTests(Framework):
    def setUp(self):
        super(StorageRoutersTests, self).setUp()
        self.Login.Login(cookies_login=True)
        self.navigation_bar = 'navigation bar'
        self.lg('go to storage routers page')
        self.StorageRouters.get_it()
        self.assertTrue(self.StorageRouters.is_at())

    def test01_storagerrouters_page_basic_elements(self):
        """
        PRTL-001
        *Test case to make sure the basic elements in storage routers page as expected*

        **Test Scenario:**
        #. go to storage routers page
        #. check page url & title
        #. check navigation bar
        #. check page title
        #. check 'show records per page' list
        """
        self.lg('check page url & title')
        self.assertEqual(self.driver.title, 'CBGrid - Storage Routers')
        self.assertIn('cbgrid/Storage%20Routers', self.driver.current_url)
        self.lg('check navigation bar')
        self.assertEqual(self.get_navigation_bar(self.navigation_bar), ['Cloud Broker', 'Storage Routers'])
        self.lg('check page title')
        self.assertEqual(self.get_text('page title'), 'Storage Routers')


    def test02_storagerrouters_page_paging_table(self):
        """
        PRTL-002
        *Test case to make sure that show 'records per page' of storage routers page is working as expected*

        **Test Scenario:**
        #. go to storage routers page.
        #. try paging from the available page numbers and verify it should succeed.
        """
        self.lg('%s STARTED' % self._testID)
        self.lg('try paging from the available page numbers and verify it should succeed')
        self.assertTrue(self.Tables.check_show_list('storge_routers'))
        self.lg('%s ENDED' % self._testID)

    def test03_storagerrouters_page_table_paging_buttons(self):
        """
        PRTL-003
        *Test case to make sure that paging of storage routers page is working as expected*

        **Test Scenario:**
        #. go to storage routers page.
        #. try paging from start/previous/next/last and verify it should succeed.
        """
        self.lg('%s STARTED' % self._testID)
        self.lg('try paging from start/previous/next/last and verify it should succeed')
        self.assertTrue(self.Tables.check_next_previous_buttons('storge_routers'))
        self.lg('%s ENDED' % self._testID)

        # @parameterized.expand(['Grid ID',
        #                        'Name',
        #                        'Grid Node ID',
        #                        'IP Address'])
        # def test05_storagerrouters_table_search(self, column):
        #     """
        #     PRTL-005
        #     *Test case to make sure that searching in storage routers table is working as expected*
        #
        #     **Test Scenario:**
        #     #. go to storage routers page.
        #     #. try general search box to search for values in all columns and verfiy it return the right value
        #     #. try the search box in every column and  verfiy it return the right value
        #     """
        #     self.lg('%s STARTED' % self._testID)
        #     self.lg('try general search box to search for values in all columns and verfiy it return the right value')
        #     self.assertTrue(self.Tables.check_search_box('storge_routers', column))
        #     self.lg('try the search box in every column and verfiy it return the right value')
        #     self.assertTrue(self.Tables.check_data_filters('storge_routers', column))
        #     self.lg('%s ENDED' % self._testID)
