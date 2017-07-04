from unittest import TestCase
from api_objects.providers_api import Providers
from api_objects.search_api import Search


class BaseTest(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.providers = Providers()
        self.search = Search()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def compare_dict(self, original, result):
        for key in original:
            if key not in result.keys():
                return False
            else:
                if original[key] != result[key]:
                    return False
        return True