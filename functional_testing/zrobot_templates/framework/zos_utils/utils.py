import time
from testconfig import config
from framework.constructor import constructor
from js9 import j
from framework.zos_utils import *

class ZOS_BaseTest(constructor):
    zos_redisaddr = config['main']['redisaddr']

    def __init__(self, *args, **kwargs):
        templatespath = ['./framework/zos_utils/templates', './framework/base_templates']
        super(ZOS_BaseTest, self).__init__(templatespath, *args, **kwargs)

    @classmethod
    def setUpClass(cls):
        cls.zos_client = cls.zos_client(cls, cls.zos_redisaddr)
        cls.zos_node_name = cls.random_string()
        cls.zos_nodes = {cls.zos_node_name: {'redisAddr': cls.zos_redisaddr,
                                             'redisPort': 6379, 'hostname': "myzeros"}}
        cls.cont_flist = 'https://hub.gig.tech/gig-official-apps/ubuntu1604.flist'
        cls.cont_storage = 'ardb://hub.gig.tech:16379'

    @classmethod
    def tearDownClass(cls):
        cls.delete_services(cls())

    def setUp(self):
        super(ZOS_BaseTest, self).setUp()

    def zos_client(self, ip):
        data = {'host': ip, 'port':6379,
                'timeout': 100, 'ssl': True}
        return j.clients.zero_os.get(instance='main', data=data)

    def handle_blueprint(self, yaml, **kwargs):
        blueprint = self.create_blueprint(yaml, **kwargs)
        return self.execute_blueprint(blueprint)

    def create_zos_node(self, **kwargs):
        return self.handle_blueprint('node.yaml', zos_nodes=self.zos_nodes, **kwargs)

    def create_container(self, **kwargs):
        return self.handle_blueprint('container.yaml', zos_nodes=self.zos_nodes, **kwargs)

    def create_vm(self, **kwargs):
        return self.handle_blueprint('vm.yaml', zos_nodes=self.zos_nodes, **kwargs)