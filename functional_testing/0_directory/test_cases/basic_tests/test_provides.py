from test_cases.base_test import BaseTest
from unittest import skip


class TestProviders(BaseTest):
    @skip('https://github.com/zero-os/0-directory/issues/23')
    def test01_create_resource_pool(self):
        """ ZDT-001
        *POST:/providers/resource_pools*

        **Test Scenario:**

        #. Create new resource pool with default parameters
        #. Get its details, Should be identical
        """
        response = self.providers.create_resource_pool()
        self.assertEqual(response.status_code, 201, response.status_code)
        resource_pool = response.json()
        self.assertTrue(self.compare_dict(original=self.providers.data, result=resource_pool))

    @skip('https://github.com/zero-os/0-directory/issues/23')
    def test02_list_resource_pools(self):
        """ ZDT-002
        *GET:/providers/resource_pools*

        **Test Scenario:**

        #. Create new resource pool with default parameters
        #. List the resource pools.
        #. Make sure that this list has the created resource.
        """
        resource_pool_response = self.providers.create_resource_pool()
        self.assertEqual(resource_pool_response.status_code, 201, resource_pool_response.content)
        resource_pools_response = self.providers.list_resource_pools()
        self.assertEqual(resource_pools_response.status_code, 200, resource_pools_response.content)
        for rp in resource_pools_response.json():
            if resource_pool_response.json()['UID'] == rp['UID']:
                self.assertTrue(self.compare_dict(original=resource_pool_response.json(), result=rp))
                break
        else:
            self.fail("Resource pools list doesn't have the created resource pool!")

    def test03_delete_resource_pool(self):
        """ ZDT-003
        *DEL:/providers/resource_pools*

        **Test Scenario:**

        #. Create new resource pool with default parameters
        #. Delete this resource pool
        #. List all the resource pools
        #. Make sure that this list doesn't have the created resource.
        """
        resource_pool_response = self.providers.create_resource_pool()
        self.assertEqual(resource_pool_response.status_code, 201, resource_pool_response.content)
        self.assertEqual(self.providers.delete_resource_pool(poolid=resource_pool_response.json()['UID']), 204)
        resource_pools_response = self.providers.list_resource_pools()
        self.assertEqual(resource_pools_response.status_code, 200, resource_pools_response.content)
        for rp in resource_pools_response.json():
            if resource_pool_response.json()['UID'] == rp['UID']:
                self.fail("Resource pools list still has the deleted resource pool!")

    @skip('Under implementation')
    def test04_update_resource_pool(self):
        pass

    @skip('Under implementation')
    def test05_get_resource_pool_details(self):
        pass

    @skip('Under implementation')
    def test06_list_all_nodes(self):
        pass

    @skip('Under implementation')
    def test07_search_for_resource_pool(self):
        pass

    @skip('Under implementation')
    def test08_delete_none_exist_resource_pool(self):
        pass
