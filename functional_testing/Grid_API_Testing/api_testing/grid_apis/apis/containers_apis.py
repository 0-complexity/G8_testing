from api_testing.grid_apis.grid_api_base import GridAPIBase


class ContainersAPI(GridAPIBase):
    def __init__(self):
        super().__init__()

    def get_containers(self, node_id):
        method = 'get'
        api = ['nodes', node_id, 'containers']
        return self.request_api(method=method,
                                api=api)
    def post_containers(self, node_id, body):
        method = 'post'
        api = ['nodes', node_id, 'containers']
        return self.request_api(method=method,
                                api=api, body=body)

    def delete_containers_containerid(self, node_id, containerid):
        method = 'delete'
        api = ['nodes', node_id, 'containers', containerid]
        return self.request_api(method=method,
                                api=api)

    def get_containers_containerid(self, node_id, containerid):
        method = 'get'
        api = ['nodes', node_id, 'containers', containerid]
        return self.request_api(method=method,
                                api=api)

    def post_containers_containerid_start(self, node_id, containerid):
        method = 'post'
        api = ['nodes', node_id, 'containers', containerid, 'start']
        return self.request_api(method=method,
                                api=api)
    def post_containers_containerid_stop(self, node_id, containerid):
        method = 'post'
        api = ['nodes', node_id, 'containers', containerid, 'stop']
        return self.request_api(method=method,
                                api=api)

    def post_containers_containerid_filesystem(self, node_id, containerid, body):
        method = 'post'
        api = ['nodes', node_id, 'containers', containerid, 'filesystem']
        return self.request_api(method=method,
                                api=api, body=body)


    def get_containers_containerid_filesystem(self, node_id, containerid):
        method = 'get'
        api = ['nodes', node_id, 'containers', containerid, 'filesystem']
        return self.request_api(method=method,
                                api=api)

    def delete_containers_containerid_filesystem(self, node_id, containerid):
        method = 'delete'
        api = ['nodes', node_id, 'containers', containerid, 'filesystem']
        return self.request_api(method=method,
                                api=api)

    def get_containers_containerid_jobs(self, node_id, containerid):
        method = 'get'
        api = ['nodes', node_id, 'containers', containerid, 'jobs']
        return self.request_api(method=method,
                                api=api)

    def post_containers_containerid_jobs(self, node_id, containerid):
        method = 'post'
        api = ['nodes', node_id, 'containers', containerid, 'jobs']
        return self.request_api(method=method,
                                api=api)

    def post_containers_containerid_jobs(self, node_id, containerid):
        method = 'post'
        api = ['nodes', node_id, 'containers', containerid, 'jobs']
        return self.request_api(method=method,
                                api=api)
