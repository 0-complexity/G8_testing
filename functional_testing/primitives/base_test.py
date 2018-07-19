from unittest import TestCase
from primitives import PRIMITAVES
from testconfig import config
import requests
import logging,time
import subprocess


class TestcasesBase(TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = config['iyo']['application_id_']
        self.client_secret = config['iyo']['secert']
        self.jwt = self.get_jwt()
        self.ovc_data = {"address": config['ovc']['address'],
                         "location": config['ovc']['loaction'],
                         "port": config['ovc']['port'],
                         "jwt_": self.jwt
                        }
        self.ssh_key = config['main']['ssh_key']
        self.zt_token = config['zerotier']['zt_token']

        self.primitive = PRIMITAVES(ovc_data=self.ovc_data, zt_token=self.zt_token, ssh_key=self.ssh_key)
        self.create_zos_node()

    def setUp(self):
        self._testID = self._testMethodName
        self._startTime = time.time()
        self._logger = logging.LoggerAdapter(logging.getLogger('primitive_testsuite'),
                                             {'testid': self.shortDescription() or self._testID})

    def setUp(self):
        pass

    def get_jwt(self):
        jwt = requests.post('https://itsyou.online/v1/oauth/access_token?grant_type=client_credentials&client_id=%s&client_secret=%s&response_type=id_token' % (
                             self.client_id, self.client_secret))
        return jwt.text

    def create_zos_node(self):
        self.primitive.install_zt_host()
        self.primitive.create_zerotier_nw()
        self.primitive.host_join_zt()
        self.primitive.create_account()
        self.primitive.create_cloudspace()
        self.primitive.create_zos_node()

    def execute_command(self, ip, cmd):
        target = "ssh -o 'StrictHostKeyChecking no' root@%s '%s'" % (ip, cmd)
        ssh = subprocess.Popen(target,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        result = ssh.stdout.readlines()
        error = ssh.stderr.readlines()
        return result, error

    def log(self, msg):
        self._logger.info(msg)