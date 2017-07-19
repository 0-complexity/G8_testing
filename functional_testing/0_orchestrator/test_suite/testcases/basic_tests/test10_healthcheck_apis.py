import random
import time
import unittest
from testcases.testcases_base import TestcasesBase


class TesthealthcheckAPI(TestcasesBase):

    def test001_list_all_nodes_healthcheck(self):
        """ GAT-001
        *GET:/health/nodes/ Expected: List of all nodes health*

        **Test Scenario:**

        #. Get list of nodes .
        #. Send get list of all_nodes_healthcheck api request.
        #. Check that all nodes have health check, should succeed .
        #. Check that nodes health check status is ok .

        """
        self.lg.info("Get list of nodes . ")
        response = self.nodes_api.get_nodes()
        self.assertEqual(response.status_code, 200)
        Nodes_result = response.json()

        self.lg.info(" Send get list of all_nodes_healthcheck api request")
        response = self.healthcheck_api.get_all_nodes_health()
        self.assertEqual(response.status_code, 200)
        health_result = response.json()

        self.lg.info(" Check that all nodes have health check. ")
        self.assertEqual(len(health_result), len(Nodes_result))

        self.lg.info("Check that nodes health check status is ok")
        for health in health_result:
            health_status = [health['status'] for node in Nodes_result if node['id'] == health['id']][0]
            self.assertEqual(health_status,'OK', "Error in node %s"%(health['id']))

    def test002_get_node_healthcheck(self):
        """ GAT-002

        *GET:/health/nodes/nodeid Expected: List of all healthcheck for nodeid. *

        **Test Scenario:**

        #. Get random node .
        #. Get health status of this node, should be ok .
        #. Get node_health api request .
        #. Check that all healthchecks status is ok, should succeed .

        """
        self.lg.info("Get health status of this node, should be ok .")
        response = self.healthcheck_api.get_all_nodes_health()
        self.assertEqual(response.status_code, 200)
        health_result = response.json()
        general_health = [health for health in health_result if health['id'] == self.nodeid][0]
        self.assertEqual('OK', general_health['status'])

        self.lg.info(" Get node_health api request .")
        response = self.healthcheck_api.get_node_health(self.nodeid)
        self.assertEqual(response.status_code, 200)
        healthchecks = response.json()["healthchecks"]

        self.lg.info("Check that all healthchecks status is ok, should succeed .")
        for healthcheck in healthchecks:
            self.assertEqual(healthcheck["status"], "OK",
                             "Error in health check %s in node %s"%(healthcheck["name"], self.nodeid))
