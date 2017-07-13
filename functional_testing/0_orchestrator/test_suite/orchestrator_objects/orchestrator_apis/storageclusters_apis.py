from orchestrator_objects.orchestrator_apis import *


class Storageclusters:
    def __init__(self, orchestrator_driver):
        self.orchestrator_driver = orchestrator_driver
        self.orchestrator_client = self.orchestrator_driver.orchestrator_client

    @catch_exception_decoration
    def post_storageclusters(self, data):
        return self.orchestrator_client.storageclusters.DeployNewCluster(data=data)

    @catch_exception_decoration
    def get_storageclusters(self):
        return self.orchestrator_client.storageclusters.ListAllClusters()

    @catch_exception_decoration
    def get_storageclusters_label(self, label):
        return self.orchestrator_client.storageclusters.GetClusterInfo(label=label)

    @catch_exception_decoration
    def delete_storageclusters_label(self, label):
        return self.orchestrator_client.storageclusters.KillCluster(label=label)
