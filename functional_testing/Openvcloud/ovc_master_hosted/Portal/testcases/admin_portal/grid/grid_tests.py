import re
import time
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.framework import Framework


class GridTests(Framework):

    def __init__(self, *args, **kwargs):
        super(GridTests, self).__init__(*args, **kwargs)

    def setUp(self):
        super(GridTests, self).setUp()
        self.Login.Login()

    def test001_error_condition_page(self):

        """ PRTL-021
        *Test case for checking error condition page in the admin portal

        **Test Scenario:**

        #. do login using admin username/password, should succeed
        #. click grid arrow then click on error condition
        #. check that all elements on error condition page exist
        #. check if show 10 and 25 entries works as expected
        #. click action button then click on purge
        #. select All and click on confirm, and check that all ECS are deleted
        """
        self.lg('%s STARTED' % self._testID)

        self.lg('click grid cruser then click on error condition')
        self.click('grid_arrow')
        self.click('Error_Conditions')

        self.lg('check that all elements on error condition page exist')
        self.assertEqual(self.get_text("grid_portal_header1"),"Grid Portal")
        self.assertEqual(self.get_text("error_conditions_header1"),"Error Conditions")
        self.assertEqual(self.get_text("error_conditions_header2"),"Error Conditions")
        self.assertEqual(self.get_text("ec_table_header2"),"Time Stamp")
        self.assertEqual(self.get_text("ec_table_header3"),"Error Message")
        self.assertEqual(self.get_text("ec_table_header4"),"Level")
        self.assertEqual(self.get_text("ec_table_header5"),"App name")
        self.assertEqual(self.get_text("ec_table_header6"),"Node ID")
        self.assertEqual(self.get_text("ec_table_header7"),"GID")

        self.lg('check if show 10 and 25 entries works as expected')
        def wait_until_entries_info_change():
            match2 = re.search("(\d+)\s+of", self.get_text("ec_entries_info"))
            while(int(match2.group(1)) == 10):
                match2 = re.search("(\d+)\s+of", self.get_text("ec_entries_info"))
                time.sleep(1)

        table_body_height_10 = float(self.get_size("ec_table_body")['height'])
        table_row_height = float(self.get_size("ec_table_row")['height'])
        match = re.search("([\d]*[,]*[\d]*)\s+entries", self.get_text("ec_entries_info"))
        entries_no = int(match.group(1).replace(',',''))
        if entries_no >= 10:
            self.lg('check the number of table\'s rows,  should be equal to 10')
            self.assertEqual(round(table_body_height_10/table_row_height), 10.0)
            self.lg('- select show 25 entries')
            self.click('entries_select')
            self.click('entries_select_option2')
            self.click('entries_select')
            if entries_no >= 25:
                self.lg('check the number of table\'s rows,  should be equal to 25')
                wait_until_entries_info_change()
                self.assertEqual(round(float(self.get_size("ec_table_body")['height'])
                                       /table_row_height), 25.0)
            else:
                self.lg('check the number of table\'s rows,  should be between 10 and 25')
                wait_until_entries_info_change()
                num = round(float(self.get_size("ec_table_body")['height'])/table_row_height)
                self.assertTrue(num > 10.0 and num < 25.0)
        else:
            self.lg('check the number of table\'s rows,  should be less than 10')
            self.assertTrue(round(float(self.get_size("ec_table_body")['height'])
                                  /table_row_height) < 10.0)

        self.lg('click action button then click on purge')
        self.click('ec_action_button')
        self.click('purge_button')

        self.lg('select All and click on confirm, and check that all ECS are deleted')
        self.click('action_purge_select')
        self.click('ALL_option')
        self.click('action_purge_confirm_button')
        self.assertEqual(self.get_text("ec_table_no_data_text"),"No data available in table")

        self.lg('%s ENDED' % self._testID)



