from test_suite.orchestrator_objects.orchestrator_apis import *


class ContainersAPI:
    def __init__(self, orchestrator_client):
        self.orchestrator_client = orchestrator_client
        self.createdcontainer = []

    @catch_exception_decoration
    def get_containers(self, nodeid):
        return self.orchestrator_client.nodes.ListContainers(nodeid=nodeid)

    @catch_exception_decoration
    def post_containers(self, nodeid, data):
        response = self.orchestrator_client.nodes.CreateContainer(nodeid=nodeid, data=data)
        if response.status_code == 201:
            self.createdcontainer.append({"node": nodeid, "name": data["name"]})
        return response

    @catch_exception_decoration
    def delete_containers_containerid(self, nodeid, containername):
        response = self.orchestrator_client.nodes.DeleteContainer(nodeid=nodeid, containername=containername)
        if response.status_code == 204:
            self.createdcontainer.remove({"node": nodeid, "name": containername})
        return response

    @catch_exception_decoration
    def get_containers_containerid(self, nodeid, containername):
        return self.orchestrator_client.nodes.GetContainer(nodeid=nodeid, containername=containername)

    @catch_exception_decoration
    def post_containers_containerid_start(self, nodeid, containername):
        return self.orchestrator_client.nodes.StartContainer(nodeid=nodeid, containername=containername, data={})

    @catch_exception_decoration
    def post_containers_containerid_stop(self, nodeid, containername):
        return self.orchestrator_client.nodes.StopContainer(nodeid=nodeid, containername=containername, data={})

    @catch_exception_decoration
    def post_containers_containerid_filesystem(self, nodeid, containername, data, params):
        return self.orchestrator_client.nodes.FileUpload(nodeid=nodeid, containername=containername, data=data,
                                                         query_params=params)

    @catch_exception_decoration
    def get_containers_containerid_filesystem(self, nodeid, containername, params):
        return self.orchestrator_client.nodes.FileDownload(nodeid=nodeid, containername=containername,
                                                           query_params=params)

    ### https://github.com/Jumpscale/go-raml/issues/280
    @catch_exception_decoration
    def delete_containers_containerid_filesystem(self, nodeid, containername, data):
        return self.orchestrator_client.nodes.FileDelete(nodeid=nodeid, containername=containername, data=data)

    @catch_exception_decoration
    def get_containers_containerid_jobs(self, nodeid, containername):
        return self.orchestrator_client.nodes.ListContainerJobs(nodeid=nodeid, containername=containername)

    @catch_exception_decoration
    def delete_containers_containerid_jobs(self, nodeid, containername):
        return self.orchestrator_client.nodes.KillAllContainerJobs(nodeid=nodeid, containername=containername)

    @catch_exception_decoration
    def get_containers_containerid_jobs_jobid(self, nodeid, containername, jobid):
        return self.orchestrator_client.nodes.GetContainerJob(nodeid=nodeid, containername=containername, jobid=jobid)

    @catch_exception_decoration
    def post_containers_containerid_jobs_jobid(self, nodeid, containername, jobid, data):
        return self.orchestrator_client.nodes.SendSignalToJob(nodeid=nodeid, containername=containername, jobid=jobid,
                                                              data=data)

    @catch_exception_decoration
    def delete_containers_containerid_jobs_jobid(self, nodeid, containername, jobid):
        return self.orchestrator_client.nodes.KillContainerJob(nodeid=nodeid, containername=containername, jobid=jobid)

    @catch_exception_decoration
    def post_containers_containerid_ping(self, nodeid, containername):
        return self.orchestrator_client.nodes.PingContainer(nodeid=nodeid, containername=containername, data={})

    @catch_exception_decoration
    def get_containers_containerid_state(self, nodeid, containername):
        return self.orchestrator_client.nodes.GetContainerState(nodeid=nodeid, containername=containername)

    @catch_exception_decoration
    def get_containers_containerid_info(self, nodeid, containername):
        return self.orchestrator_client.nodes.GetContainerOSInfo(nodeid=nodeid, containername=containername)

    @catch_exception_decoration
    def get_containers_containerid_processes(self, nodeid, containername):
        return self.orchestrator_client.nodes.ListContainerProcesses(nodeid=nodeid, containername=containername)

    @catch_exception_decoration
    def post_containers_containerid_jobs(self, nodeid, containername, data):
        return self.orchestrator_client.nodes.StartContainerJob(nodeid=nodeid, containername=containername, data=data)

    @catch_exception_decoration
    def get_containers_containerid_processes_processid(self, nodeid, containername, processid):
        return self.orchestrator_client.nodes.GetContainerProcess(nodeid=nodeid, containername=containername,
                                                                  processid=processid)

    @catch_exception_decoration
    def post_containers_containerid_processes_processid(self, nodeid, containername, processid, data):
        return self.orchestrator_client.nodes.SendSignalToProcess(nodeid=nodeid, containername=containername,
                                                                  processid=processid, data=data)

    @catch_exception_decoration
    def delete_containers_containerid_processes_processid(self, nodeid, containername, processid):
        return self.orchestrator_client.nodes.KillContainerProcess(nodeid=nodeid, containername=containername,
                                                                   processid=processid)
