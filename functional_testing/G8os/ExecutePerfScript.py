import requests
from g8os import resourcepool
import paramiko
import time

execution_time = 12*3600
output = '12hour'

resourcepoolip = '10.244.188.186'
controllerip = '10.101.107.254'
username = ''
password = ''

resoucepoolserver = 'http://10.244.188.186:8080'
nodes_number = 9
node_ssd = 7
driver_type = 'ssd'


def get_nodes_id():
    nodes_id = []
    for i in range(300):
        nodes = client.nodes.ListNodes().json()
        if len(nodes) < 9:
            time.sleep(30)
            print(' [*] nodes number = %d' % len(nodes))
        else:
            print(' [*] nodes number = %d' % len(nodes))
            break
            
    for node in nodes:
        if node['hostname'] != 'cpu-10':
            nodes_id.append(node['id'])
    print(' [*]', nodes_id)
    return nodes_id

def create_storagecluster(nodes_id):
    print( ' [*] Create storage cluster : xTremX')
    data = {"label": 'xTremX',
            "servers": nodes_number*node_ssd,
            "driveType": driver_type,
            "nodes": nodes_id}
    client.storageclusters.DeployNewCluster(data=data)

def check_storagecluster_status():
    print(' [*] Check storage cluster status')
    status = client.storageclusters.GetClusterInfo(label='xTremX').json()['status']
    print('[*] Cluster status : %s ' % status)

def get_ssh_client(ip, user='', password=''):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if ip == resourcepoolip:
        ssh_client.connect(ip, port=22)
    else:
        ssh_client.connect(ip, port=22, username=user, password=password)
    return ssh_client

def execute_command(ssh_client, command):
    for i in range(100):
        stdin, stdout, stderr = ssh_client.exec_command(cmd)
        tracback = stdout.readlines()
        if not stderr.readlines():
            print(' [OK!] ')
            break
        else:
            time.sleep(3)
    else:
        import ipdb; ipdb.set_trace()

ssh_resoucepool = get_ssh_client(ip=resourcepoolip)
cmd = 'cd /optvar/cockpit_repos/resourcepool-server && ays repo destroy'
print(' [*] %s ' % cmd)
execute_command(ssh_resoucepool, cmd)
time.sleep(60)

ssh_controller = get_ssh_client(ip=controllerip, user=username, password=password)
cmd = 'for i in {71..79}; do ipmitool -I lanplus -H 10.107.2.${i} -U ADMIN -P ADMIN chassis power cycle; done'
print(' [*] %s ' % cmd)
execute_command(ssh_controller, cmd)
time.sleep(60)

cmd = 'cd /root/resourcepool/scripts && python3 diskwiper.py 10.107.2.11 10.107.2.12 10.107.2.13 10.107.2.14 10.107.2.15 10.107.2.16 10.107.2.17 10.107.2.18 10.107.2.19'
print(' [*] %s ' % cmd)
execute_command(ssh_resoucepool, cmd)

cmd = 'cd /optvar/cockpit_repos/resourcepool-server && ays blueprint bootstrap.bp && ays run create -y'
print(' [*] %s ' % cmd)
execute_command(ssh_resoucepool, cmd)

client = resourcepool.Client(resoucepoolserver).api
create_storagecluster(nodes_id=get_nodes_id())
check_storagecluster_status()

cmd = """ tmux new-session -d -s bd-performance "cd /root/resourcepool/tests && python3 bd-performance.py --resourcepoolserver http://10.244.188.186:8080 --storagecluster xTremX --vdiskCount 99 --vdiskSize 10 --runtime %d --vdiskType db --resultDir /root/%s --nodeLimit 9; bash -i" """ % (execution_time, output)
print(' [*] %s ' % cmd)
execute_command(ssh_resoucepool, cmd)

