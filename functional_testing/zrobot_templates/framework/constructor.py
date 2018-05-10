import os
import uuid
import logging
import time
import unittest
from js9 import j
from testconfig import config
from requests.exceptions import HTTPError
from jinja2 import Environment, FileSystemLoader
from zerorobot.dsl.ZeroRobotAPI import ZeroRobotAPI
from zerorobot.cli import utils


class constructor(unittest.TestCase):

    def __init__(self, templatespath, *args, **kwargs):
        super(constructor, self).__init__(*args, **kwargs)
        self.j2_env = Environment(loader=FileSystemLoader(searchpath=templatespath), trim_blocks=True)
        self.j2_env.globals.update(random_string=self.random_string)
        self.j2_env.globals.update(config_params=self.config_params)
        self.api = ZeroRobotAPI()
        instance, _ = utils.get_instance()
        self.zrobot_client = j.clients.zrobot.get(instance)

    def setUp(self):
        self._testID = self._testMethodName
        self._startTime = time.time()
        self._logger = logging.LoggerAdapter(logging.getLogger('openvcloud_testsuite'),
                                             {'testid': self.shortDescription() or self._testID})

    @staticmethod
    def random_string():
        return str(uuid.uuid4())[0:8]

    def config_params(self, param):
        return config['main'][param]

    def log(self, msg):
        self._logger.info(msg)

    def create_blueprint(self, yaml, **kwargs):
        """
        yaml file that is used for blueprint creation
        """
        blueprint = self.j2_env.get_template('base.yaml').render(services=yaml,
                                                                 actions='actions.yaml',
                                                                 **kwargs)
        return blueprint

    def update_zrobot_client_secrets(response):
        header = 'Bearer '
        for service in response.services:
            header += '%s ' % service.secret
        self.zrobot_client.api.security_schemes.passthrough_client_zrobot.set_zrobot_header(header)

    def execute_blueprint(self, blueprint):
        os.system('echo "{0}" >> /tmp/{1}.yaml'.format(blueprint, self.random_string()))
        content = j.data.serializer.yaml.loads(blueprint)
        data = {'content': content}
        try:
            response, _ = self.zrobot_client.api.blueprints.ExecuteBlueprint(data)
            self.update_zrobot_client_secrets(response)
            result = dict()
            for task in response.tasks:
                if task.service_name in result.keys():
                    result[task.service_name].update({task.action_name: task.guid})
                else:
                    result[task.service_name] = {task.action_name: task.guid}
            return result
        except HTTPError as err:
            msg = err.response.json()['message']
            self.log('message: %s' % msg)
            self.log('code: %s' % err.response.json()['code'])
            return msg

    def delete_services(self):
        for r in self.api.robots.keys():
            robot = self.api.robots[r]
            for service in robot.services.names.values():
                service.delete()

    def wait_for_service_action_status(self, servicename, task_guid, timeout=100):
        for service in self.zrobot_client.api.services.listServices()[0]:
            if service.name == servicename:
                break
        else:
            raise ValueError('service not found')
        task = self.zrobot_client.api.services.GetTask(task_guid, service.guid)[0]
        for _ in range(timeout):
            time.sleep(1)
            if task.state == 'ok':
                break
            elif task.state == 'error':
                self.log(task.eco.printTraceback())
                return task.eco.errormessage

    def check_if_service_exist(self, servicename):
        for r in self.api.robots.keys():
            robot = self.api.robots[r]
            if servicename in robot.services.names.keys():
                return True
            return False
