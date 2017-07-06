from test_cases.base_test import BaseTest


class TestSearch(BaseTest):
    def test07_search_for_resource_pool(self):
        """ ZDT-007
        *GET:/providers/resource_pools/{poolid}*

        **Test Scenario:**

        #. Create new resource pool with default parameters
        #. Get this resource pool details, should be identical
        """
        resource_pool_response = self.providers.create_resource_pool()
        self.assertEqual(resource_pool_response.status_code, 201, resource_pool_response.content)

        resource_pool_details_response = self.search.list_resource_pools(poolid=resource_pool_response.json()['UID'])
        self.assertEqual(resource_pool_details_response.status_code, 200)
        self.assertTrue(resource_pool_details_response.json(), resource_pool_response.json())
