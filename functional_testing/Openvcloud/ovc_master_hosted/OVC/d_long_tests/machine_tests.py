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

    @unittest.skip('https://github.com/0-complexity/openvcloud/issues/1130')
    def test01_export_import_vm(self):
        """ OVC-047
        *Test case for checking cloned VM ip, portforwards and credentials*
        **Test Scenario:**
        #. Create virtual machine (VM1), should succeed.
        #. Create data disk (DD1), should succeed.
        #. Attach disk (DD1) to virtual machine (VM1), should succeed.
        #. Write file (F1) on the boot disk of the virtual machine (VM1), should succeed.
        #. Write file (F2) on the data disk of the virtual machine (VM1), should succeed.
        #. Export virtual machine (VM1), should succeed.
        #. Import virtual machine (VM1), should succeed.
        #. Check that file (F1) exists in the imported virtual machine.
        #. Check that file (F2) exists in the imported virtual machine's data disk (DD1).
        """
        self.lg('Create virtual machine (VM1), should succeed')
        machine_1_id = self.cloudapi_create_machine(self.cloudspace_id)

        self.lg('Create data disk (DD1), should succeed')
        disk_id = self.create_disk(self.account_id)

        self.lg('Attach disk (DD1) to virtual machine (VM1), should succeed')
        response = self.api.cloudapi.machines.attachDisk(machineId=machine_1_id, diskId=disk_id)
        self.assertTrue(response)

        self.lg('Write file (F1) on the boot disk of the virtual machine (VM1), should succeed')
        machine_1_client = VMClient(machine_1_id)
        machine_1_client.execute('echo "helloWorld" > test1.txt')

        self.lg('Write file (F2) on the data disk of the virtual machine (VM1), should succeed')
        machine_1_client.execute('mkdir data')
        machine_1_client.execute('mkfs.ext4 /dev/vdb', sudo=True)
        machine_1_client.execute('mount /dev/vdb data', sudo=True)
        machine_1_client.execute('chown ${USER}:${USER} data', sudo=True)
        machine_1_client.execute('echo "helloWorld" > data/test2.txt')
        
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

        try:
            self.lg('Export virtual machine (VM1), should succeed')
            response = self.api.cloudapi.machines.exportOVF(
                link=web_dav_link,
                machineId=machine_1_id,
                username=self.owncloud_user,
                passwd=self.owncloud_password,
                path=folder_name
            )

            self.assertTrue(response)

            time.sleep(500)

            self.lg('Import virtual machine (VM2), should succeed')
            self.api.cloudapi.machines.importOVF(
                link=web_dav_link,
                username=self.owncloud_user,
                passwd=self.owncloud_password,
                path=folder_name,
                cloudspaceId=self.cloudspace_id,
                name="imported_vm",
                sizeId=2
            )

            machines = self.api.cloudbroker.machine.list(cloudspaceId=self.cloudspace_id)
            imported_vm_id = [i['id'] for i in machines if i['id'] != machine_1_id]

            if not imported_vm_id:
                self.fail("can't import vm")

            self.lg('Check that file (F1) exists in the imported virtual machine')
            imported_vm_client = VMClient(
                imported_vm_id[0],
                login=machine_1_client.login,
                password=machine_1_client.password,
                timeout=120
            )

            stdin, stdout, stderr = imported_vm_client.execute('cat test1.txt')
            self.assertIn('helloWorld', stdout.read())

            self.lg('Check that file (F2) exists in the imported virtual machine\'s data disk (DD1)')
            stdin, stdout, stderr = imported_vm_client.execute('cat data/test2.txt')
            self.assertIn('helloWorld', stdout.read())

        except:
            raise
        
        finally:
            self.lg('Delete folder in owncloud')
            requests.request('DELETE', url=folder_url, auth=owncloud_auth)


    def test002_node_maintenance_migrateVMs(self):
        """ OVC-48
        *Test case for putting node in maintenance with action migrate all vms.*

        **Test Scenario:**

        #. Create 2 VMs, should succeed.
        #. Put node in maintenance with migrate all vms, should succeed.
        #. Check that the 2 VMs have been migrated.
        #. Check that the 2 VMs are in running state.
        #. Check that the 2 VMs are working well, should succeed.
        #. Enable the node back, should succeed.
        """
        stackId = self.get_running_stackId()
        gridId = self.get_node_gid(stackId)
        
        self.lg('Create 2 VMs, should succeed')
        machine_1_id = self.cloudbroker_create_machine(self.cloudspace_id, stackId=stackId)
        machine_2_id = self.cloudbroker_create_machine(self.cloudspace_id, stackId=stackId)

        self.lg('Put node in maintenance with migrate all vms, should succeed')
        response = self.api.cloudbroker.computenode.maintenance(id=stackId, gid=gridId, vmaction='move', message='test')
        self.assertTrue(response)

        try:
            self.lg('Check that the 2 VMs are in running state')
            machine_1_info = self.api.cloudapi.machines.get(machine_1_id)
            machine_2_info = self.api.cloudapi.machines.get(machine_2_id)
            self.assertTrue(machine_1_info['status'], 'RUNNING')
            self.assertTrue(machine_2_info['status'], 'RUNNING')

            self.lg('Check that the 2 VMs are working well, should succeed')
            machine_1_client = VMClient(machine_1_id)
            stdin, stdout, stderr = machine_1_client.execute('uname')
            self.assertIn('Linux', stdout.read())
            machine_2_client = VMClient(machine_2_id)
            stdin, stdout, stderr = machine_2_client.execute('uname')
            self.assertIn('Linux', stdout.read())

        except:
            raise
        finally:
           response = self.api.cloudbroker.computenode.enable(id=stackId, gid=gridId)
           self.assertTrue(response)