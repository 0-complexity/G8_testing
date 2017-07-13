from orchestrator_objects.orchestrator_apis import *

class BridgesAPI:
    def __init__(self, orchestrator_driver):
        self.orchestrator_driver = orchestrator_driver
        self.orchestrator_client = self.orchestrator_driver.orchestrator_client
        self.createdbridges = []

    @catch_exception_decoration
    def get_nodes_bridges(self, nodeid):
        return self.orchestrator_client.nodes.ListBridges(nodeid=nodeid)

    @catch_exception_decoration
    def get_nodes_bridges_bridgeid(self, nodeid, bridgeid):
        return self.orchestrator_client.nodes.GetBridge(nodeid=nodeid, bridgeid=bridgeid)

    @catch_exception_decoration
    def post_nodes_bridges(self, nodeid, data):
        response = self.orchestrator_client.nodes.CreateBridge(nodeid=nodeid, data=data)
        if response.status_code == 201:
            self.createdbridges.append({"node": nodeid, "name": data["name"]})
        return response

    @catch_exception_decoration
    def delete_nodes_bridges_bridgeid(self, nodeid, bridgeid):
        response = self.orchestrator_client.nodes.DeleteBridge(nodeid=nodeid, bridgeid=bridgeid)
        if response.status_code == 204:
            self.createdbridges.remove({"node": nodeid, "name": bridgeid})
        return response
