from test_suite.orchestrator_objects.orchestrator_apis import *


class VmsAPI:
    def __init__(self, orchestrator_client):
        self.orchestrator_client = orchestrator_client

    @catch_exception_decoration
    def get_nodes_vms(self, nodeid):
        return self.orchestrator_client.nodes.ListVMs(nodeid=nodeid)

    @catch_exception_decoration
    def get_nodes_vms_vmid(self, nodeid, vmid):
        return self.orchestrator_client.nodes.GetVM(nodeid=nodeid, vmid=vmid)

    @catch_exception_decoration
    def get_nodes_vms_vmid_info(self, nodeid, vmid):
        return self.orchestrator_client.nodes.GetVMInfo(nodeid=nodeid, vmid=vmid)

    @catch_exception_decoration
    def post_nodes_vms(self, nodeid, data):
        return self.orchestrator_client.nodes.CreateVM(nodeid=nodeid, data=data)

    @catch_exception_decoration
    def put_nodes_vms_vmid(self, nodeid, vmid, data):
        return self.orchestrator_client.nodes.UpdateVM(nodeid=nodeid, vmid=vmid, data=data)

    @catch_exception_decoration
    def delete_nodes_vms_vmid(self, nodeid, vmid):
        return self.orchestrator_client.nodes.DeleteVM(nodeid=nodeid, vmid=vmid)

    @catch_exception_decoration
    def post_nodes_vms_vmid_start(self, nodeid, vmid):
        return self.orchestrator_client.nodes.StartVM(nodeid=nodeid, vmid=vmid, data={})

    @catch_exception_decoration
    def post_nodes_vms_vmid_stop(self, nodeid, vmid):
        return self.orchestrator_client.nodes.StopVM(nodeid=nodeid, vmid=vmid, data={})

    @catch_exception_decoration
    def post_nodes_vms_vmid_pause(self, nodeid, vmid):
        return self.orchestrator_client.nodes.PauseVM(nodeid=nodeid, vmid=vmid, data={})

    @catch_exception_decoration
    def post_nodes_vms_vmid_resume(self, nodeid, vmid):
        return self.orchestrator_client.nodes.ResumeVM(nodeid=nodeid, vmid=vmid, data={})

    @catch_exception_decoration
    def post_nodes_vms_vmid_shutdown(self, nodeid, vmid):
        return self.orchestrator_client.nodes.ShutdownVM(nodeid=nodeid, vmid=vmid, data={})

    @catch_exception_decoration
    def post_nodes_vms_vmid_migrate(self, nodeid, vmid, data):
        return self.orchestrator_client.nodes.MigrateVM(nodeid=nodeid, vmid=vmid, data=data)
