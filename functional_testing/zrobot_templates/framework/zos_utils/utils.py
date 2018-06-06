from testconfig import config
from framework.constructor import constructor
from js9 import j
from framework.zos_utils import *
import time

class ZOS_BaseTest(constructor):
    zos_redisaddr = config['main']['redisaddr']

    def __init__(self, *args, **kwargs):
        templatespath = ['./framework/zos_utils/templates', './framework/base_templates']
        super(ZOS_BaseTest, self).__init__(templatespath, *args, **kwargs)

    @classmethod
    def setUpClass(cls):
        cls.zos_client = cls.zos_client(cls, cls.zos_redisaddr)
        cls.cont_flist = 'https://hub.gig.tech/gig-official-apps/ubuntu1604.flist'
        cls.vm_flist = 'https://hub.gig.tech/gig-bootable/ubuntu:16.04.flist'
        cls.cont_storage = 'ardb://hub.gig.tech:16379'
        cls.vm_username = config['main']['username']
        cls.vm_password = config['main']['password']

    @classmethod
    def tearDownClass(cls):
        cls.delete_services(cls())

    def setUp(self):
        super(ZOS_BaseTest, self).setUp()

    def zos_client(self, ip):
        data = {'host': ip, 'port': 6379,
                'timeout': 100, 'ssl': True}
        return j.clients.zero_os.get(instance='main', data=data)

    def handle_blueprint(self, yaml, **kwargs):
        blueprint = self.create_blueprint(yaml, **kwargs)
        return self.execute_blueprint(blueprint)

    def create_container(self, **kwargs):
        return self.handle_blueprint('container.yaml', **kwargs)

    def create_vm(self, **kwargs):
        return self.handle_blueprint('vm.yaml', **kwargs)

    def check_vnc(self, vnc_ip):
        vnc = 'vncdotool -s %s' % vnc_ip
        result,error = self.execute_shell_commands(cmd="%s type %s key enter" % (vnc, repr('ls')))       
        return error 
        
    def enable_ssh_access(self, vnc_ip, username=None, password=None):

        username = username or self.vm_username
        password = password or self.vm_password

        """
            Add ssh key to a vm with active vnc protocol.
        """
        vnc = 'vncdotool -s %s' % vnc_ip
        commands = [
            '%s' % username,
            '%s' % password,
            'sudo su',
            '%s' % password,
            'sed -i "s/^#PasswordAuthentication yes/PasswordAuthentication yes/g" /etc/ssh/sshd',
            'sed -i "s/PermitRootLogin yes/PermitRootLogin yes/g" /etc/ssh/sshd',            
            'service sshd restart'
        ]
        for cmd in commands:
            if "sed" in cmd:
                self.execute_shell_commands(cmd="%s type %s" % (vnc, repr(cmd)))
                self.execute_shell_commands(cmd="%s key shift-_ type config key enter" % vnc)
                time.sleep(1)
            elif 'https' in cmd:
                self.execute_shell_commands(cmd="%s type %s" % (vnc, repr(cmd)))
                self.execute_shell_commands(cmd="%s key shift-:" % vnc)
            else:
                self.execute_shell_commands(cmd="%s type %s key enter" % (vnc, repr(cmd)))
                time.sleep(1)

    def execute_command_inside_vm(self, client, vmip,  cmd, username=None, password=None):
        username = username or self.vm_username
        password = password or self.vm_password

        cmd = 'sshpass -p "{password}" ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=5 {username}@{vmip} "{cmd}"'.format(
            vmip=vmip,
            username=username,
            password=password,
            cmd=cmd
        )

        response = client.bash(cmd).get()
        return response
    
    def execute_shell_commands(self, cmd):
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, error = process.communicate()
        return out.decode('utf-8'), error.decode('utf-8')

    def vm_info(self, vm_name):
        vms = self.zos_client.kvm.list()
        vm = [vm for vm in vms if vm['name'] == vm_name]
        return vm