from test_suite.orchestrator_objects.orchestrator_apis import *


class VDisksAPIs:
    def __init__(self, orchestrator_client):
        self.orchestrator_client = orchestrator_client

    @catch_exception_decoration
    def get_vdisks(self):
        return self.orchestrator_client.vdisks.ListVdisks()

    @catch_exception_decoration
    def post_vdisks(self, data):
        return self.orchestrator_client.vdisks.CreateNewVdisk(data=data)

    @catch_exception_decoration
    def get_vdisks_vdiskid(self, vdiskid):
        return self.orchestrator_client.vdisks.GetVdiskInfo(vdiskid=vdiskid)

    @catch_exception_decoration
    def delete_vdisks_vdiskid(self, vdiskid):
        return self.orchestrator_client.vdisks.DeleteVdisk(vdiskid=vdiskid)

    @catch_exception_decoration
    def post_vdisks_vdiskid_resize(self, vdiskid, data):
        return self.orchestrator_client.vdisks.ResizeVdisk(vdiskid=vdiskid, data=data)

    @catch_exception_decoration
    def post_vdisks_vdiskid_rollback(self, vdiskid, data):
        return self.orchestrator_client.vdisks.RollbackVdisk(vdiskid=vdiskid, data=data)
