import time, random
from testcases import *

class LibCloudBasicTests(TestcasesBase):

    def setUp(self):
        super().setUp()   
        response = self.api.cloudapi.locations.list()
        self.assertEqual(response.status_code, 200)

        locations = response.json()
        if not locations:
            self.skipTest('No locations were found in the environment')
        
        self._location = random.choice(locations)
        self.location = self._location['name'] 
        self.gid = self._location['gid']
        
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

    def test03_register_release_network_id_range(self):
        """ OVC-003
        #. Create account (AC1), should succeed.
        #. Create cloudspace (CS1), should succeed.
        #. Register network id, should succeed.
        #. Register network id in range of deployed networkids, should fail
        #. Register network id of invalid grid id, should fail.
        #. Register network id of invalid start value, should fail.
        """
        self.lg.info('Create account (AC1), should succeed')
        data, response = self.api.cloudbroker.account.create(username=self.whoami)
        self.assertEqual(response.status_code, 200, response.content)
        account_id = int(response.text)
        self.CLEANUP['accounts'].append(account_id)

        self.lg.info('Create cloudspace (CS1), should succeed')
        data, response = self.api.cloudapi.cloudspaces.create(accountId=account_id, location=self.location, access=self.whoami)
        self.assertEqual(response.status_code, 200)
        cloudspace_id = int(response.text)

        for _ in range(20):
            response = self.api.cloudapi.cloudspaces.get(cloudspaceId=cloudspace_id)
            if response.json()['status'] == 'DEPLOYED':
                break
            time.sleep(5)
        else:
            self.fail('Can\'t create cloudspace')

        response = self.api.cloudbroker.cloudspace.getVFW(cloudspaceId=cloudspace_id)
        self.assertEqual(response.status_code, 200)
        network_id = int(response.json()['id'])
        
        self.lg.info('Register network id, should succeed')
        data, response = self.api.libcloud.libvirt.registerNetworkIdRange(gid=self.gid)
        self.assertIn(response.status_code, [200, 409])

        self.lg.info('Register network id in range of deployed networkids, should fail')
        data, response = self.api.libcloud.libvirt.registerNetworkIdRange(gid=self.gid, start=network_id-1, end=network_id+1)
        self.assertEqual(response.status_code, 409)

        self.lg.info('Register network id of invalid grid id, should fail')
        gid = self.utils.random_string()
        data, response = self.api.libcloud.libvirt.registerNetworkIdRange(gid=gid)
        self.assertEqual(response.status_code, 400)

        self.lg.info('Register network id of invalid start value, should fail')
        start = self.utils.random_string()
        data, response = self.api.libcloud.libvirt.registerNetworkIdRange(gid=self.gid, start=start)
        self.assertEqual(response.status_code, 400)

        self.lg.info('Register network id of invalid end value, should fail')
        end = self.utils.random_string()
        data, response = self.api.libcloud.libvirt.registerNetworkIdRange(gid=self.gid, end=end)
        self.assertEqual(response.status_code, 400)

    def test04_store_retreive_info(self):
        """ OVC-004
        #. Store info without timeout, should succeed.
        #. Retreive info, should succeed.
        #. Retreive info and reset, should succeed.
        #. Retreive info again, info should be null.
        #  Store info with timeout, should succeed.
        #. Retreive info before timeout, should useds.
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

        self.lg.info('Retreive info before timeout, should useds')
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
