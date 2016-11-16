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
