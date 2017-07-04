from test_cases.base_test import BaseTest


class TestProviders(BaseTest):
    def test01_create_resource_pool(self):
        """ ZDT-001
        *POST:/providers/resource_pools*

        **Test Scenario:**

        #. Create new resource pool with default parameters
        #. Get its details, Should be identical
        """
        response = self.providers.create_resource_pool()
        data = self.providers.data
        self.assertTrue(self.compare_dict(original=data, result=response))

