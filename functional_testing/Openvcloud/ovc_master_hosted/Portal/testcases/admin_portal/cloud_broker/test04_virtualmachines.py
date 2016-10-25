import time
import unittest
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.framework import Framework


class VirtualmachinesTests(Framework):
    def setUp(self):
        super(VirtualmachinesTests, self).setUp()
        self.Login.Login(username=self.admin_username, password=self.admin_password)

    def test01_VirtualmachinesTests_page_paging_table(self):
        """ PRTL-036
        *Test case to make sure that paging and sorting of Virtualmachines page are working as expected*

        **Test Scenario:**
        #. go to Virtualmachines page.
        #. get number of Virtualmachines
        #. try paging from the available page numbers and verify it should succeed
        """
        self.lg('%s STARTED' % self._testID)
        self.VirtualMachines.get_it()
        self.assertTrue(self.VirtualMachines.is_at())

        table_paging_options = [25, 50, 100, 10]
        table_info = self.Tables.get_table_info('table cloudbroker vmachine info')
        table_number_max_number = int(table_info[(table_info.index('f') + 2):(table_info.index('entries') - 1)])

        for table_paging_option in table_paging_options:
            self.select('account selector', table_paging_option)
            time.sleep(5)
            table_info_ = self.Tables.get_table_info('table cloudbroker vmachine info')
            table_number_max_number_ = int(table_info_[table_info_.index('f') + 2:table_info_.index('en') - 1])
            table_avaliable_ = int(table_info_[(table_info_.index('to') + 3):(table_info_.index('of') - 1)])
            self.assertEqual(table_number_max_number, table_number_max_number_)
            if table_number_max_number > table_paging_option:
                self.assertEqual(table_avaliable_, table_paging_option)
            else:
                self.assertLess(table_avaliable_, table_paging_option)

    def test05_VirtualmachinesTests_page_table_paging_buttons(self):
        """ PRTL-034
        *Test case to make sure that paging and sorting of virtual machines page are working as expected*

        **Test Scenario:**
        #. go to virtual machines page.
        #. get number of virtual machines
        #. try paging from start/previous/next/last and verify it should succeed
        """
        self.lg('%s STARTED' % self._testID)
        self.VirtualMachines.get_it()
        self.assertTrue(self.VirtualMachines.is_at())

        table_max_number = self.Tables.get_table_max_number('table cloudbroker vmachine info')
        pagination = self.get_list_items('pagination')

        for _ in range((len(pagination) - 3)):
            table_start_number = self.Tables.get_table_start_number('table cloudbroker vmachine info')
            table_end_number = self.Tables.get_table_end_number('table cloudbroker vmachine info')
            previous_button, next_button = self.Tables.get_previous_next_button()

            next_button.click()
            time.sleep(1)

            table_start_number_ = self.Tables.get_table_start_number('table cloudbroker vmachine info')
            table_end_number_ = self.Tables.get_table_end_number('table cloudbroker vmachine info')

            self.assertEqual(table_start_number_, table_start_number + 10)
            if table_end_number_ < table_max_number:
                self.assertEqual(table_end_number_, table_end_number + 10)
            else:
                self.assertEqual(table_end_number_, table_max_number)

    def test06_VirtualmachinesTests_page_table_sorting(self):
        """ PRTL-035
        *Test case to make sure that paging and sorting of virtual machines page are working as expected*

        **Test Scenario:**
        #. go to virtual machines page.
        #. get number of virtual machines
        #. sorting of all fields of virtual machines table, should be working as expected
        """
        self.lg('%s STARTED' % self._testID)
        self.VirtualMachines.get_it()
        self.assertTrue(self.VirtualMachines.is_at())

        table_head_elements = self.get_table_head_elements()
        self.assertNotEqual(table_head_elements, False)

        for column_order in range(len(table_head_elements)):
            table_head_elements = self.get_table_head_elements()
            element = table_head_elements[column_order]
            element.click()
            sorting_item = element.text
            time.sleep(1)
            table_before = self.Tables.get_table_data('table cloudbroker vmachine info')

            table_head_elements = self.get_table_head_elements()
            element = table_head_elements[column_order]
            element.click()
            element.click()
            table_after = self.Tables.get_table_data('table cloudbroker vmachine info')

            self.assertEqual(len(table_before), len(table_after),
                             'The length of table is changing according to sorting by %s, %s != %s' % (
                             sorting_item, len(table_before), len(table_after)))

            for temp in range(len(table_before)):
                self.assertEqual(table_before[temp][column_order],
                                 table_after[(len(table_after) - temp - 1)][column_order])

            self.lg('pass %s' % sorting_item)
