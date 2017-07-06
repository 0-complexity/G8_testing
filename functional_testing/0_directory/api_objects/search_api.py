from random import *
from api_objects.base_api import *


class Search(BaseAPI):
    @catch_exception_decoration
    def list_resource_pools(self, **kwargs):
        data = {
            "page": randint(1, 100),
            "per_page": randint(1, 100),
            "longitute": None,
            "lattitude": None,
            "address": None,
            "min_cu": None,
            "min_su": None,
            "min_tu": None,
            "uptime": None,
            "network_speed": None,
            "network_redundant": None,
            "currency": None,
            "datacenter_tier": None
        }
        data = self.update_default_data(data, kwargs=kwargs)
        return self.client.api.search.search_get(query_params=data, headers=self.headers)