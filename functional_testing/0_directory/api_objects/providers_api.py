from random import *
from api_objects.base_api import *


class Providers(BaseAPI):
    def __init__(self):
        super().__init__()
        self.data = ''

    @catch_exception_decoration
    def list_providers(self, **kwargs):
        self.data = {
            "page": randint(1, 100),
            "per_page": randint(1, 100)
        }
        self.data = self.update_default_data(data=self.data, kwargs=kwargs)
        return self.client.api.providers.ListProviders(query_params=self.data, headers=self.headers)

    @catch_exception_decoration
    def list_resource_pools(self, **kwargs):
        self.data = {
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
            "self.datacenter_tier": None
        }
        self.data = self.update_default_data(data=self.data, kwargs=kwargs)
        return self.client.api.providers.ListResourcePools(query_params=self.data, headers=self.headers)

    @catch_exception_decoration
    def create_resource_pool(self, **kwargs):
        self.data = {
            "network_speed": randint(50, 100),
            "network_redundant": False,
            "ipv4_nr_pub": randint(20, 199),
            "ipv4_ranges": ["212.23.52.64/27"],
            "ipv4_enabled": True,
            "ipv6_enabled": True,
            "pricing_currency": choice(["usd", "euro"]),
            "cu_planned": randint(100, 2000),
            "su_planned": randint(100, 2000),
            "tu_planned": randint(100, 2000),
            "cu_max": randint(100, 2000),
            "su_max": randint(100, 2000),
            "tu_max": randint(100, 2000),
            "self.datacenter_tier": randint(1, 4),
            "self.datacenter_uptime_sla_min": 99.95,
            "pricing": [{
                "min_nr_months": 1,
                "cu": randint(1, 50),
                "su": randint(1, 50),
                "tu": randint(1, 50)
            }, {
                "min_nr_months": 24,
                "cu": randint(1, 50),
                "su": randint(1, 50),
                "tu": randint(1, 50)
            }, {
                "min_nr_months": 36,
                "cu": randint(1, 50),
                "su": randint(1, 50),
                "tu": randint(1, 50)
            }],
            "location": {
                "name": "GIG_%i" % randint(1, 100),
                "description": "...",
                "remarks": "...",
                "longitute": 1.820115,
                "latitude": 3.092479,
                "address": "Lochristi, Belgium"
            },
            "nodes": [{
                "uid": "0cc47a740636",
                "description": "...",
                "remarks": "...",
                "nr_cu": randint(5, 50),
                "nr_su": randint(5, 50),
                "nr_tu": randint(5, 250)
            }, {
                "uid": "0cc47a740632",
                "description": "...",
                "remarks": "...",
                "nr_cu": randint(5, 50),
                "nr_su": randint(5, 50),
                "nr_tu": randint(5, 250)
            }, {
                "uid": "0cc47a740646",
                "description": "...",
                "remarks": "...",
                "nr_cu": randint(5, 50),
                "nr_su": randint(5, 50),
                "nr_tu": randint(5, 250)
            }, {
                "uid": "0cc47a740610",
                "description": "...",
                "remarks": "...",
                "nr_cu": randint(5, 50),
                "nr_su": randint(5, 50),
                "nr_tu": randint(5, 250)
            }]
        }
        self.data = self.update_default_data(data=self.data, kwargs=kwargs)
        return self.client.api.providers.CreateResourcePool(data=self.data, headers=self.headers)

    @catch_exception_decoration
    def get_resource_pool_details(self, poolid):
        return self.client.api.providers.GetResourcePool(poolid=poolid, headers=self.headers)

    @catch_exception_decoration
    def delete_resource_pool(self, poolid):
        return self.client.api.providers.DeleteResourcePool(poolid=poolid, headers=self.headers).status_code

    @catch_exception_decoration
    def update_resource_pool(self):
        return self.client.api.providers.UpdateResourcePool(headers=self.headers)

    @catch_exception_decoration
    def list_nodes(self, **kwargs):
        self.data = {
            "page": randint(1, 100),
            "per_page": randint(1, 100)
        }
        self.data = self.update_default_data(self.data, kwargs=kwargs)
        return self.client.api.providers.ListNodes(headers=self.headers, query_params=self.data)
