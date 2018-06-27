from primitives import PRIMITAVES
'''
    Use this tool to construct n of zOS node each of them has a k of ubuntu vms connect with each other through a vlan.

    Script flow description:
     -  Get parameters.
     -  Install zerotier client.
     -  Create a new zerotier nw.
     -  Host join this zerotier nw.
     -
'''

import argparse, requests
from termcolor import colored
from js9 import j

print(colored(' [*] Get parameters', 'white'))
parser = argparse.ArgumentParser()
parser.add_argument("-n", dest="zos_nodes", type=int, default=1, help="no. of zos nodes, default 1")
parser.add_argument("-k", dest="ubuntu_vms", type=int, default=1, help="no. of ubuntu vms, default 1")
args = parser.parse_args()

NUMBER_OF_ZOS_NODES = args.zos_nodes
NUMBER_OF_UBUNTU_VMS = args.ubuntu_vms

SSHKEY = 'ssh-rsa ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDcxh3D1DcfLQH2C4IgUTwaBAPkWI3stuYzunSZpjzq3GGkufgUHrxjSEzQ0RkEhs9LyrkTC+UJAQ2cG920J728KYiq+cBZgd5vRblXZ9niAe5pf71vFWN7OKj8zflF22XUdgbmQKLwIvl1gTQPB0WCMhY2j1iis1G0yPyxWmLFpxh4aPyEOvTjRWV1O6s9Yvv5Sqoqt4dwJwmbquHuz7Npo/86W0GN4qf4ZPft2KEYbtE5tCx7LWCvbUNPBf1215z81iDzkzQM5A8Sin0phexzEcU6Tegsw9VCvONOoPYKnYFaexvSB5XrrPLl7/2K7soOu2ieFoiOqsPwBFBMiFU5qKHfu/h4n+bk39gw9B64/S/Zk6WNALS18g+g26zXSAo3lFZdWw9X6bQmk7jEx6B/ZlpdegzYkQDN91dZU6DkAWWXg4XazdekOmcyEE86oJqOW8pJpBGTZ4qFYYOklgkgtXoiKpcHbVft9Dne1F3msVNDDZeEcaW2N43lArRf26EvD0y1DG76canGZJnfETzEv8LfkfH6AQ/StiMwRrA91Z6Y6zlYFPO7DVLxmpapWmJu8uVrhwPqbAq7PDQLmDH/t3eVc838be0BRMQ8A6jlfV9IW9OwZ73IThu5RenwatCLyyVYOmUV+aK/a5+HpPYxd2OIkTtwZB4xqM7n0cPWNw== /home/dina/.ssh/id_rsa'
IYO_CLIENT_ID = 'x07qa5MpigcqjQWQY2X6cHW-O0Ly'
IYO_CLIENT_SECRET = 'UnLW2HoTaWgmtmIRnabTwq2iPB42'
PACKET_AUTH = ''
ZT_TOKEN = 'jp5CUSmvwTWnuvJRz7T1tXKka1grUspu'
OVC_DATA = {"address": "be-g8-3.demo.greenitglobe.com",
            "location": "be-g8-3",
            "port": 443}


print(colored(' [*] Get jwt', 'grey'))
get_jwt = requests.post(
    'https://itsyou.online/v1/oauth/access_token?grant_type=client_credentials&client_id=%s&client_secret=%s&response_type=id_token' % (
        IYO_CLIENT_ID, IYO_CLIENT_SECRET))
jwt = get_jwt.text

OVC_DATA['jwt_'] = jwt

obj = PRIMITAVES(ovc_data=OVC_DATA, zt_token=ZT_TOKEN, ssh_key=SSHKEY)
obj.install_zt_host()
obj.create_zerotier_nw()
obj.host_join_zt()
import ipdb; ipdb.set_trace()
obj.create_account()
obj.create_cloudspace()
obj.create_zos_node()
obj.create_ovs_container()
obj.create_gw_passthrough_vlan()
obj.deploy_zdb_disk()
obj.create_ubuntu_vms_vlan(22022,22)
import ipdb; ipdb.set_trace()