import random
from api_testing.testcases.testcases_base import TestcasesBase
from api_testing.grid_apis.apis.nodes_apis import NodesAPI
from api_testing.python_client.client import Client
import unittest

class TestNodeidAPI(TestcasesBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nodes_api = NodesAPI()
        self.base_test = TestcasesBase()

    def setUp(self):
        self.node_id = self.base_test.get_random_node()
        self.g8os_ip = self.config['%s_ip'%self.node_id.lower()]
        self.pyhton_client = Client(self.g8os_ip)

    def test001_list_nodes(self):
        """ GAT-001
        *GET:/node/ Expected: List of all nodes*

        **Test Scenario:**

        #. Send get nodes api request.
        #. Compare results with golden value.
        """
        self.lg.info('sendo get nodes api request ')
        response = self.nodes_api.get_nodes()

        self.lg.info('Compare results with golden value.')
        self.assertEqual(response.status_code, 200)

    def test002_get_nodes_details(self):
        """ GAT-002
        *GET:/nodes/{nodeid} - Expected: id, status, hostname*

        **Test Scenario:**

        #. Choose one random node of list of running nodes.
        #. Send get nodes/{nodeid} api request.
        #. Compare results with golden value.
        """

        self.lg.info(' Send get nodes/{nodeid} api request.')
        response = self.nodes_api.get_nodes_nodeid(node_id=self.node_id)
        self.assertEqual(response.status_code, 200)
        self.lg.info('Compare results with golden value.')

    @unittest.skip('give error on docker machine as shown"error": "result is in state (UNKNOWN_CMD): STDOUT:\n\nSTDERR:\n\n - data()"')
    def test003_list_jobs(self):
        """ GAT-003
        *GET:/nodes/{nodeid}/jobs - Expected: job list items*

        **Test Scenario:**

        #. Choose one random node of list of running nodes.
        #. Send get /nodes/{nodeid}/jobs api request.
        #. Compare results with golden value.
        """
        self.lg.info('Send get /nodes/{nodeid}/jobs api request.')
        response = self.nodes_api.get_nodes_nodeid_jobs(node_id=self.node_id)
        self.assertEqual(response.status_code, 200)
        self.lg.info('Compare results with golden value.')

    @unittest.skip('give error on docker machine as shown"error": "result is in state (UNKNOWN_CMD): STDOUT:\n\nSTDERR:\n\n - data()"')
    def test004_kill_jobs(self):
        """ GAT-004
        *DELETE:/nodes/{nodeid}/jobs *

        **Test Scenario:**

        #. Choose one random node of list of running nodes.
        #. Send get /nodes/{nodeid}/jobs api request.
        #. Check that all jobs has been killed.
        """

        self.lg.info(' Send get /nodes/{nodeid}/jobs api request.')
        status_code = self.nodes_api.delete_nodes_nodeid_jobs(node_id=self.node_id)
        self.assertEqual(status_code, 204)
        self.lg.info('Check that all jobs has been killed.')
        response = response.self.nodes_api.get_nodes_nodeid_jobs(node_id=node_id)
        jobs_list = response.json()
        for job in jobs_list:
            self.assertTrue(job['state'], 'KILLED')

    @unittest.skip('give error on docker machine as shown"error": "result is in state (UNKNOWN_CMD): STDOUT:\n\nSTDERR:\n\n - data()"')
    def test005_get_job_details(self):
        """ GAT-005
        *GET:/nodes/{nodeid}/jobs/{jobid} *

        **Test Scenario:**

        #. Choose one random node of list of running nodes.
        #. Get list of jobs of this node .
        #. Choose one of these jobs to list its details.
        #. Send get /nodes/{nodeid}/jobs/{jobid} api request.
        #. Compare response with the golden values.
        """
        self.lg.info('Get list of jobs of this node .')
        response = self.nodes_api.get_nodes_nodeid_jobs(node_id=self.node_id)
        self.assertEqual(response.status_code, 200)

        self.lg.info('Choose one of these jobs to list its details.')
        jobs_list = response.json()
        job_id = jobs_list[random.randint(0, len(jobs_list))]['id']

        self.lg.info('Send get /nodes/{nodeid}/jobs/{jobid} api request.')
        response = self.nodes_api.get_nodes_nodeid_jobs_jobid(node_id=self.node_id, job_id=job_id)
        self.assertEqual(response.status_code, 200)

        self.lg.info('Compare response with the golden values.')
        ##result ->from python client should be in form of dectionary
        # Properties= response.json()
        # for key in Properties.keys():
        #     self.assertEqual(Properties['key'],result[key])

    @unittest.skip('give error on docker machine as shown"error": "result is in state (UNKNOWN_CMD): STDOUT:\n\nSTDERR:\n\n - data()"')
    def test006_kill_specific_job(self):
        """ GAT-006
        *DELETE:/nodes/{nodeid}/jobs/{jobid} *

        **Test Scenario:**

        #. Choose one random node of list of running nodes.
        #. get list of jobs.
        #. choose one of these jobs to list its details.
        #. delete /nodes/{nodeid}/jobs/{jobid} api.
        #. verify this job has been killed.
        """
        self.lg.info('get list of jobs.')
        response = self.nodes_api.get_nodes_nodeid_jobs(node_id=self.node_id)
        self.assertEqual(response.status_code, 200)

        job_list =response.json()

        self.lg.info('choose one of these jobs to list its details.')
        job_id = job_list[random.randint(0, len(job_list)-1)]['id']

        self.lg.info(' delete /nodes/{nodeid}/jobs/{jobid} api.')
        response = self.nodes_api.get_nodes_nodeid_jobs_jobid(node_id=self.node_id, job_id=job_id)
        self.assertEqual(response.status_code, 204)

        self.lg.info(' verify this job has been killed.')
        response = self.nodes_api.get_nodes_nodeid_job_jobid(node_id=self.node_id,job_id=job_id)
        content = response.json()
        self.assertEqual(content['state'],'KILLED')

    def test007_ping_specific_node(self):
        """ GAT-007
        *POST:/nodes/{nodeid}/ping *

        **Test Scenario:**

        #. Choose one random node of list of running nodes.
        #. post /nodes/{nodeid}/ping api.
        #. check response status code.
        """
        self.lg.info('post /nodes/{nodeid}/ping api.')
        response = self.nodes_api.post_nodes_nodeid_ping(node_id=self.node_id)

        self.lg.info('check response status code.')
        self.assertEqual(response.status_code, 200)

    def test008_get_node_state(self):
        """ GAT-008
        *GET:/nodes/{nodeid}/state *

        **Test Scenario:**

        #. Choose one random node of list of running nodes.
        #. Get /nodes/{nodeid}/state api.
        #. Compare response data with the golden values.
        """
        self.lg.info(' get /nodes/{nodeid}/state api.')
        response = self.nodes_api.get_nodes_nodeid_state(node_id=self.node_id)
        self.assertEqual(response.status_code, 200)

        self.lg.info('Compare response data with the golden values.')
        ##result ->from python client should be in form of dectionary of cpu,rss,vms and swap.
        # Properties=response
        # for key in Properties.keys():
        #     self.assertEqual(Properties[key],result[key])

    @unittest.skip('give error on docker machine as shown"error": "404 page not found"')
    def test009_reboot_node(self):
        """ GAT-009
        *POST:/nodes/{nodeid}/reboot *

        **Test Scenario:**

        #. Choose one random node of list of running nodes.
        #. post /nodes/{nodeid}/reboot api.
        #. verify that this node has been rebooted.
        """
        self.lg.info('post /nodes/{nodeid}/reboot api.')
        response = self.nodes_api.post_nodes_nodeid_reboot(node_id=self.node_id)
        self.assertEqual(response.status_code, 204)

        self.lg.info('verify that this node has been rebooted.')
        content = response.json()
        self.assertEqual(content,'Machine reboot signal sent successfully')

    @unittest.skip("https://github.com/g8os/core0/issues/168")
    def test010_get_cpus_details(self):
        """ GAT-010
        *GET:/nodes/{nodeid}/cpus *

        **Test Scenario:**

        #. Choose one random node from list of running nodes.
        #. get /nodes/{nodeid}/cpus api.
        #. compare response data with the golden values.
        """
        self.lg.info('get /nodes/{nodeid}/cpus api.')
        response = self.nodes_api.get_nodes_nodeid_cpus(node_id=self.node_id)
        self.assertEqual(response.status_code, 200)

        self.lg.info('compare response data with the golden values.')
        result = self.pyhton_client.get_nodes_cpus()

        cpus_info = response.json()
        for i, cpu_info in enumerate(cpus_info):
            for key in cpu_info.keys():
                self.assertEqual(cpu_info[key], result[i][key],'cpu_info[%s]=%s'%(key,cpu_info[key]))


    def test011_get_disks_details(self):
        """ GAT-011
        *GET:/nodes/{nodeid}/disks *

        **Test Scenario:**

        #. Choose one random node from list of running nodes.
        #. Get /nodes/{nodeid}/disks api.
        #. Compare response data with the golden values.
        """
        self.lg.info('get /nodes/{nodeid}/disks api.')
        response = self.nodes_api.get_nodes_nodeid_disks(node_id=self.node_id)
        self.assertEqual(response.status_code, 200)
        disks_info=response.json()
        self.lg.info('compare response data with the golden values.')
        # result = self.pyhton_client.get_nodes_disks()
        # for i, disk_info in enumerate(disks_info):
        #     for key in disk_info.keys():
        #         self.assertEqual(disk_info[key], result[i][key])


    def test012_get_memmory_details(self):
        """ GAT-012
        *GET:/nodes/{nodeid}/mem *

        **Test Scenario:**

        #. Choose one random node from list of running nodes.
        #. get /nodes/{nodeid}/mem api.
        #. compare response data with the golden values.
        """
        self.lg.info('get /nodes/{nodeid}/mem api.')
        response = self.nodes_api.get_nodes_nodeid_mem(node_id=self.node_id)
        self.assertEqual(response.status_code, 200)

        self.lg.info('compare response data with the golden values.')
        result = self.pyhton_client.get_nodes_mem()
        memory_info = response.json()
        # for key in memory_info.keys():
        #     self.assertEqual(memory_info[key], result[key])

    def test013_get_nics_details(self):
        """ GAT-013
        *GET:/nodes/{nodeid}/nics - network interface information*

        **Test Scenario:**

        #. Choose one random node from list of running nodes.
        #. Get /nodes/{nodeid}/nics api.
        #. compare response data with the golden values.
        """
        self.lg.info('get /nodes/{nodeid}/nics api.')
        response = self.nodes_api.get_nodes_nodeid_nics(node_id=self.node_id)
        self.assertEqual(response.status_code, 200)

        self.lg.info('compare response data with the golden values.')
        result = self.pyhton_client.get_nodes_nics()
        nics_info = response.json()
        # for i, nic_info in enumerate(nics_info):
        #     for key in nic_info.keys():
        #         self.assertEqual(nic_info[key], result[i][key])
        #

    def test014_get_os_info_details(self):
        """ GAT-014
        *GET:/nodes/{nodeid}/info - os information*

        **Test Scenario:**

        #. Choose one random node from list of running nodes.
        #. Get /nodes/{nodeid}/info api.
        #. ompare response data with the golden values.
        """
        self.lg.info('Get /nodes/{nodeid}/info api.')
        response = self.nodes_api.get_nodes_nodeid_info(node_id=self.node_id)
        self.assertEqual(response.status_code, 200)

        self.lg.info('compare response data with the golden values.')
        result = self.pyhton_client.get_nodes_nics()
        # OS_info=response
        # for key in OS_info.keys:
        #     self.assertEqual(OS_info[key],result[key])

    @unittest.skip('"error": "json: cannot unmarshal number into Go struct field Process.cpu of type client.CPUStats"')
    def test015_list_processes(self):
        """ GAT-015
        *GET:/nodes/{nodeid}/process *

        **Test Scenario:**

        #. Choose one random node from list of running nodes.
        #. get /nodes/{nodeid}/processes api.
        #. compare response data with the golden values.
        """
        self.lg.info('Get /nodes/{nodeid}/process api.')
        response = self.nodes_api.get_nodes_nodeid_processes(node_id=self.node_id)
        self.assertEqual(response.status_code, 200)

        self.lg.info('compare response data with the golden values.')
        ##result ->from python client in form of dectionary .
        # processes=response
        # for process in processes:
        #     for process_info ,i in enumerate(process_info.keys()):
        #         if process_info == 'cmd':
        #             for key in process_info.keys():
        #                 self.assertEqual(process_info['key'],result[i][process_info][key])
        #         else:
        #             self.assertEqual(process[process_info],result[i][process_info])


    @unittest.skip('"error": "json: cannot unmarshal number into Go struct field Process.cpu of type client.CPUStats"')
    def test016_get_process_details(self):
        """ GAT-016
        *GET:/nodes/{nodeid}/processes/{processid} *

        **Test Scenario:**

        #. Choose one random node from list of running nodes.
        #. Get list of running processes
        #. choose one of them.
        #. Get /nodes/{nodeid}/processes/{processid} api.
        #. compare response data with the golden values.

        """
        self.lg.info('Get list of running processes')
        response = self.nodes_api.get_nodes_nodeid_processes(node_id=self.node_id)
        self.assertEqual(response.status_code, 200)
        processes_list=response.json()

        self.lg.info('Choose one of these processes to list its details.')
        process_id = processes_list[random.randint(0, len(processes_list)-1)]['pid']

        self.lg.info('Get /nodes/{nodeid}/process/{processid} api.')
        response = self.nodes_api.get_nodes_nodeid_processes_processid(node_id=self.node_id,process_id=process_id)
        self.assertEqual(response.status_code, 200)

        self.lg.info('Compare response data with the golden values.')
        ##result ->from python client in form of dectionary .
        # process=response.json()
        # for process_info in process.keys():
        #     if process_info == 'cmd':
        #         for key in process_info.keys():
        #             self.assertEqual(process_info['key'],result[process_info][key])
        #     else:
        #         self.assertEqual(process[process_info],result[process_info])

    @unittest.skip('"error": "json: cannot unmarshal number into Go struct field Process.cpu of type client.CPUStats"')
    def test017_delete_process(self):
        """ GAT-017
        *DELETE:/nodes/{nodeid}/processes/{processid} *

        **Test Scenario:**

        #. Choose one random node from list of running nodes.
        #. Get list of running processes
        #. Choose one of them.
        #. Delete /nodes/{nodeid}/processes/{processid} api.
        #. Make sure that this process has been killed.
        """
        self.lg.info('Get list of running processes')
        response = self.nodes_api.get_nodes_nodeid_process(node_id=self.node_id)
        self.assertEqual(response.status_code, 200)
        processes_list=response.json()

        self.lg.info('Choose one of these processes to list its details.')
        process_id = processes_list[random.randint(0, len(processes_list)-1)]['pid']

        self.lg.info('delete /nodes/{nodeid}/processes/{processid} api.')
        response = self.nodes_api.delete_nodes_nodeid_process_processid(node_id=self.node_id,process_id=process_id)
        self.assertEqual(response.status_code, 204)

        self.lg.info('Make sure that this process has been killed.')
        #result ->from python client in form of dectionary .
        # content=response.json()
        # self.assertEqual(content,'Job killed successfully')
        # ##check if u kill process will disappear from list or not

    @unittest.skip("list bridges don't work give invalid character '<'")
    def test018_list_bridges(self):
        """ GAT-018
        *GET:/nodes/{nodeid}/bridges *

        **Test Scenario:**

        #. Choose one random node from list of running nodes.
        #. Get /nodes/{nodeid}/bridges api.
        #. Compare response data with the golden values.

        """
        self.lg.info('Get /nodes/{nodeid}/bridge api.')
        response = self.nodes_api.get_nodes_nodeid_bridges(node_id=self.node_id)
        self.assertEqual(response.status_code, 200)

        self.lg.info('Compare response data with the golden values.')
        #result ->from python client in form of dectionary .
        # bridges_list=response.json()
        # for bridge,i in enumerate(bridges_list):
        #     for key in bridge.keys():
        #         self.assertEqual(bridge[key],result[i][key])

    @unittest.skip("in note ")
    def test019_create_bridge(self):
        """ GAT-019
        *POST:/nodes/{nodeid}/bridges *

        **Test Scenario:**

        #. Choose one random node from list of running nodes.
        #. post /nodes/{nodeid}/bridge api.
        #. compare response data with the golden values.
        #. Delete created bridge by Delete /nodes/{nodeid}/bridges/{bridgeid} api.

        """
        bridge_name = self.base_test.rand_str()
        hardwareaddress=self.base_test.randomMAC()
        nat=random.choice([True,False])
        network_setting = {'none':{},'static':{'cidr':'10.1.1.1/24'},
                        ' dnsmasq':{'cidr':'10.1.1.1/24','start':'10.1.1.2','end':'10.1.1.5'}}

        networkMode = random.choice(list(network_setting.keys()))
        settings = network_setting[networkMode]

        body={'name':bridge_name , 'hwaddr':hardwareaddress, 'networkMode':networkMode,
              'nat':nat, 'settings':settings}

        self.lg.info('post /nodes/{nodeid}/bridge api.')
        response = self.nodes_api.post_nodes_nodeid_bridges(node_id=self.node_id,body=body)
        self.assertEqual(response.status_code, 201)
        content = response().json()
        self.assertEqual(content, "Bridge created successfully")
        location=response.headers

        self.lg.info('Compare response data with the golden values.')

        self.lg.info('Remove created bridge.')
        response = self.nodes_api.delete_nodes_nodeid_bridges_bridgeid(node_id=self.node_id, bridge_id=bridge_name  )
        self.assertEqual(response.status_code, 204)
        content = response().json()
        self.assertEqual(content, "Bridge removed successfully")
    @unittest.skip("list bridges don't work give invalid character '<'")
    def test020_get_bridge_details(self):
        """ GAT-020
        *GET:/nodes/{nodeid}/bridges/{bridgeid} - network interface information*

        **Test Scenario:**

        #. Choose one random node from list of running nodes.
        #. Get bridges list.
        #. Choose one randome bridge .
        #. get /nodes/{nodeid}/bridges/{bridgeid}
        #. compare response data with the golden values.

        """
        self.lg.info('Get bridges list.')
        response = self.nodes_api.get_nodes_nodeid_bridges(node_id=self.node_id)
        self.assertEqual(response.status_code, 200)
        bridges_list = response.json()

        self.lg.info('Choose one of these bridges to list its details.')
        bridge_id = bridges_list[random.randint(0, len(bridges_list)-1)]['name']

        self.lg.info('get /nodes/{nodeid}/bridges/{bridgeid}.')
        response = self.nodes_api.get_nodes_nodeid_bridges_bridgeid(node_id=self.node_id, bridge_id=bridge_id)
        self.assertEqual(response.status_code, 200)
        bridge_info = response.json()

        self.lg.info('Compare response data with the golden values.')
        ##result ->from python client in form dectionary .
        # for key in bridge_info.keys():
        #         self.assertEqual(bridge_info[key],result[key])
