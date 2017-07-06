from unittest import TestCase
from api_objects.providers_api import Providers
from api_objects.search_api import Search
from termcolor import colored


class BaseTest(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.providers = Providers()
        self.search = Search()

    def setUp(self):
        pass

    def tearDown(self):
        resource_pools = self.providers.list_resource_pools().json()
        for resource_pool in resource_pools:
            pool_id = resource_pool['UID']
            self.providers.delete_resource_pool(poolid=pool_id)

    def compare_dict(self, original, result):
        for key in original:
            if key not in result.keys():
                print(colored(" [*] Result dict miss this [ %s ] key" % key, 'red'))
                return False
            else:
                if original[key] != result[key]:
                    print(colored(" [*] original[%s] > %s != %s < result[%s]" % (key, original[key], result[key], key),
                                  'red'))
                    return False
        return True
