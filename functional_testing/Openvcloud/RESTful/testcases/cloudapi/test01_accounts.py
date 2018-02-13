from testcases import *

class Test(TestcasesBase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self):
        super().setUp()   
        
    def tearDown(self):
        super().tearDown()

    # @print_test
    def test001_create_account(self):
        """ OVC-001
        """
        print(self._testID)

    def test002_get_account(self):
        """ OVC-002
        """
        pass

    def test003_delete_account(self):
        """ OVC-003
        """
        pass

    def test004_list_accounts(self):
        """ OVC-004
        """
        pass

    def test005_add_user_to_account(self):
        """ OVC-005
        """
        pass

    def test006_delete_user_from_account(self):
        """ OVC-006
        """
        pass

    