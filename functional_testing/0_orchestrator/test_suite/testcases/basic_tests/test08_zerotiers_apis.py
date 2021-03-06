import time, unittest
from testcases.testcases_base import TestcasesBase

@unittest.skip('https://github.com/gig-projects/org_quality/issues/686')
class TestZerotiersAPI(TestcasesBase):
    def setUp(self):
        super().setUp()
        self.lg.info(' [*] Join zerotier network (ZT0)')
        self.nw_id = self.create_zerotier_network()
        self.response, self.data = self.zerotiers_api.post_nodes_zerotiers(self.nodeid, nwid=self.nw_id)

    def tearDown(self):
        self.lg.info(' [*] Exit zerotier network (ZT0)')
        self.zerotiers_api.delete_nodes_zerotiers_zerotierid(self.nodeid, nwid=self.nw_id)
        self.delete_zerotier_network(nwid=self.nw_id)
        super(TestZerotiersAPI, self).tearDown()

    def test001_get_nodes_zerotiers_zerotierid(self):
        """ GAT-078
        **Test Scenario:**

        #. Get random nodid (N0), should succeed.
        #. Join zerotier network (ZT0).
        #. Get zerotier (ZT0) details and compare it with results from python client, should succeed with 200.
        #. Get non-existing zerotier network, should fail with 404.
        """
        self.lg.info(
            ' [*] Get zerotier (ZT0) details and compare it with results from python client, should succeed with 200')
        response = self.zerotiers_api.get_nodes_zerotiers_zerotierid(self.nodeid, nwid=self.nw_id)
        self.assertEqual(response.status_code, 200)
        zerotiers = self.core0_client.client.zerotier.list()
        zerotier_ZT0 = [x for x in zerotiers if x['nwid'] == self.nw_id]
        self.assertNotEqual(zerotier_ZT0, [])
        for key in zerotier_ZT0[0].keys():
            expected_result = zerotier_ZT0[0][key]
            if type(expected_result) == str and key != 'status':
                expected_result = expected_result.lower()
            if key in ['routes', 'id']:
                continue
            self.assertEqual(response.json()[key], expected_result, expected_result)

        self.lg.info(' [*] Get non-existing zerotier network, should fail with 404')
        response = self.zerotiers_api.get_nodes_zerotiers_zerotierid(self.nodeid, self.rand_str())
        self.assertEqual(response.status_code, 404)

    def test002_list_node_zerotiers(self):
        """ GAT-079
        **Test Scenario:**

        #. Get random nodid (N0), should succeed.
        #. Join zerotier network (ZT0).
        #. List node (N0) zerotiers networks, should succeed with 200.
        #. List zerotier networks using python client, (ZT0) should be listed
        """
        self.lg.info(' [*] Get node (N0) zerotiers networks, should succeed with 200')
        response = self.zerotiers_api.get_nodes_zerotiers(self.nodeid)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.nw_id, [x['nwid'] for x in response.json()])

        self.lg.info(' [*] List zerotier networks using python client, (ZT0) should be listed')
        zerotiers = self.core0_client.client.zerotier.list()
        self.assertIn(self.nw_id, [x['nwid'] for x in zerotiers])

    def test003_post_zerotier(self):
        """ GAT-080
        **Test Scenario:**

        #. List node (N0) zerotier networks, (ZT1) should be listed.
        #. List zerotier networks using python client, (ZT1) should be listed
        #. Leave zerotier network (ZT1), should succeed with 204.
        #. Join zerotier with invalid body, should fail with 400.
        """
        self.lg.info(' [*] List node (N0) zerotier networks, (ZT1) should be listed')
        response = self.zerotiers_api.get_nodes_zerotiers(self.nodeid)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.nw_id, [x['nwid'] for x in response.json()])

        self.lg.info(' [*] List zerotier networks using python client, (ZT1) should be listed')
        zerotiers = self.core0_client.client.zerotier.list()
        self.assertIn(self.nw_id, [x['id'] for x in zerotiers])

        self.lg.info(' [*] Leave zerotier network (ZT1), should succeed with 204')
        response = self.zerotiers_api.delete_nodes_zerotiers_zerotierid(self.nodeid, self.nw_id)
        self.assertEqual(response.status_code, 204)

        self.delete_zerotier_network(self.nw_id)

        self.lg.info(' [*] Join zerotier with invalid body, should fail with 400')
        body = {"worngparameter": self.rand_str()}
        response = self.zerotiers_api.post_nodes_zerotiers(self.nodeid, body)
        self.assertEqual(response.status_code, 400)

    def test004_leave_zerotier(self):
        """ GAT-081
        **Test Scenario:**

        #. Leave zerotier network (ZT0), should succeed with 204.
        #. List node (N0) zerotier networks, (ZT0) should be gone.
        #. List zerotier networks using python client, (ZT0) should be gone.
        #. Leave nonexisting zerotier network, should fail with 404
        """
        self.lg.info(' [*] Leave zerotier network (ZT0), should succeed with 204')
        response = self.zerotiers_api.delete_nodes_zerotiers_zerotierid(self.nodeid, nwid=self.nw_id)
        self.assertEqual(response.status_code, 204)

        self.lg.info(' [*] List node (N0) zerotier networks, (ZT0) should be gone')
        response = self.zerotiers_api.get_nodes_zerotiers(self.nodeid)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.nw_id, [x['nwid'] for x in response.json()])

        self.lg.info(' [*] List zerotier networks using python client, (ZT0) should be gone')
        zerotiers = self.core0_client.client.zerotier.list()
        self.assertNotIn(self.nw_id, [x['nwid'] for x in zerotiers])

        self.lg.info(' [*] Leave nonexisting zerotier network, should fail with 404')
        response = self.zerotiers_api.delete_nodes_zerotiers_zerotierid(self.nodeid, 'fake_zerotier')
        self.assertEqual(response.status_code, 404)
