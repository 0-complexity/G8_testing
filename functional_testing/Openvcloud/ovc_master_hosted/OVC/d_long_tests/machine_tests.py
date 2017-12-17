import unittest, random, uuid
from ....utils.utils import BasicACLTest, VMClient
from nose_parameterized import parameterized
from JumpScale.portal.portal.PortalClient2 import ApiError
from JumpScale.baselib.http_client.HttpClient import HTTPError
import time
import threading
import os, requests

class MachineLongTests(BasicACLTest):
    def setUp(self):
        super(MachineLongTests, self).setUp()
        self.default_setup()

    @unittest.skip('https://github.com/0-complexity/openvcloud/issues/1088')
    def test01_export_import_vm(self):
        """ OVC-047
        *Test case for checking cloned VM ip, portforwards and credentials*
        **Test Scenario:**
        #. Create virtual machine (VM1), should succeed.
        #. Write file (F1) on virtual machine (VM1), should succeed.
        #. Export virtual machine (VM1), should succeed.
        #. Import virtual machine (VM1), should succeed.
        #. Check that file (F1) exists in the imported virtual machine.
        """
        self.lg('Create virtual machine (VM1), should succeed')
        machine_1_id = self.cloudapi_create_machine(self.cloudspace_id)

        self.lg('Write file (F1) on virtual machine (VM1), should succeed')
        machine_1_client = VMClient(machine_1_id)
        machine_1_client.execute('echo "helloWorld" > test.txt')

        folder_name = str(uuid.uuid4()).replace('-', '')[:10]        
        owncloud_auth = (self.owncloud_user, self.owncloud_password)

        web_dav_link = self.owncloud_url + '/remote.php/webdav/'

        folder_url = '{url}/remote.php/dav/files/{user}/{folder}'.format(
            url=self.owncloud_url, 
            user=self.owncloud_user, 
            folder=folder_name
        )

        self.lg('Create folder in owncloud')
        requests.request('MKCOL', url=folder_url, auth=owncloud_auth)

        self.lg('Export virtual machine (VM1), should succeed')
        response = self.api.cloudapi.machines.exportOVF(
            link=web_dav_link,
            machineId=machine_1_id,
            username=self.owncloud_user,
            passwd=self.owncloud_password,
            path=folder_name
        )

        self.assertTrue(response)

        time.sleep(400)

        self.lg('Import virtual machine (VM2), should succeed')
        imported_vm_id = self.api.cloudapi.machines.importOVF(link=web_dav_link,
                                                              username=self.owncloud_user,
                                                              passwd=self.owncloud_password,
                                                              path=folder_name,
                                                              cloudspaceId=self.cloudspace_id,
                                                              name="imported_vm",
                                                              sizeId=2)

        self.lg('Check that file (F1) exists in the imported virtual machine')
        imported_vm_client = VMClient(imported_vm_id)
        stdin, stdout, stderr = imported_vm_client.execute('cat test.txt')
        self.assertIn('helloWorld', stdout.read())

        self.lg('Delete folder in owncloud')
        requests.request('DELETE', url=folder_url, auth=owncloud_auth)