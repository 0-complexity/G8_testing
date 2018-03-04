import time, random, unittest
from testcases import *
from nose_parameterized import parameterized


class DisksTests(TestcasesBase):
    def setUp(self):
        super().setUp()
        self.account_id = self.api.create_account()
        self.assertTrue(self.account_id)
        self.CLEANUP['accounts'].append(self.account_id)
        self.disk_data, self.response = self.api.cloudapi.disks.create(accountId=self.account_id, gid=self.gid)
        self.assertEqual(self.response.status_code, 200, self.response.content)        
        self.diskId = int(self.response.text)

    def tearDown(self):
        self.api.cloudapi.disks.delete(diskId=self.diskId)
        super().tearDown()
    
    @parameterized.expand([
        ('exists_account', 200), 
        ('non_exists_account', 404), 
        ('invalid_account', 400)
    ])
    def test01_list_disks(self, case, response_code):
        """ OVC-001
        #. Create Account (A1), should succeed.
        #. Create disk (D1), should succeed.
        #. List account (A1) disks, (D1) should be listed. 
        """
        account_id = self.account_id

        if case == 'non_exists_account':
            account_id = random.randint(100000, 200000)
        elif case == 'invalid_account':
            account_id = self.utils.random_string()

        response = self.api.cloudapi.disks.list(accountId=account_id)
        self.assertEqual(response.status_code, response_code, response.content)

        if case == 'exists_account':
            self.assertIn(self.diskId, [disk['id'] for disk in response.json()])

    @parameterized.expand([
        ('exists_disk', 200), 
        ('non_exists_disk', 404),
        ('invalid_disk', 400)
    ])
    def test02_get_disk(self, case, response_code):
        """ OVC-001
        #. Create Account (A1), should succeed.
        #. Create disk (D1), should succeed.
        #. List account (A1) disks, (D1) should be listed. 
        """
        diskId = self.diskId

        if case == 'non_exists_disk':
            diskId = random.randint(100000, 200000)
        elif case == 'invalid_disk':
            diskId = self.utils.random_string()

        response = self.api.cloudapi.disks.get(diskId=diskId)
        self.assertEqual(response.status_code, response_code, response.content)

        if case == "exists_disk":
            self.assertEqual(response.json()['name'], self.disk_data['name'])
            self.assertEqual(response.json()['descr'], self.disk_data['description'])
            self.assertEqual(response.json()['type'], self.disk_data['type'])

    @parameterized.expand([
        ('exists_disk', 200),
        ('non_exists_disk', 404), 
        ('invalid_disk_size', 400)
    ])
    def test03_resize_disk(self, case, response_code):
        """ OVC-001
        #. Create Account (A1), should succeed.
        #. Create disk (D1), should succeed.
        #. List account (A1) disks, (D1) should be listed. 
        """
        diskId = self.diskId
        size = self.disk_data['size'] + random.randint(1, 20)
        
        if case == 'non_exists_disk':
            diskId = random.randint(100000, 200000)
        elif case == 'invalid_disk_size':
            size = self.disk_data['size'] - random.randint(1, 20)

        response = self.api.cloudapi.disks.resize(diskId=diskId, size=size)
        self.assertEqual(response.status_code, response_code, response.content)

        if case == "exists_disk":
            response = self.api.cloudapi.disks.get(diskId=diskId)
            self.assertEqual(response.status_code, response_code, response.content)
            self.assertEqual(response.json()['sizeMax'], size)

    @parameterized.expand([
        ('exists_disk', 200),
        ('non_exists_disk', 404), 
        ('invalid_disk', 400)
    ])
    def test04_delete_disk(self, case, response_code):
        """ OVC-001
        #. Create Account (A1), should succeed.
        #. Create disk (D1), should succeed.
        #. List account (A1) disks, (D1) should be listed. 
        """
        diskId = self.diskId

        if case == 'non_exists_disk':
            diskId = random.randint(100000, 200000)
        elif case == 'invalid_disk':
            diskId = self.utils.random_string()

        response = self.api.cloudapi.disks.delete(diskId=diskId)
        self.assertEqual(response.status_code, response_code, response.content)
        

    
