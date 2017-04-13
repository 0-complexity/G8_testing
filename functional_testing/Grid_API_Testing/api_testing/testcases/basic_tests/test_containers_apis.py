import random
from api_testing.testcases.testcases_base import TestcasesBase
from api_testing.grid_apis.apis.nodes_apis import NodesAPI


class TestcontaineridAPI(TestcasesBase):
    def __init__(self, *args, **kwargs):
        self.nodes_api = NodesAPI()
        self.base_test = TestcasesBase()
        self.containers_api = ContainersAPI()
        self.root_url = 'https://hub.gig.tech/maxux/ubuntu1604.flist'
        self.storage = 'ardb://hub.gig.tech:16379'
        super(TestcontaineridAPI, self).__init__(*args, **kwargs)

    def setUp(self):
        self.container_name = self.base_test.rand_str()
        self.hostname = self.base_test.rand_str()
        self.body = {'id': self.container_name, 'hostname': self.hostname,
                'flist': self.root_url, 'initProcesses': [],
                'filesystems': [], 'nics': [], 'hostNetworking': 'false',
                'ports': [], 'storage': self.storage}


    def test001_list_containers(self):
        """ GAT-001
        *GET:/node/{nodeid}/containers Expected: List of all running containers *

        **Test Scenario:**

        #. Choose one random node of list of running nodes.
        #. Send get nodes/{nodeid}/containers api request.
        #. Compare results with golden value.
        """
        self.lg('Choose one random node of list of running nodes.')
        node_id = self.base_test.get_random_node()

        self.lg('Send get nodes/{nodeid}/containers api request.')
        response = self.containers_api.get_containers(node_id)
        self.assertEqual(response.status_code, 200)

        self.lg('Compare results with golden value.')
        contaiers_list = response.response_content.json()
        #result :list from python client with contaires
        self.assertEqual(len(contaiers_list), len(result),
                         'different length from apis than python client')
        for container, i in enumerate(contaiers_list):
            for key in container.keys():
                self.assertEqual(container['key'], result[i]['key'])

        ################################
            # container_Id=container['id']
            # for client_container in result:
            #     if client_container[id]==container_Id:
            #         for key in container.keys():
            #             self.assertEqual(container['key'],client_container['key'])
            #
            #         break
        ###################################################

    def test002_create_containers(self):
        """ GAT-001
        *post:/node/{nodeid}/containers Expected: create container then delete it *

        **Test Scenario:**

        #. Choose one random node of list of running nodes.
        #. Send post nodes/{nodeid}/containers api request.
        #. Compare results with golden value.
        #. Delete ctreated container,should succeed
        #. make sure that it deleted .
        """
    #    self.lg('Choose one random node of list of running nodes.')
        node_id = self.base_test.get_random_node()
    #    self.lg('Send post nodes/{nodeid}/containers api request.')
        response = self.containers_api.post_containers(node_id, self.body)
        self.assertEqual(response.status_code, 201)

    #    self.lg('Compare results with golden value.')

    #    self.lg('delete created container')
        response = self.containers_api.delete_containers_containerid(node_id, self.container_name)
        self.assertEqual(response.status_code, 204)
    #   self.lg('Make sure that it deleted ')
        response = self.containers_api.get_containers(node_id)
        containers_list = response.response_content.json()
        for container in containers_list:
            self.assertNotEqual(container['id'], self.container_name)

    def test003_get_container_details(self):
        """ GAT-001
        *get:/node/{nodeid}/containers/containerid Expected: get container details *

        **Test Scenario:**

        #. Choose one random node of list of running nodes.
        #. Choose one random conatainer of list of running containers.
        #. Get:/node/{nodeid}/containers/containerid

        """
    #   self.lg('Choose one random node of list of running nodes.')
        node_id = self.base_test.get_random_node()
    #   self.lg('Choose random container of list of running nodes')
        container_id = self.base_test.get_random_container(node_id)

        self.lg('Send get nodes/{nodeid}/containers/containerid api request.')
        response = self.containers_api.get_containers_containerid(node_id, container_id)
        self.assertEqual(response.status_code, 200)

        self.lg('Compare results with golden value.')

    def test004_stop_and_start_container(self):
        """ GAT-001
        *post:/node/{nodeid}/containers/containerid/start Expected: get container details *

        **Test Scenario:**

        #. Choose one random node of list of running nodes.
        #. Create container.
        #. post:/node/{nodeid}/containers/containerid/stop.
        #. Check that container stpoed .
        #. Post:/node/{nodeid}/containers/containerid/start.
        #. Check that container running .

        """
        #   self.lg('Choose one random node of list of running nodes.')
        node_id = self.base_test.get_random_node()
        #   self.lg('Create container ')
        response = self.containers_api.post_containers(node_id, self.body)
        self.assertEqual(response.status_code,200)
        #   self.lg('post:/node/{nodeid}/containers/containerid/stop.')
        response = self.containers_api.post_containers_containerid_stop(node_id, self.container_name)
        self.assertEqual(response.status_code,201)

        #   self.lg('Check that container stoped.')
        response = self.containers_api.get_containers_containerid(node_id, self.container_name)
        container_details = response.response_content.json()
        self.assertEqual(container_details['status'], 'halted')
        ##Check_from_python_client_too
        #   self.lg('post:/node/{nodeid}/containers/containerid/start.')
        response = self.containers_api.post_containers_containerid_start(node_id, self.container_name)
        self.assertEqual(response.status_code,201)
        #   self.lg('Check that container running.')
        response = self.containers_api.get_containers_containerid(node_id, self.container_name)
        container_details = response.response_content.json()
        self.assertEqual(container_details['status'], 'running')
        # #Check_from_python_client_too
