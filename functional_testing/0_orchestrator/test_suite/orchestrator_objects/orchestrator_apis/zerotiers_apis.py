from test_suite.orchestrator_objects.orchestrator_apis import *


class ZerotiersAPI:
    def __init__(self, orchestrator_client):
        self.orchestrator_client = orchestrator_client

    @catch_exception_decoration
    def get_nodes_zerotiers(self, nodeid):
        return self.orchestrator_client.nodes.ListZerotier(nodeid=nodeid)

    @catch_exception_decoration
    def get_nodes_zerotiers_zerotierid(self, nodeid, zerotierid):
        return self.orchestrator_client.nodes.GetZerotier(nodeid=nodeid, zerotierid=zerotierid)

    @catch_exception_decoration
    def post_nodes_zerotiers(self, nodeid, data):
        return self.orchestrator_client.nodes.JoinZerotier(nodeid=nodeid, data=data)

    @catch_exception_decoration
    def delete_nodes_zerotiers_zerotierid(self, nodeid, zerotierid):
        return self.orchestrator_client.nodes.ExitZerotier(nodeid=nodeid, zerotierid=zerotierid)
