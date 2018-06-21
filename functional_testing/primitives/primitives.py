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

    def create_zerotier_nw(self):
        zt_config_instance_name = str(uuid.uuid4()).replace('-', '')[:10]
        nw_name = str(uuid.uuid4()).replace('-', '')[:10]
        self.zt_client = j.clients.zerotier.get(instance=zt_config_instance_name, data={'token_': self.zt_token})
        self.zt_network = self.zt_client.network_create(public=False, name=nw_name, auto_assign=True,
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

    def create_account(self):
        self.acount_name = str(uuid.uuid4()).replace('-', '')[:10]
        self.account_client = self.client_ovc.account_get(self.acount_name)
        print(colored(' [*] Account: %s' % self.acount_name, 'green'))

    def create_cloudspace(self):
        cs_name = str(uuid.uuid4()).replace('-', '')[:10]
        self.cs_client = self.account_client.space_get(cs_name)
        print(' [*] CS: %s' % cs_name, 'green')

    def create_zos_node(self):
        zos_name = str(uuid.uuid4()).replace('-', '')[:10]
        self.zos_vm = self.cs_client.machine_create(name=zos_name, memsize=8, disksize=10, datadisks=[10],
                                                    image='ipxe boot',
                                                    authorize_ssh=False, userdata=self.ipxe)
        self.zos_ip = self.authorize_zos()
        zos_cfg = {"host": self.zos_ip}
        self.zos_client = j.clients.zos.get(instance=zos_name, data=zos_cfg)
        self.zos_node = j.clients.zos.sal.get_node(instance=zos_name)
        print(colored(' [*] ZOS: %s' % zos_name, 'green'))

    def authorize_zos(self):
        znw_member = self.zt_network.member_get(address=self.zt_network.members_list()[0].address)
        znw_member.authorize()
        return znw_member.private_ip

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

        print('[*] Create zerotier network interface')
        self.private_net = self.gw.networks.add_zerotier(self.zt_network)
        self.private_net.hosts.nameservers = ['8.8.8.8']

        self.gw.deploy()

    def deploy_zdb_disk(self):
        print(colored(' [*] Deploy ZDB disk', 'white'))
        destination_dict = str(uuid.uuid4()).replace('-', '')[:10]
        self.zos_node.client.bash('mkdir -p /var/cache/%s' % destination_dict)
        zdb = self.zos_node.primitives.create_zerodb('myzdb', '/var/cache/zdb')
        self.disk = self.zos_node.primitives.create_disk('mydisk', zdb, filesystem='btrfs')
        self.disk.deploy()

    def create_ubuntu_vms(self, source_port, destination_port):
        print(colored(' [*] Create an ubuntu machine.', 'white'))
        vm_name = str(uuid.uuid4()).replace('-', '')[:10]
        sshkey_instance = str(uuid.uuid4()).replace('-', '')[:10]
        self.ubuntu_vm_ip = '192.168.103.%i' % random.randint(1, 254)
        self.ubuntu_vm = self.zos_node.primitives.create_virtual_machine(vm_name, 'ubuntu:latest')
        self.ubuntu_vm.disks.add(self.disk)
        self.ubuntu_vm.configs.add(sshkey_instance, '/root/.ssh/authorized_keys', self.ssh_key)

        self.private_net.hosts.add(self.ubuntu_vm, self.ubuntu_vm_ip)
        self.gw.portforwards.add('httpforward', (self.public_net, source_port), (self.ubuntu_vm_ip, destination_port))

        self.gw.deploy()
        self.ubuntu_vm.deploy()

    def install_zt_host(self):
        print(colored(' [*] Install zerotier client', 'white'))
        try:
            j.tools.prefab.local.network.zerotier.install()
        finally:
            j.tools.prefab.local.network.zerotier.start()
