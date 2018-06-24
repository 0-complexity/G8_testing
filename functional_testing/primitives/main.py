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

SSHKEY = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCjPfKUsaFuaGJsnHvF3k0PbqQTr3GL2pNuddn/xQjsroF35ELJVEovAsd9IlsFWOmDWlL6B+JYFgj8g5IykklHCDfmTu6LcGXjdfAYVp+eXARmgoCJKxVyenSVHu6No9O1e+QKFvMJTiJXdl08fZD1Fd2kRetDRKAijCZ76pmB4/KwVFiJKCVVdsDW/0R+td0gNVJyCQyRTcWEPmBfGMW/JrvRCSHfxlLdqsD3txLOm9pHlQ/LmEwOP3bqEEpQU1jP32JbdAdreuD6BYB+YRp02yyU33gd1QbqIEgftcN+6TuZJOU3j2VRSiUQX8h5SjtWV1UXE15ELlIlhcFJYH6L root@islamtaha-TT'
IYO_CLIENT_ID = 'wrzcIurg4zXEjlJOA1z0CX806jKx'
IYO_CLIENT_SECRET = 'WaKRgZgLTHdTfFEgkrSfieKkd734'
PACKET_AUTH = 'vqzwphNXwsr7LrBCAEX87iaqSbSBWxeZ'
ZT_TOKEN = 'MyuDhfUYxCkc8eCH8cA4bt4WMgR6saWT'
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

import ipdb; ipdb.set_trace()