import unittest
import time
import os
import requests
import uuid
import zipfile
import random
from xlrd import open_workbook
from io import BytesIO
from ....utils.utils import BasicACLTest
from JumpScale.portal.portal.PortalClient2 import ApiError
from JumpScale.baselib.http_client.HttpClient import HTTPError


class ExtendedTests(BasicACLTest):
    def setUp(self):
        super(ExtendedTests, self).setUp()
        self.location = self.get_location()['locationCode']
        self.account_owner = self.username
        self.default_setup(create_default_cloudspace=False)

    def test001_basic_resource_limits(self):

        """ OVC-016
        *Test case for testing basic resource limits on account and cloudspace limits.*

        **Test Scenario:**

        #. create account with passing negative values in the account's limitation, should fail
        #. create account with certain limits, should succeed
        #. create cloudspace with passing negative values in the cloudspace's limitation, should fail
        #. create cloudspace that exceeds account's max_cores, should fail
        #. create cloudspace that exceeds account's max_memory, should fail
        #. create cloudspace that exceeds account's max_vdisks, should fail
        #. create cloudspace that exceeds account's max_IPs, should fail
        #. create cloudspace without exceeding account limits, should succeed
        #. Try to create another cloudspace without exceeding account limits, should fail as account\'s maxIPs=1
        #. create VM with exceeding cloudspace\'s cores number, should fail
        #. create VM with exceeding cloudspace\'s Memory, should fail
        #. create VM with exceeding cloudspace\'s disks capacity, should fail
        #. create VM with allowed limits
        #. add publicip to this VM, should fail as account's max_IPs=1
        """
        self.lg('- create account with passing negative values in the account\'s limitation')
        try:
            self.cloudbroker_account_create(self.account_owner, self.account_owner, self.email,
                                            maxMemoryCapacity=-5, maxVDiskCapacity=-3,
                                            maxCPUCapacity=-4, maxNumPublicIP= -2)
        except HTTPError as e:
            self.lg('- expected error raised %s' % e.message)
            self.assertEqual(e.status_code, 400)

        self.lg(' - create account with certain limits, should succeed')
        self.account_id = self.cloudbroker_account_create(self.account_owner, self.account_owner,
                                                          self.email, maxMemoryCapacity=2,
                                                          maxVDiskCapacity=60 , maxCPUCapacity=4,
                                                          maxNumPublicIP= 1)
        self.account_owner_api = self.get_authenticated_user_api(self.account_owner)

        self.lg('- create cloudspace with passing negative values in the cloudspace\'s limitation, should fail')
        try:
            self.cloudapi_cloudspace_create(account_id=self.account_id,
                                                       location=self.location,
                                                       name='cs1', access=self.account_owner,
                                                       api=self.account_owner_api, maxMemoryCapacity=-5,
                                                       maxDiskCapacity=-4, maxCPUCapacity=-3,
                                                       maxNumPublicIP=-2)
        except ApiError as e:
            self.lg('- expected error raised %s' % e.message)
            self.assertEqual(e.message, '400 Bad Request')


        list =[{'mC':8, 'mM':0, 'mVD':0, 'mIP':0, 's':'max_cores'},
               {'mC':0, 'mM':8, 'mVD':0, 'mIP':0, 's':'max_memory'},
               {'mC':0, 'mM':0, 'mVD':100, 'mIP':0, 's':'max_vdisks'},
               {'mC':0, 'mM':0, 'mVD':0, 'mIP':2, 's':'max_IPs'}]
        for i in list:
            self.lg('- create cloudspace that exceeds account\'s %s, should fail'%i['s'])
            try:
                self.cloudapi_cloudspace_create(account_id=self.account_id, location=self.location,
                                                name='cs1', access=self.account_owner,
                                                api=self.account_owner_api,
                                                maxMemoryCapacity=i['mM'] or 2,
                                                maxDiskCapacity=i['mVD'] or 60,
                                                maxCPUCapacity= i['mC'] or 4,
                                                maxNumPublicIP=i['mIP'] or 1)
            except ApiError as e:
                self.lg('- expected error raised %s' % e.message)
                self.assertEqual(e.message, '400 Bad Request')


        self.lg('- create cloudspace without exceeding account limits, should succeed')
        cloudspaceId = self.cloudapi_cloudspace_create(account_id=self.account_id,
                                                       location=self.location,
                                                       name='cs1', access=self.account_owner,
                                                       api=self.account_owner_api, maxMemoryCapacity=2,
                                                       maxDiskCapacity=60, maxCPUCapacity=4,
                                                       maxNumPublicIP=1)

        self.lg('Try to create another cloudspace without exceeding account limits,'
                ' should fail as account\'s maxIPs=1')
        try:
            self.cloudapi_cloudspace_create(account_id=self.account_id,
                                                       location=self.location,
                                                       name='cs2', access=self.account_owner,
                                                       api=self.account_owner_api, maxMemoryCapacity=2,
                                                       maxDiskCapacity=60, maxCPUCapacity=4,
                                                       maxNumPublicIP=1)
        except ApiError as e:
            self.lg('- expected error raised %s' % e.message)
            self.assertEqual(e.message, '400 Bad Request')


        self.lg('- create VM with exceeding cloudspace\'s cores number (Mem=16, C=8), '
                'should fail as (c=8)>4')
        try:
            self.cloudapi_create_machine(cloudspaceId, self.account_owner_api, size_id=5)
        except ApiError as e:
            self.lg('- expected error raised %s' % e.message)
            self.assertEqual(e.message, '400 Bad Request')

        self.lg('- create VM with (Mem=8, C=4), should fail as (M=8)>2')
        try:
            self.cloudapi_create_machine(cloudspaceId, self.account_owner_api, size_id=4)
        except ApiError as e:
            self.lg('- expected error raised %s' % e.message)
            self.assertEqual(e.message, '400 Bad Request')

        self.lg('- create VM with (BD=100), should fail as (BD=100)>60')
        try:
            self.cloudapi_create_machine(cloudspaceId, self.account_owner_api, disksize=10)
        except ApiError as e:
            self.lg('- expected error raised %s' % e.message)
            self.assertEqual(e.message, '400 Bad Request')


        self.lg('- create VM with allowed limits, should succeed')
        machineId = self.cloudapi_create_machine(cloudspaceId, self.account_owner_api)

        self.lg('- Add publicip to this VM, should fail as max_IPs=1')
        try:
            self.account_owner_api.cloudapi.machines.attachExternalNetwork(machineId=machineId)
        except ApiError as e:
            self.lg('- expected error raised %s' % e.message)
            self.assertEqual(e.message, '400 Bad Request')


    def test002_resource_limits_on_account_level(self):
        """ OVC-017
        *Test case for testing basic resource limits on account and cloudspace limits.*

        **Test Scenario:**

        #. create account with certain limits, should succeed
        #. create 1st cloudspace that doesn't exceed account limits
        #. create 2nd cloudspace that doesn't exceed account limits
        #. create VM on the 1st cloudspace without exceeding account limits , should succeed
        #. create VM on the 2nd cloudspace, should fail (as total VMs Memory and cores exceeds that of the account)
        #. create VM on the 2nd cloudspace, should fail (as total VMs disks capacity exceeds that of the account)
        #. create 2nd VM  on the 2nd cloudspace without exceeding account total limits, should succeed
        #. Add publicip to the 2nd VM, should fail as acoount total IPs=2

        """
        self.lg('- create account with certain limits, should succeed')
        self.account_id = self.cloudbroker_account_create(self.account_owner, self.account_owner, self.email,
                                                          maxMemoryCapacity=12,
                                                          maxVDiskCapacity=250 , maxCPUCapacity=6,
                                                          maxNumPublicIP= 2)
        self.account_owner_api = self.get_authenticated_user_api(self.account_owner)

        self.lg('- create 1st cloudspace that doesn\'t exceed account limits')
        cloudspaceId_1 = self.cloudapi_cloudspace_create(account_id=self.account_id,
                                                       location=self.location,
                                                       name='cs1', access=self.account_owner,
                                                       api=self.account_owner_api, maxMemoryCapacity=8,
                                                       maxDiskCapacity=130, maxCPUCapacity=4,
                                                       maxNumPublicIP=1)

        self.lg('- create 2st cloudspace that doesn\'t exceed account limits')
        cloudspaceId_2 = self.cloudapi_cloudspace_create(account_id=self.account_id,
                                                       location=self.location,
                                                       name='cs2', access=self.account_owner,
                                                       api=self.account_owner_api, maxMemoryCapacity=4,
                                                       maxDiskCapacity=120, maxCPUCapacity=2,
                                                       maxNumPublicIP=1)

        self.lg('- create VM (M=8, C=4, BD=100, DD=[10,10,10]) on the 1st cloudspace, should succeed')
        self.cloudapi_create_machine(cloudspaceId_1, self.account_owner_api, size_id=4,
                                     disksize=100, datadisks=[10,10,10])

        self.lg('- create VM (M=8, C=4) on the 2nd cloudspace, should fail as T_M=16 & T_C=8')
        try:
            self.cloudapi_create_machine(cloudspaceId_2, self.account_owner_api, size_id=4)
        except ApiError as e:
            self.lg('- expected error raised %s' % e.message)
            self.assertEqual(e.message, '400 Bad Request')

        self.lg('- create VM (M=2, C=2, BD=100, DD=[10,10,10]) on the 2nd cloudspace,'
                ' should fail as T_VD=260')
        try:
            self.cloudapi_create_machine(cloudspaceId_2, self.account_owner_api, size_id=2,
                                         disksize=100, datadisks=[10,10,10])
        except ApiError as e:
            self.lg('- expected error raised %s' % e.message)
            self.assertEqual(e.message, '400 Bad Request')

        self.lg('- create 2nd VM (M=4, C=2, BD=100, DD=[10,10]) on the 2nd cloudspace, should succeed')
        machineId_2 = self.cloudapi_create_machine(cloudspaceId_2, self.account_owner_api, size_id=3,
                                                 disksize=100, datadisks=[10,10])

        self.lg('- Add publicip to the 2nd VM, should fail as T_IPs=2')
        try:
            self.account_owner_api.cloudapi.machines.attachExternalNetwork(machineId=machineId_2)
        except ApiError as e:
            self.lg('- expected error raised %s' % e.message)
            self.assertEqual(e.message, '400 Bad Request')



    def test003_resource_limits_on_cloudspace_level(self):
        """ OVC-018
        *Test case for testing basic resource limits on account and cloudspace limits.*

        **Test Scenario:**

        #. create account with certain limits, should succeed
        #. create cloudspace that doesn't exceed account limits
        #. create 1st VM on the created cloudspace without exceeding its limits, should succeed
        #. create another VM on the created cloudspace, should fail (as total VMs Memory and cores exceeds that of the cloudspace)
        #. create another VM on the created cloudspace, should fail (as total VMs disks capacity exceeds that of the cloudspace)
        #. create 2nd VM on the created cloudspace, should succeed
        #. Add publicip to the 2nd VM, should fail as total cloudspace IPs=1

        """
        self.lg('- create account with certain limits, should succeed')
        self.account_id = self.cloudbroker_account_create(self.account_owner, self.account_owner, self.email,
                                                          maxMemoryCapacity=200,
                                                          maxVDiskCapacity=500 , maxCPUCapacity=100,
                                                          maxNumPublicIP= 10)
        self.account_owner_api = self.get_authenticated_user_api(self.account_owner)

        self.lg('- create cloudspace that doesn\'t exceed account limits')
        cloudspaceId= self.cloudapi_cloudspace_create(account_id=self.account_id,
                                                       location=self.location,
                                                       name='cs1', access=self.account_owner,
                                                       api=self.account_owner_api, maxMemoryCapacity=20,
                                                       maxDiskCapacity=250, maxCPUCapacity=10,
                                                       maxNumPublicIP=1)

        self.lg('- create 1st VM (M=16, C=8, BD=100, DD=[10,10,10]) on the created cloudspace, should succeed')
        self.cloudapi_create_machine(cloudspaceId, self.account_owner_api, size_id=5,
                                     disksize=100, datadisks=[10,10,10])

        self.lg('- create another VM (M=8, C=4) on the created cloudspace, should fail as T_M=24 & T_C=12')
        try:
            self.cloudapi_create_machine(cloudspaceId, self.account_owner_api, size_id=4)
        except ApiError as e:
            self.lg('- expected error raised %s' % e.message)
            self.assertEqual(e.message, '400 Bad Request')

        self.lg('- create VM (M=2, C=2, BD=100, DD=[10,10,10]) on the created cloudspace,'
                ' should fail as T_VD=260')
        try:
            self.cloudapi_create_machine(cloudspaceId, self.account_owner_api, size_id=2,
                                         disksize=100, datadisks=[10,10,10])
        except ApiError as e:
            self.lg('- expected error raised %s' % e.message)
            self.assertEqual(e.message, '400 Bad Request')

        self.lg('- create 2nd VM (M=2, C=2, BD=100, DD=[10,10]) on the created cloudspace, should succeed')
        machineId = self.cloudapi_create_machine(cloudspaceId, self.account_owner_api, size_id=2,
                                                 disksize=100, datadisks=[10,10])

        self.lg('- Add publicip to the 2nd VM, should fail as T_IPs=1')
        try:
            self.account_owner_api.cloudapi.machines.attachExternalNetwork(machineId=machineId)
        except ApiError as e:
            self.lg('- expected error raised %s' % e.message)
            self.assertEqual(e.message, '400 Bad Request')

    def test004_getting_account_resources(self):
        """ OVC-045
        *Test case for checking account's resources retrieval*

        **Test Scenario:**

        #. Create account.
        #. Create cloudspaces CS1 and CS2.
        #. Create VM1 on CS1 and VM2 & VM3 on CS2 with certain specs.
        #. Get the account information binary file.
        #. Convert binary file to .xls file to be able extract account's information.
        #. Check if the account's information in the .xls file matches the vms and cloudspaces information.
        """
        self.lg('%s STARTED' % self._testID)

        self.lg('Create account')
        self.account_id = self.cloudbroker_account_create(self.account_owner, self.account_owner, self.email)

        self.lg('Create cloudspaces CS1 and CS2')
        cs1_id = self.cloudapi_cloudspace_create(self.account_id,
                                                 self.location,
                                                 self.account_owner)
        cs2_id = self.cloudapi_cloudspace_create(self.account_id,
                                                 self.location,
                                                 self.account_owner)
        css_ids = [cs1_id, cs2_id]

        self.lg('Create VM1 on CS1 and VM2 & VM3 on CS2 with certain specs')
        bdisk_size = 10
        used_size = 2
        vm1_id = self.cloudapi_create_machine(cs1_id, size_id=used_size, disksize=bdisk_size)
        vm2_id = self.cloudapi_create_machine(cs2_id, size_id=used_size, disksize=bdisk_size)
        vm3_id = self.cloudapi_create_machine(cs2_id, size_id=used_size, disksize=bdisk_size)
        vms_cs1_count = 1
        vms_cs2_count = 2
        vms_cs_count = [vms_cs1_count, vms_cs2_count]

        self.lg('Determine cpu, mem and boot disk sizes for cs1 and cs2')
        sizes = self.api.cloudapi.sizes.list(cloudspaceId=cs1_id)
        size = [s for s in sizes if s['id'] == used_size][0]
        total_mem_cs = [vms_cs1_count * size['memory'], vms_cs2_count * size['memory']]
        total_cpu_cs = [vms_cs1_count * size['vcpus'], vms_cs2_count * size['vcpus']]
        total_diskz_cs = [vms_cs1_count * bdisk_size, vms_cs2_count * bdisk_size]

        self.lg("Trigger jumscript on the controller to collect account's information.")
        now = time.time()
        delta = 60 * 60 * 3
        end = now + delta
        start = now - delta
        password = str(uuid.uuid4())[0:8]
        username = self.cloudbroker_user_create(group='admin', password=password)
        user_api = self.get_authenticated_user_api(username=username, password=password)
        stackId = self.api.cloudbroker.machine.get(machineId=vm1_id)["stackId"]
        gid = self.get_node_gid(stackId)
        res = user_api.system.agentcontroller.executeJumpscript(organization='jumpscale', name='resmonitoring',
                                                                gid=gid, role='controller')
        self.assertEqual(res['state'], 'OK')
        time.sleep(5)

        self.lg("Trigger jumscript on the master to collect account's information")
        res = user_api.system.agentcontroller.executeJumpscript(organization='greenitglobe', name='aggregate_account_data',
                                                                gid=gid, role='master')
        self.assertEqual(res['state'], 'OK')

        self.lg('Download the account information binary file')
        credential = {'name': username, 'secret': password}
        url = 'https://' + "{}.demo.greenitglobe.com".format(self.environment)
        login_url = url + '/restmachine/system/usermanager/authenticate'
        session = requests.Session()
        session.post(url=login_url, data=credential)
        api_url = url + '/restmachine/cloudapi/accounts/getConsumption?accountId={}&start={}&end={}'.format(self.account_id, start, end)
        response = session.get(url=api_url)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.text, '')

        self.lg('Writing capnp schema into a file')
        first_part = '        @0x934efea7f327fff0;'
        second_part = """
        struct CloudSpace {
          cloudSpaceId @0 :Int32;
          accountId @1 :Int32;
          machines @2 :List(VMachine);
          state @3 :Text;
          struct VMachine {
            id @0 :Int32;
            type @1 :Text;
            vcpus @2 :Int8;
            cpuMinutes @3 :Float32;
            mem @4 :Float32;
            networks @5 :List(Nic);
            disks @6 :List(Disk);
            imageName @7 :Text;
            status @8 :Text;
            struct Nic {
              id @0 :Int32;
              type @1 :Text;
              tx @2 :Float32;
              rx @3 :Float32;
            }
            struct Disk {
                id @0 :Int32;
                size @1 :Float32;
                iopsRead  @2 :Float32;
                iopsWrite  @3 :Float32;
                iopsReadMax @4 :Float32;
                iopsWriteMax @5 :Float32;
            }
          }
        }
        struct Account {
          accountId @0  :UInt32;
          cloudspaces @1 :List(CloudSpace);
        }
        """

        res_mon_schema = first_part + second_part
        os.mkdir('{}/resource_mang'.format(os.getcwd()))
        try:
            cwd = os.getcwd() + '/resource_mang'
            os.mkdir('{}/resourcetracking'.format(cwd))
            os.system("touch {}/resourcemonitoring.capnp".format(cwd))
            with open('{}/resourcemonitoring.capnp'.format(cwd), 'w') as f:
                f.write('{}'.format(res_mon_schema))

            self.lg("Convert binary file to .xls file to be able extract account's information.")
            bin_to_xls_script = """
            from JumpScale import j
            import argparse
            import os
            import xlwt
            import pprint
            import capnp
            from datetime import datetime
            from os import listdir
            capnp.remove_import_hook()
            schemapath = os.path.join('{0}', 'resourcemonitoring.capnp')
            resources_capnp = capnp.load(schemapath)
            root_path = '{0}/resourcetracking'
            accounts = listdir(root_path)
            book = xlwt.Workbook(encoding='utf-8')
            nosheets = True
            for dirpath, subdirs, files in os.walk(root_path):
                for x in files:
                    file_path = os.path.join(dirpath, x)
            for account in accounts:
                nosheets = False
                sheet = book.add_sheet('account %s' % account)
                sheet.write(0, 0, 'Cloud Space ID')
                sheet.write(0, 1, 'Machine Count')
                sheet.write(0, 2, 'Total Memory')
                sheet.write(0, 3, 'Total VCPUs')
                sheet.write(0, 4, 'Disk Size')
                sheet.write(0, 5, 'Disk IOPS Read')
                sheet.write(0, 6, 'Disk IOPS Write')
                sheet.write(0, 7, 'NICs TX')
                sheet.write(0, 8, 'NICs RX')
                with open(file_path, 'rb') as f:
                    account_obj = resources_capnp.Account.read(f)
                    for idx, cs in enumerate(account_obj.cloudspaces):
                        cs_id = cs.cloudSpaceId
                        machines = len(cs.machines)
                        vcpus = 0
                        mem = 0
                        disksize = 0
                        disk_iops_read = 0
                        disk_iops_write = 0
                        nics_tx = 0
                        nics_rx = 0
                        for machine in cs.machines:
                            vcpus += machine.vcpus
                            mem += machine.mem
                            for disk in machine.disks:
                                disk_iops_read += disk.iopsRead
                                disk_iops_write += disk.iopsWrite
                                disksize += disk.size
                            for nic in machine.networks:
                                nics_tx += nic.tx
                                nics_rx += nic.rx
                        sheet.write(idx + 1, 0, cs_id)
                        sheet.write(idx + 1, 1, machines)
                        sheet.write(idx + 1, 2, mem)
                        sheet.write(idx + 1, 3, vcpus)
                        sheet.write(idx + 1, 4, disksize)
                        sheet.write(idx + 1, 5, disk_iops_read)
                        sheet.write(idx + 1, 6, disk_iops_write)
                        sheet.write(idx + 1, 7, nics_tx)
                        sheet.write(idx + 1, 8, nics_rx)
            if nosheets is False:
                book.save('example.xls')
            else:
                print('No data found')
            """.format(cwd)

            os.system("touch {}/export_acc.py".format(cwd))
            with open('{}/export_acc.py'.format(cwd), 'w') as f:
                f.write('{}'.format(bin_to_xls_script))
            os.system("sed -i 's/            //' {}/export_acc.py".format(cwd))
            os.system("sed -i 's/            //' {}/resourcemonitoring.capnp".format(cwd))

            self.lg('Extracting .xls zip file')
            file = zipfile.ZipFile(BytesIO(response.content))
            file.extractall('{}/resourcetracking'.format(cwd))
            os.system('cd {}; python export_acc.py'.format(cwd))

            self.lg('Extracting info from xls file')
            wb = open_workbook("{}/example.xls".format(cwd))
            wb.sheet_by_index(0)
            s = wb.sheet_by_index(0)
            cs1_id = int(s.cell(1, 0).value)
            cs1_vms_nums = int(s.cell(1, 1).value)
            cs1_total_mem = int(s.cell(1, 2).value)
            cs1_total_vcpu = int(s.cell(1, 3).value)
            cs1_Disk_size = int(s.cell(1, 4).value)

            cs2_id = int(s.cell(2, 0).value)
            cs2_vms_nums = int(s.cell(2, 1).value)
            cs2_total_mem = int(s.cell(2, 2).value)
            cs2_total_vcpu = int(s.cell(2, 3).value)
            cs2_Disk_size = int(s.cell(2, 4).value)

            if cs1_id == css_ids[0]:
                c1 = 0; c2 = 1
            else:
                c1 = 1; c2 = 0

            self.assertEqual(cs1_id, css_ids[c1])
            self.assertEqual(cs2_id, css_ids[c2])
            self.assertEqual(cs1_vms_nums, vms_cs_count[c1] + 1)
            self.assertEqual(cs2_vms_nums, vms_cs_count[c2] + 1)
            self.assertEqual(cs1_total_mem, total_mem_cs[c1])
            self.assertEqual(cs2_total_mem, total_mem_cs[c2])
            self.assertEqual(cs1_total_vcpu, total_cpu_cs[c1])
            self.assertEqual(cs2_total_vcpu, total_cpu_cs[c2])
            self.assertEqual(cs1_Disk_size, total_diskz_cs[c1])
            self.assertEqual(cs2_Disk_size, total_diskz_cs[c2])
        except:
            raise
        finally:
            os.system("rm -rf {}/resource_mang".format(os.getcwd()))

        self.lg('%s ENDED' % self._testID)

    def test005_update_account_users(self):
        """ OVC-052
        *Test case for testing basic resource limits on account and cloudspace limits.*

        **Test Scenario:**

        #. Create user (U1), should succeed.
        #. Create user (U2), should succeed.
        #. Add user (U1) to account (AC1) with read access, should succeed.
        #. Add user (U2) to account (AC1) with admin access, should succeed.
        #. Try to create cloudspace using user (U1), should fail.
        #. Update user (U1) access to write, should succeed.
        #. Try to create cloudspace using user (U1), should succeed.
        #. Try to delete user (U2) from account (AC1) using user (U1), should fail.
        #. Update user (U1) access to admin, should succeed.
        #. Try to delete user (U2) from account (AC1) using user (U1), should succeed.
        #. Update account (AC1) user using non-existing account id, should fail.
        #. Update account (AC1) user using non-existing user id, should fail.
        #. Update user (U1) access to invalid access type, should fail.
        """
        self.lg('Create user (U1), should succeed')
        user_1_id = self.cloudbroker_user_create()
        user_1_api = self.get_authenticated_user_api(user_1_id)
        self.assertTrue(user_1_api)

        self.lg('Create user (U2), should succeed')
        user_2_id = self.cloudbroker_user_create()
        user_2_api = self.get_authenticated_user_api(user_2_id)
        self.assertTrue(user_2_api)

        self.lg('Add user (U1) to account (AC1) with read access, should succeed')
        self.api.cloudapi.accounts.addUser(accountId=self.account_id, userId=user_1_id, accesstype='R')

        self.lg('Add user (U2) to account (AC1) with read access, should succeed')
        self.api.cloudapi.accounts.addUser(accountId=self.account_id, userId=user_2_id, accesstype='ARCXDU')

        self.lg('Try to create cloudspace using user (U1), should fail')
        with self.assertRaises(ApiError) as e:
            self.cloudapi_cloudspace_create(self.account_id, self.location, user_1_id, user_1_api)

        self.lg('Update user (U1) access to write, should succeed')
        self.api.cloudapi.accounts.updateUser(accountId=self.account_id, userId=user_1_id, accesstype='RCX')

        self.lg('Try to create cloudspace using user (U1), should succeed')
        response = self.cloudapi_cloudspace_create(self.account_id, self.location, user_1_id, user_1_api)
        self.assertTrue(response)

        self.lg('Try to delete user (U2) from account (AC1) using user (U1), should fail')
        with self.assertRaises(ApiError) as e:
            user_1_api.cloudapi.accounts.deleteUser(accountId=self.account_id, userId=user_2_id, recursivedelete=True)
        
        self.lg('Update user (U1) access to admin, should succeed')
        self.api.cloudapi.accounts.updateUser(accountId=self.account_id, userId=user_1_id, accesstype='ARCXDU')

        self.lg('Try to delete user (U2) from account (AC1) using user (U1), should succeed')
        response = user_1_api.cloudapi.accounts.deleteUser(accountId=self.account_id, userId=user_2_id, recursivedelete=True)
        self.assertTrue(response)

        self.lg('Update account (AC1) user using non-existing account id, should fail')
        invalid_account_id = random.randint(10000, 20000)
        with self.assertRaises(HTTPError) as e:
            self.api.cloudapi.accounts.updateUser(accountId=invalid_account_id, userId=user_1_id, accesstype='R')
        self.assertEqual(e.exception.status_code, 404)
        
        self.lg('Update account (AC1) user using non-existing user id, should fail')
        invalid_user_id = random.randint(10000, 20000)
        with self.assertRaises(HTTPError) as e:
            self.api.cloudapi.accounts.updateUser(accountId=self.account_id, userId=invalid_user_id, accesstype='R')
        self.assertEqual(e.exception.status_code, 404)

        self.lg('Update user (U1) access to invalid access type, should fail')
        with self.assertRaises(HTTPError) as e:
            self.api.cloudapi.accounts.updateUser(accountId=self.account_id, userId=user_1_id, accesstype='FAKE')
        self.assertEqual(e.exception.status_code, 400)
