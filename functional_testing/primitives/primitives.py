import time, subprocess, argparse, re, uuid, requests, random
from termcolor import colored
from js9 import j


class PRIMITAVES:
    """
        Goal: Create CSs, ZOSs, ubuntu machines
        Input: OVC account client, # ZOS, #ubuntu machines
        Output: CSs' clients, ZOs' clients, VMs' clients
    """

    def __init__(self, ovc_data, zt_token, ssh_key):
        self.client_ovc = j.clients.openvcloud.get(data=ovc_data)
        self.zt_token = zt_token
        self.ssh_key = ssh_key
        self.zt_members = {}

    def install_zt_host(self):
        print(colored(' [*] Install zerotier client', 'white'))
        try:
            j.tools.prefab.local.network.zerotier.install()
        finally:
            j.tools.prefab.local.network.zerotier.start()

    def create_zerotier_nw(self):
        zt_config_instance_name = str(uuid.uuid4()).replace('-', '')[:10]
        self.zt_name = str(uuid.uuid4()).replace('-', '')[:10]
        self.zt_client = j.clients.zerotier.get(instance=zt_config_instance_name, data={'token_': self.zt_token})
        self.zt_network = self.zt_client.network_create(public=False, name=self.zt_name, auto_assign=True,
                                                        subnet='10.147.19.0/24')
        self.ipxe = 'ipxe: http://unsecure.bootstrap.gig.tech/ipxe/development/{}/console=ttyS1,115200%20development'.format(
            self.zt_network.id)

    def host_join_zt(self):
        print(colored(' [*] Host join zt network)', 'white'))
        j.tools.prefab.local.network.zerotier.network_join(network_id=self.zt_network.id)
        zt_machine_addr = j.tools.prefab.local.network.zerotier.get_zerotier_machine_address()
        time.sleep(60)
        host_member = self.zt_network.member_get(address=zt_machine_addr)
        host_member.authorize()
        self.zt_members[host_member.address] = host_member.private_ip

    def create_account(self):
        self.acount_name = str(uuid.uuid4()).replace('-', '')[:10]
        self.account_client = self.client_ovc.account_get(self.acount_name)
        print(colored(' [*] Account: %s' % self.acount_name, 'green'))

    def create_cloudspace(self):
        cs_name = str(uuid.uuid4()).replace('-', '')[:10]
        self.cs_client = self.account_client.space_get(cs_name)
        print(colored(' [*] CS: %s' % cs_name, 'green'))

    def create_zos_node(self):
        zos_name = str(uuid.uuid4()).replace('-', '')[:10]
        self.zos_vm = self.cs_client.machine_create(name=zos_name, memsize=8, disksize=10, datadisks=[10],
                                                    image='ipxe boot',
                                                    authorize_ssh=False, userdata=self.ipxe)
        time.sleep(180)
        self.zos_ip = self._authorize_zos()
        zos_cfg = {"host": self.zos_ip}
        self.zos_client = j.clients.zos.get(instance=zos_name, data=zos_cfg)
        self.zos_node = j.clients.zos.sal.get_node(instance=zos_name)
        print(colored(' [*] ZOS: %s' % zos_name, 'green'))

        # print(colored(' [*] Forward port 6379', 'white'))
        # self.zos_vm.portforward_create(6379, 6379)
        # time.sleep(120)

    def _authorize_zos(self):
        zt_memebrs = self.zt_network.members_list()
        for zt_member in zt_memebrs:
            if zt_member.address not in self.zt_members.keys():
                zt_member.authorize()
                self.zt_members[zt_member.address] = zt_member.private_ip
                return zt_member.private_ip

    def deploy_zdb_disk(self):
        print(colored(' [*] Deploy ZDB disk', 'white'))
        destination_dict = str(uuid.uuid4()).replace('-', '')[:10]
        self.zos_node.client.bash('mkdir -p /var/cache/%s' % destination_dict)
        zdb = self.zos_node.primitives.create_zerodb('myzdb', '/var/cache/%s' % destination_dict)
        self.disk = self.zos_node.primitives.create_disk('mydisk', zdb, filesystem='btrfs')
        self.disk.deploy()

    # create ovs container for vlan and vxlan network
    def create_ovs_container(self):
        ovs_container_name = str(uuid.uuid4()).replace('-', '')[:10]
        self.zos_node.network.configure(cidr='192.168.69.0/24', vlan_tag=2312, ovs_container_name=ovs_container_name)
        self.ovs_container = self.zos_node.containers.get(name=ovs_container_name)

    ##Block#1 (passthrough---GW---zt---VM)
    def create_gw_passthrough_zt(self):
        print(' [*] Create a GW with public and ZT networks')
        gw_name = str(uuid.uuid4()).replace('-', '')[:10]
        self.gw = self.zos_node.primitives.create_gateway(name=gw_name)

        print(' [*] Create "passthrough" public network ')
        self.zos_vm.externalnetwork_attach()
        time.sleep(60)
        external_network_ip_address = self.zos_vm.model['interfaces'][1]['ipAddress']
        external_gw_ip_address = self.zos_vm.model['interfaces'][1]['params'].split()[0].rsplit(':')[1]
        public_network_name = 'public'

        self.public_net = self.gw.networks.add(name=public_network_name, type_='passthrough', networkid='eth1')
        self.public_net.ip.cidr = external_network_ip_address
        self.public_net.ip.gateway = external_gw_ip_address

        print(colored('[*] private network is the zt network', 'white'))
        self.private_net = self.gw.networks.add_zerotier(self.zt_network)
        self.private_net.hosts.nameservers = ['8.8.8.8']

        self.gw.deploy()

    def create_ubuntu_vms_zt(self, source_port, destination_port):
        print(colored(' [*] Create an ubuntu machine.', 'white'))
        vm_name = str(uuid.uuid4()).replace('-', '')[:10]
        sshkey_instance = str(uuid.uuid4()).replace('-', '')[:10]
        self.ubuntu_vm = self.zos_node.primitives.create_virtual_machine(vm_name, 'ubuntu:latest')
        print(colored(' [*] Add disk.', 'white'))
        self.ubuntu_vm.disks.add(self.disk)
        print(colored(' [*] Add ssh key.', 'white'))
        self.ubuntu_vm.configs.add(sshkey_instance, '/root/.ssh/authorized_keys', self.ssh_key)
        print(colored(' [*] Join zt nw.', 'white'))
        self.ubuntu_vm.nics.add_zerotier(self.zt_network)
        self.ubuntu_vm.deploy()
        time.sleep(180)
        ubutnu_vm_name = self.ubuntu_vm.zt_identity.split(':')[0]
        self.ubuntu_vm.zt_ip = self.zt_network.member_get(ubutnu_vm_name).private_ip
        print(colored(' [*] ubuntu IP : %s ' % self.ubuntu_vm.zt_ip, 'green'))

        print(colored(' [*] SSH forward from public to the ubuntu vm'))
        self.gw.portforwards.add('sshforward', (self.public_net, source_port), (self.ubuntu_vm.zt_ip, destination_port))
        self.gw.deploy()
        return  self.ubuntu_vm.zt_ip

    ##Block#2 (passthrough---GW---vlan---VM)
    def create_gw_passthrough_vlan(self):
        print(' [*] Create a GW with public and vlan networks')
        gw_name = str(uuid.uuid4()).replace('-', '')[:10]
        self.gw = self.zos_node.primitives.create_gateway(name=gw_name)
        print(' [*] Create "passthrough" public network ')
        self.zos_vm.externalnetwork_attach()
        time.sleep(60)
        external_network_ip_address = self.zos_vm.model['interfaces'][1]['ipAddress']
        external_gw_ip_address = self.zos_vm.model['interfaces'][1]['params'].split()[0].rsplit(':')[1]
        public_network_name = 'public'

        self.public_net = self.gw.networks.add(name=public_network_name, type_='passthrough', networkid='eth1')
        self.public_net.ip.cidr = external_network_ip_address
        self.public_net.ip.gateway = external_gw_ip_address

        print(colored('[*] private network is the vlan  network', 'white'))
        vlan_tag = random.randint(1, 4094)
        self.private = self.gw.network.add('private', 'vlan', vlan_tag)
        self.private.private.ip.cidr = '192.168.103.1/24'
        self.gw.deploy()

    def create_ubuntu_vms_vlan(self, source_port, destination_port):
        print(colored(' [*] Create an ubuntu machine.', 'white'))
        vm_name = str(uuid.uuid4()).replace('-', '')[:10]
        sshkey_instance = str(uuid.uuid4()).replace('-', '')[:10]
        self.ubuntu_vm = self.zos_node.primitives.create_virtual_machine(vm_name, 'ubuntu:latest')
        print(colored(' [*] Add disk.', 'white'))
        self.ubuntu_vm.disks.add(self.disk)
        print(colored(' [*] Add ssh key.', 'white'))
        self.ubuntu_vm.configs.add(sshkey_instance, '/root/.ssh/authorized_keys', self.ssh_key)
        print(colored(' [*] add vm to vlan network.', 'white'))
        vlanhost = self.private.hosts.add(self.ubuntu_vm)
        self.ubuntu_vm.deploy()
     
        print(colored(' [*] ubuntu IP : %s ' % vlanhost.ipaddress, 'green'))
        print(colored(' [*] SSH forward from public to the ubuntu vm'))
        self.gw.portforwards.add('sshforward', (self.public_net, source_port), (vlanhost.ipaddress, destination_port))
        self.gw.deploy()

    ## Block#3 (passthrough---GW---vxlan---VM)
    def create_gw_passthrough_vxlan(self):
        print(' [*] Create a GW with public and vlan networks')
        gw_name = str(uuid.uuid4()).replace('-', '')[:10]
        self.gw = self.zos_node.primitives.create_gateway(name=gw_name)

        print(' [*] Create "passthrough" public network ')
        self.zos_vm.externalnetwork_attach()
        time.sleep(60)
        external_network_ip_address = self.zos_vm.model['interfaces'][1]['ipAddress']
        external_gw_ip_address = self.zos_vm.model['interfaces'][1]['params'].split()[0].rsplit(':')[1]
        public_network_name = 'public'

        self.public_net = self.gw.networks.add(name=public_network_name, type_='passthrough', networkid='eth1')
        self.public_net.ip.cidr = external_network_ip_address
        self.public_net.ip.gateway = external_gw_ip_address

        print(colored('[*] private network is the vlan  network', 'white'))
        vxlan_tag = random.randint(1, 100000)
        self.private = self. gw.network.add('private', 'vxlan', vxlan_tag)
        self.private.private.ip.cidr = '192.168.103.1/24'
        self.gw.deploy()

    def create_ubuntu_vms_vxlan(self, source_port, destination_port):
        print(colored(' [*] Create an ubuntu machine.', 'white'))
        vm_name = str(uuid.uuid4()).replace('-', '')[:10]
        sshkey_instance = str(uuid.uuid4()).replace('-', '')[:10]
        self.ubuntu_vm = self.zos_node.primitives.create_virtual_machine(vm_name, 'ubuntu:latest')
        print(colored(' [*] Add disk.', 'white'))
        self.ubuntu_vm.disks.add(self.disk)
        print(colored(' [*] Add ssh key.', 'white'))
        self.ubuntu_vm.configs.add(sshkey_instance, '/root/.ssh/authorized_keys', self.ssh_key)
        print(colored(' [*] add vm to vxlan network.', 'white'))
        vxlanhost = self.private.hosts.add(self.ubuntu_vm)
        self.ubuntu_vm.deploy()
     
        print(colored(' [*] ubuntu IP : %s ' % vxlanhost.ipaddress, 'green'))
        print(colored(' [*] SSH forward from public to the ubuntu vm'))
        self.gw.portforwards.add('sshforward', (self.public_net, source_port), (vxlanhost.ipaddress, destination_port))
        self.gw.deploy()

    ##Block#4 (default---GW---vxlan---VM)
    def create_gw_default_vxlan(self):
        print(' [*] Create a GW with default public networks')
        gw_name = str(uuid.uuid4()).replace('-', '')[:10]
        self.gw = self.zos_node.primitives.create_gateway(name=gw_name)

        print(' [*] Create "default" public network ')
        public_network_name = 'public'
        self.public_net = self.gw.networks.add(name=public_network_name, type_='default')
        self.public_net.public = True

        print(colored('[*] private network is the vxlan  network', 'white'))
        vxlan_tag = random.randint(1, 100000)
        self.private = self. gw.network.add('private', 'vxlan', vxlan_tag)
        self.private.private.ip.cidr = '192.168.103.1/24'
        self.gw.deploy()
    ##def create_ubuntue_vms_vxlan


    ##Block#5 (default---GW---vlan---VM)
    def create_gw_default_vlan(self):
        print(' [*] Create a GW with default public networks')
        gw_name = str(uuid.uuid4()).replace('-', '')[:10]
        self.gw = self.zos_node.primitives.create_gateway(name=gw_name)

        print(' [*] Create "default" public network ')
        public_network_name = 'public'
        self.public_net = self.gw.networks.add(name=public_network_name, type_='default')
        self.public_net.public = True

        print(colored('[*] private network is the vlan  network', 'white'))
        vlan_tag = random.randint(1, 4096)
        self.private = self. gw.network.add('private', 'vlan', vlan_tag)
        self.private.private.ip.cidr = '192.168.103.1/24'
        self.gw.deploy()

    ##def create_ubuntue_vms_vlan


    ##block#6 (default---GW--zt--VM)
    def create_gw_default_zt(self):
        print(' [*] Create a GW with default public and ZT networks')
        gw_name = str(uuid.uuid4()).replace('-', '')[:10]
        self.gw = self.zos_node.primitives.create_gateway(name=gw_name)

        print(' [*] Create "default" public network ')
        public_network_name = 'public'
        self.public_net = self.gw.networks.add(name=public_network_name, type_='default')
        self.public_net.public = True

        print(colored('[*] private network is the zt network', 'white'))
        self.private_net = self.gw.networks.add_zerotier(self.zt_network)
        self.private_net.hosts.nameservers = ['8.8.8.8']

        self.gw.deploy()

    ##def create_ubuntue_vms_zt