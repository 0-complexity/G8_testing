from api_testing.grid_apis.grid_api_base import GridAPIBase


class StoragepoolsAPI(GridAPIBase):
    def __init__(self):
        super(StoragepoolsAPI, self).__init__()

    def get_nodes_nodeid_storagepools(self, nodeid):
        method = 'get'
        api = ['nodes', nodeid, 'storagepools']
        return self.request_api(method=method,
                                api=api)

    def post_nodes_nodeid_storagepools(self, nodeid, body):
        method = 'post'
        api = ['nodes', nodeid, 'storagepools']
        return self.request_api(method=method,
                                api=api,
                                body=body)

    def get_nodes_nodeid_storagepools_storagepoolname(self, nodeid, storagepoolname):
        method = 'get'
        api = ['nodes', nodeid, 'storagepools', storagepoolname]
        return self.request_api(method=method,
                                api=api)

    def delete_nodes_nodeid_storagepools_storagepoolname(self, nodeid, storagepoolname):
        method = 'delete'
        api = ['nodes', nodeid, 'storagepools', storagepoolname]
        return self.request_api(method=method,
                                api=api)

    def get_nodes_nodeid_storagepools_storagepoolname_devices(self, nodeid, storagepoolname):
        method = 'get'
        api = ['nodes', nodeid, 'storagepools', storagepoolname, 'devices']
        return self.request_api(method=method,
                                api=api)

    def post_nodes_nodeid_storagepools_storagepoolname_devices(self, nodeid, storagepoolname, body):
        method = 'post'
        api = ['nodes', nodeid, 'storagepools', storagepoolname, 'devices']
        return self.request_api(method=method,
                                api=api,
                                body=body)

    def get_nodes_nodeid_storagepools_storagepoolname_devices_deviceid(self, nodeid, storagepoolname):
        method = 'get'
        api = ['nodes', nodeid, 'storagepools', storagepoolname, 'devices']
        return self.request_api(method=method,
                                api=api)

    def delete_nodes_nodeid_storagepools_storagepoolname_devices_deviceid(self, nodeid, storagepoolname, deviceid,
                                                                          body):
        method = 'delete'
        api = ['nodes', nodeid, 'storagepools', storagepoolname, 'devices', deviceid]
        return self.request_api(method=method,
                                api=api,
                                body=body)

    def get_nodes_nodeid_storagepools_storagepoolname_filesystems(self, nodeid, storagepoolname):
        method = 'get'
        api = ['nodes', nodeid, 'storagepools', storagepoolname, 'filesystems']
        return self.request_api(method=method,
                                api=api)

    def post_nodes_nodeid_storagepools_storagepoolname_filesystems(self, nodeid, storagepoolname, body):
        method = 'post'
        api = ['nodes', nodeid, 'storagepools', storagepoolname, 'filesystems']
        return self.request_api(method=method,
                                api=api,
                                body=body)

    def get_nodes_nodeid_storagepools_storagepoolname_filesystems_filesystemname(self, nodeid, storagepoolname,
                                                                                 filesystemname):
        method = 'get'
        api = ['nodes', nodeid, 'storagepools', storagepoolname, 'filesystems', filesystemname]
        return self.request_api(method=method,
                                api=api)

    def delete_nodes_nodeid_storagepools_storagepoolname_filesystems_filesystemname(self, nodeid, storagepoolname,
                                                                                    filesystemname):
        method = 'delete'
        api = ['nodes', nodeid, 'storagepools', storagepoolname, 'filesystems', filesystemname]
        return self.request_api(method=method,
                                api=api)

    def get_nodes_nodeid_storagepools_storagepoolname_filesystems_filesystemname_snapshots(self, nodeid,
                                                                                           storagepoolname,
                                                                                           filesystemname):
        method = 'get'
        api = ['nodes', nodeid, 'storagepools', storagepoolname, 'filesystems', filesystemname, 'snapshots']
        return self.request_api(method=method,
                                api=api)

    def post_nodes_nodeid_storagepools_storagepoolname_filesystems_filesystemname_snapshots(self, nodeid,
                                                                                            storagepoolname,
                                                                                            filesystemname, body):
        method = 'post'
        api = ['nodes', nodeid, 'storagepools', storagepoolname, 'filesystems', filesystemname, 'snapshots']
        return self.request_api(method=method,
                                api=api,
                                body=body)

    def get_nodes_nodeid_storagepools_storagepoolname_filesystems_filesystemname_snapshots_snapshotname(self, nodeid,
                                                                                                        storagepoolname,
                                                                                                        filesystemname,
                                                                                                        snapshotname):
        method = 'get'
        api = ['nodes', nodeid, 'storagepools', storagepoolname, 'filesystems', filesystemname, 'snapshots',
               snapshotname]
        return self.request_api(method=method,
                                api=api)

    def delete_nodes_nodeid_storagepools_storagepoolname_filesystems_filesystemname_snapshots_snapshotname(self, nodeid,
                                                                                                           storagepoolname,
                                                                                                           filesystemname,
                                                                                                           snapshotname):
        method = 'delete'
        api = ['nodes', nodeid, 'storagepools', storagepoolname, 'filesystems', filesystemname, 'snapshots',
               snapshotname]
        return self.request_api(method=method,
                                api=api)

    def post_nodes_nodeid_storagepools_storagepoolname_filesystems_filesystemname_snapshots_snapshotname_rollback(self,
                                                                                                                  nodeid,
                                                                                                                  storagepoolname,
                                                                                                                  filesystemname,
                                                                                                                  snapshotname,
                                                                                                                  rollback,
                                                                                                                  body):
        method = 'post'
        api = ['nodes', nodeid, 'storagepools', storagepoolname, 'filesystems', filesystemname, 'snapshots',
               snapshotname, rollback]
        return self.request_api(method=method,
                                api=api,
                                body=body)
