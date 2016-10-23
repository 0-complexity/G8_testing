import logging
import unittest
import uuid
import time
import signal
from nose.tools import TimeExpired
from testconfig import config
import configparser
from JumpScale import j
import gevent
from gevent.subprocess import Popen, PIPE
import socket
import os
from gevent.lock import BoundedSemaphore
_cloudspace_semaphores = dict()
_stats = dict(deployed_vms=0, deployed_cloudspaces=0)
_vmnamecache = dict()


class BaseTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(BaseTest, self).__init__(*args, **kwargs)
        self.environment = config['main']['environment']
        self.username = config['main']['username']
        self.password = config['main']['password']
        self.vmachines = config['main']['vmachines']
        self.j = j

    def setUp(self):
        self._testID = self._testMethodName
        self._startTime = time.time()
        self._logger = logging.LoggerAdapter(logging.getLogger('jumpscale_testsuite'),
                                             {'testid': self.shortDescription() or self._testID})

        def timeout_handler(signum, frame):
            raise TimeExpired('Timeout expired before end of test %s' % self._testID)

        # adding a signal alarm for timing out the test if it took longer than 15 minutes
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(900)
        self.ovc = self.j.clients.openvcloud.get(self.environment,
                                                 self.username,
                                                 self.password)

        self.account_id = self.get_account()
        self.gid = self.get_gid()

    def tearDown(self):
        """
        Environment cleanup and logs collection.
        """
        if hasattr(self, '_startTime'):
            executionTime = time.time() - self._startTime
        self.lg('Testcase %s ExecutionTime is %s sec.' % (self._testID, executionTime))

    def lg(self, msg):
        self._logger.info(msg)

    def push_results_to_repo(self, res_dir):
        config = configparser.ConfigParser()
        config.read("locations.cfg")
        if self.environment not in config.options('locations'):
            raise AssertionError('Please update the locations.cfg with your '
                                 'location:environment_repo to be able to '
                                 'push your results')
        repo = config.get("locations", self.environment)
        repo_dir = '/tmp/' + str(uuid.uuid4()) + '/'
        res_folder_name = res_dir.split('/')[-1]
        self.j.do.execute('mkdir -p %s' % repo_dir)
        self.j.do.execute('cd %s; git clone %s' % (repo_dir, repo))
        repo_path = self.j.do.listDirsInDir(repo_dir)[0]
        repo_result_dir = repo_path + '/testresults/'
        self.j.do.execute('mkdir -p %s' % repo_result_dir)
        self.j.do.execute('cp -rf %s %s' % (res_dir, repo_result_dir))
        self.j.do.chdir(repo_result_dir + res_folder_name)
        self.j.do.execute('git add *.csv ')
        self.j.do.execute("git commit -a -m 'Pushing new results' ")
        self.j.do.execute('git push')

    def get_account(self):
        account = self.ovc.api.cloudapi.accounts.list()
        if len(account) != 1:
            raise AssertionError('FAILURE: Expected to only find 1 account and found {}'.format(len(account)))
        return account[0]['id']

    def get_gid(self):
        gid = next((loc['gid'] for loc in self.ovc.api.cloudapi.locations.list() if loc['locationCode'] == self.environment),
                    None)
        if gid is None:
            raise AssertionError('FAILURE: Could not determine gid')
        return  gid

    def check_package(self, package):
        try:
            self.run_cmd_via_gevent('dpkg -l {}'.format(package))
            return True
        except RuntimeError:
            self.lg("Dependant package {} is not installed".format(package))
            return False

    def run_cmd_via_gevent(self, cmd):
        sub = Popen([cmd], stdout=PIPE, stderr=PIPE, shell=True)
        out, err = sub.communicate()
        if sub.returncode == 0:
            return out.decode('utf-8')
        else:
            error_output = err.decode('utf-8')
            raise RuntimeError("Failed to execute command.\n\ncommand:\n{}\n\n".format(cmd, error_output))

    def wait_until_remote_is_listening(self, address, port):
        while True:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect((address, port))
                s.close()
                break
            except ConnectionAbortedError:
                gevent.sleep(1)
            except ConnectionRefusedError:
                gevent.sleep(1)
            except TimeoutError:
                gevent.sleep(1)
            s.close()

    def check_remote_is_listening(self, address, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((address, port))
        finally:
            s.close()

    def safe_get_vm(self, concurrency, machine_id):
        while True:
            try:
                if concurrency is None:
                    return self.ovc.api.cloudapi.machines.get(machineId=machine_id)
                with concurrency:
                    return self.ovc.api.cloudapi.machines.get(machineId=machine_id)
            except Exception as e:
                print("Failed to get vm details for machine {}".format(machine_id))
                gevent.sleep(2)


    def get_publicport_semaphore(self, cloudspace_id):
        if cloudspace_id not in _cloudspace_semaphores:
            _cloudspace_semaphores[cloudspace_id] = BoundedSemaphore()
        return _cloudspace_semaphores[cloudspace_id]


    def get_cloudspace_template_vm_id(self, concurrency, cloudspace_id):
        machine_name = self.get_vm_name(cloudspace_id, 0)
        if machine_name in _vmnamecache:
            return _vmnamecache[machine_name]
        with self.get_publicport_semaphore(cloudspace_id):
            if machine_name in _vmnamecache:
                return _vmnamecache[machine_name]

            machines = self.ovc.api.cloudapi.machines.list(cloudspaceId=cloudspace_id)
            vm_id = next(m['id'] for m in machines if m['name'] == machine_name)

            def stop():
                print("Stopping machine {}".format(machine_name))
                self.ovc.api.cloudapi.machines.stop(machineId=vm_id)

            if concurrency is None:
                stop()
            else:
                with concurrency:
                   stop()
            while True:
                gevent.sleep(1)
                vm = self.safe_get_vm(concurrency, vm_id)
                if vm['status'] == 'HALTED':
                    break
            _vmnamecache[machine_name] = vm_id
            return vm_id
'''
    def install_req(self, machine, cloudspace, public_port, name):
        account = machine['accounts'][0]

        # Wait until vm accepts connections
        self.wait_until_remote_is_listening(cloudspace['publicipaddress'], public_port)

        # Copy install_deps.sh to vm
        templ = 'sshpass -p "{0}" scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'
        templ += ' -P {1} install_deps.sh {2}@{3}:/home/{2}'
        cmd = templ.format(account['password'], public_port, account['login'], cloudspace['publicipaddress'])
        self.run_cmd_via_gevent(cmd)

        # Run bash script on vm
        templ = 'sshpass -p "{0}" ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p {1} {2}@{3} '
        templ += '\'echo "{0}" | sudo -S bash /home/{2}/install_deps.sh\''
        cmd = templ.format(account['password'], public_port, account['login'], cloudspace['publicipaddress'])
        self.run_cmd_via_gevent(cmd)


    def safe_deploy_vm(self, name, cloudspace_id, image_id, force_create=False):
        while True:
            try:
                self.deploy_vm(name, cloudspace_id, image_id, force_create)
                return
            except Exception as e:
                templ = "Failed creating machine {} in cloudspace {}, \nError: {}\nretrying ..."
                self.lg(templ.format(name, cloudspace_id, str(e)))
                gevent.sleep(10)
                while True:
                    try:
                        machines = self.ovc.api.cloudapi.machines.list(cloudspaceId=cloudspace_id)
                        machine_id = next((m['id'] for m in machines if m['name'] == name), None)
                        if machine_id is None:
                            break
                        self.ovc.api.cloudapi.machines.delete(machineId=machine_id)
                        break
                    except Exception as e:
                        templ = "Failed cleaning up machine {} in cloudspace {}, \nError: {}\nretrying ..."
                        self.lg(templ.format(name, cloudspace_id, str(e)))
                        gevent.sleep(10)


    def deploy_vm(self, options, account_id, gid, name, cloudspace_id, image_id, force_create=False):
        # Listing sizes
        sizes = self.ovc.api.cloudapi.sizes.list(cloudspaceId=cloudspace_id)
        size_id = next((s['id'] for s in sizes if (options.bootdisk in s['disks'] and
                                                   options.memory == s['memory'] and
                                                   options.cpu == s['vcpus'])), None)
        if size_id is None:
            raise ValueError("No matching size for vm found.")

        if options.iops < 0:
            raise ValueError("Maximum iops can't be a negative value")

        clone = not force_create

        # Create vm
        with concurrency:
            if clone:
                print("Cloning {}".format(name))
                template_vm_id = self.get_cloudspace_template_vm_id(None, cloudspace_id)
                vm_id = self.ovc.api.cloudapi.machines.clone(machineId=template_vm_id, name=name)
            else:
                print("Creating {}".format(name))
                vm_id = self.ovc.api.cloudapi.machines.create(cloudspaceId=cloudspace_id,
                                                         name=name,
                                                         description=name,
                                                         sizeId=size_id,
                                                         imageId=image_id,
                                                         disksize=options.bootdisk,
                                                         datadisks=[int(options.datadisk)])


        # Wait until vm has ip address
        start = time.time()
        while True:
            gevent.sleep(5)
            machine = self.safe_get_vm(concurrency, vm_id)
            ip = machine['interfaces'][0]['ipAddress']
            if ip != 'Undefined':
                break
            now = time.time()
            if now > start + 600:
                raise RuntimeError("Machine {} did not get an ip within 600 seconds".format(vm_id))
            self.lg("Waiting {} seconds for an IP for VM {}".format(int(now - start), name))

        # Configure portforward to ssh port of vm
        self.lg("Configuring portforward for machine {}".format(name))
        cloudspace = self.ovc.api.cloudapi.cloudspaces.get(cloudspaceId=cloudspace_id)
        with self.get_publicport_semaphore(cloudspace_id):
            public_ports = [int(pf['publicPort']) for pf in ovc.api.cloudapi.portforwarding.list(cloudspaceId=cloudspace_id)]
            public_ports.append(19999)
            public_port = max(public_ports) + 1
            with concurrency:
                self.ovc.api.cloudapi.portforwarding.create(cloudspaceId=cloudspace_id,
                                                       publicIp=cloudspace['publicipaddress'],
                                                       publicPort=public_port,
                                                       machineId=vm_id,
                                                       localPort=22,
                                                       protocol='tcp')

        if not clone:
            # Install fio & unixbench via cuisine on the vm
            self.install_req(machine, cloudspace, public_port, name)

        print("Machine {} deployed succesfully.".format(name))
        _stats['deployed_vms'] += 1


    def get_vm_name(self, cloudspace_id, counter):
        return "vm-{0}-{1:0>3}".format(cloudspace_id, counter)


    def deploy_cloudspace(self, account_id, name, image_id, gid):
        # Create cloudspace
        self.lg("Creating cloudspace {}".format(name))
        cloudspace_id = self.ovc.api.cloudapi.cloudspaces.create(accountId=account_id,
                                                            location=self.environment,
                                                            name=name,
                                                            access=self.username)
        # Create first vm to force the routeros deployment
        self.lg("Deploying first vm in cloudspace {}".format(name))
        self.safe_deploy_vm(account_id, gid, self.get_vm_name(cloudspace_id, 0),
                       cloudspace_id, image_id, force_create=True)

        # Deploy the remaining vms
        jobs = [gevent.spawn(self.safe_deploy_vm, account_id, gid,
                             self.get_vm_name(cloudspace_id, x),
                             cloudspace_id, image_id) for x in range(1, self.vmachines)]
        gevent.joinall(jobs)

        _stats['deployed_cloudspaces'] += 1
'''