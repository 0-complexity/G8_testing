import time, random
from testcases import *

class LibCloudBasicTests(TestcasesBase):

    def setUp(self):
        super().setUp()   
        response = self.api.cloudapi.locations.list()
        self.assertEqual(response.status_code, 200)

        locations = response.json()
        if not locations:
            self.skip('No locations were found in the environment')

        self.gid = random.choice([x['gid'] for x in locations])
        
    def test01_get_free_mac_address(self):
        """ OVC-001
        #. Get free mac address, should succeed.
        #. Get free mac address of invalid grid id, should fail.
        """
        self.lg.info('Get free mac address, should succeed')
        response = self.api.libcloud.libvirt.getFreeMacAddress(gid=self.gid)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.text)

        self.lg.info('Get free mac address of invalid grid id, should fail')
        gid = self.utils.random_string()
        response = self.api.libcloud.libvirt.getFreeMacAddress(gid=gid)
        self.assertEqual(response.status_code, 400)
                
    def test02_get_free_network_id(self):
        """ OVC-002
        #. Get free network id, should succeed.
        #. Get free network id of invalid grid id, should fail.
        """
        self.lg.info('Get free network id, should succeed')
        response = self.api.libcloud.libvirt.getFreeNetworkId(gid=self.gid)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.text)

        self.lg.info('Get free network id of invalid grid id, should fail')
        gid = self.utils.random_string()
        response = self.api.libcloud.libvirt.getFreeNetworkId(gid=gid)
        self.assertEqual(response.status_code, 400)

    def test03_register_network_id_range(self):
        """ OVC-004
        """
        pass

    def test04_release_network_id(self):
        """ OVC-006
        """
        pass

    def test05_register_list_vnc(self):
        """ OVC-005
        #. Register new vnc (VN1).
        #. List vncs, (VN1) should be listed.  
        """
        self.lg.info('Register new vnc (VN1)')
        url = self.utils.random_string()
        response = self.api.libcloud.libvirt.registerVNC(gid=self.gid, url=url)
        self.assertEqual(response.status_code, 200)

        self.lg.info('List vncs, (VN1) should be listed')
        response = self.api.libcloud.libvirt.listVNC(gid=self.gid)
        self.assertEqual(response.status_code, 200)
        self.assertIn(url, response.json())

    def test06_store_retreive_info(self):
        """ OVC-006
        #. Store info without timeout, should succeed.
        #. Retreive info, should succeed.
        #. Retreive info and reset, should succeed.
        #. Retreive info again, info should be null.
        #  Store info with timeout, should succeed.
        #. Retreive info before timeout, should exists.
        #. Retreive the info after the timeout, should be null.
        #. Store info with invalid timeout, should fail.
        """
        self.lg.info('Store info without timeout, should succeed')
        data = self.utils.random_string()
        response = self.api.libcloud.libvirt.storeInfo(data=data)
        key = response.text.replace('"', '')
        self.assertEqual(response.status_code, 200)

        self.lg.info('Retreive info, should succeed')
        response = self.api.libcloud.libvirt.retreiveInfo(key=key)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text.replace('"', ''), data)

        self.lg.info('Retreive info, should succeed')
        response = self.api.libcloud.libvirt.retreiveInfo(key=key, reset=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text.replace('"', ''), data)

        self.lg.info('Retreive info again, info should be null')
        response = self.api.libcloud.libvirt.retreiveInfo(key=key)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'null')

        self.lg.info('Store info timeout, should succeed')
        timeout = 3
        data = self.utils.random_string()
        response = self.api.libcloud.libvirt.storeInfo(data=data, timeout=timeout)
        key = response.text.replace('"', '')
        self.assertEqual(response.status_code, 200)

        self.lg.info('Retreive info before timeout, should exists')
        response = self.api.libcloud.libvirt.retreiveInfo(key=key, reset=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text.replace('"', ''), data)

        time.sleep(timeout)

        self.lg.info('Retreive the info after the timeout, should be null')
        response = self.api.libcloud.libvirt.retreiveInfo(key=key)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'null')

        self.lg.info('Store info with invalid timeout, should fail')
        data = self.utils.random_string()
        timeout = self.utils.random_string()
        response = self.api.libcloud.libvirt.storeInfo(data=data, timeout=timeout)
        self.assertEqual(response.status_code, 400)

