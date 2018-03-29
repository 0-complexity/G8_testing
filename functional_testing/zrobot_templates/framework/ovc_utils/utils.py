import time
from testconfig import config
from framework.constructor import constructor
from js9 import j
from framework.ovc_utils import *


class OVC_BaseTest(constructor):
    env = config['main']['environment']

    def __init__(self, *args, **kwargs):
        templatespath = './framework/ovc_utils/templates'
        super(OVC_BaseTest, self).__init__(templatespath, *args, **kwargs)
        self.ovc_data = {'address': OVC_BaseTest.env,
                         'port': 443,
                         }
        self.ovc_client = self.ovc_client()
        self.CLEANUP = {'users': [], 'accounts': []}

    def setUp(self):
        super(OVC_BaseTest, self).setUp()
        self.key = self.random_string()
        self.openvcloud = self.random_string()
        self.vdcusers = {'gig_qa_1': {'openvcloud': self.openvcloud,
                                      'provider': 'itsyouonline',
                                      'email': 'dina.magdy.mohammed+123@gmail.com'}}

    def tearDown(self):
        for acc in self.CLEANUP['accounts']:
            if self.check_if_service_exist(acc):
                self.temp_actions = {'account': {'actions': ['uninstall']}}
                account = {acc: {'openvcloud': self.openvcloud}}
                self.create_account(openvcloud=self.openvcloud, vdcusers=self.vdcusers,
                                    accounts=account, temp_actions=self.temp_actions)
                self.wait_for_service_action_status(acc, res[acc]['uninstall'], timeout=20)
        self.delete_services()

    def iyo_jwt(self):
        ito_client = j.clients.itsyouonline.get(instance="main")
        return ito_client.jwt

    @catch_exception_decoration_return
    def ovc_client(self):
        return j.clients.openvcloud.get(instance='main', data=self.ovc_data)
        
    def handle_blueprint(self, yaml, **kwargs):
        kwargs['token'] = self.iyo_jwt()
        blueprint = self.create_blueprint(yaml, **kwargs)
        return self.execute_blueprint(blueprint)

    def create_account(self, **kwargs):
        return self.handle_blueprint('account.yaml', **kwargs)

    def create_cs(self, **kwargs):
        return self.handle_blueprint('vdc.yaml', key=self.key, openvcloud=self.openvcloud,
                                     vdcusers=self.vdcusers, **kwargs)

    def create_user(self, **kwargs):
        return self.handle_blueprint('vdcuser.yaml', **kwargs)

    def create_vm(self, **kwargs):
        return self.handle_blueprint('node.yaml', key=self.key, openvcloud=self.openvcloud,
                                     vdcusers=self.vdcusers, **kwargs)

    def get_cloudspace(self, name):
        time.sleep(2)
        cloudspaces = self.ovc_client.api.cloudapi.cloudspaces.list()
        for cs in cloudspaces:
            if cs['name'] == name:
                return self.ovc_client.api.cloudapi.cloudspaces.get(cloudspaceId=cs['id'])
        return False

    def get_portforward_list(self, cloudspacename, machinename):
        time.sleep(2)
        cloudspaceId = self.get_cloudspace(cloudspacename)['id']
        machineId = self.get_vm(cloudspaceId, machinename)['id']
        return self.ovc_client.api.cloudapi.portforwarding.list(cloudspaceId=cloudspaceId, machineId=machineId)
    
    def get_account(self, name):
        time.sleep(2)
        accounts = self.ovc_client.api.cloudapi.accounts.list()
        for account in accounts:
            if account['name'] == name:
                return self.ovc_client.api.cloudapi.accounts.get(accountId=account['id'])
        return False

    def get_vm(self, cloudspaceId, vmname):
        time.sleep(3)
        vms = self.ovc_client.api.cloudapi.machines.list(cloudspaceId=cloudspaceId)
        for vm in vms:
            if vm['name'] == vmname:
                return self.ovc_client.api.cloudapi.machines.get(machineId=vm['id'])
        return False

    def wait_for_cloudspace_status(self, cs, status="DEPLOYED", timeout=100):
        for _ in range(timeout):
            cloudspace = self.get_cloudspace(cs)
            time.sleep(1)
            if cloudspace["status"] == status:
                return True
        return False
