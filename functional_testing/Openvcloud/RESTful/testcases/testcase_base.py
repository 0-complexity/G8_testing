import time, signal, logging
from datetime import timedelta
from unittest import TestCase
from nose.tools import TimeExpired
from testconfig import config
from framework.api.client import Client
from framework.utils.utils import Utils

class TestcasesBase(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lg = self.logger()

    @classmethod
    def setUpClass(cls):
        cls.api = Client()
        cls.utils = Utils()
        cls.whoami = config['main']['username']
        cls.CLEANUP = {'users':[], 'accounts':[], 'groups':[]}
  
    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self._testID = self._testMethodName
        self._startTime = time.time()
        self.lg.info('====== Testcase [{}] is started ======'.format(self._testID))

        def timeout_handler(signum, frame):
            raise TimeExpired('Timeout expired before end of test %s' % self._testID)

        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(540)

    def tearDown(self):
        self._endTime = time.time()
        self._duration = int(self._endTime - self._startTime)
        self.lg.info('Testcase [{}] is ended, Duration: {} seconds'.format(self._testID, self._duration))

        for accountId in self.CLEANUP['accounts']:
            self.lg.info('[TearDown] Deleting account: {}'.format(accountId))
            self.api.cloudbroker.account.delete(accountId=accountId)

        for username in self.CLEANUP['users']:
            self.lg.info('[TearDown] Deleting user: {}'.format(username))
            self.api.cloudbroker.user.delete(username=username)

    def logger(self):
        logger = logging.getLogger('OVC')
        if not logger.handlers:
            fileHandler = logging.FileHandler('testsuite.log', mode='w')
            formatter = logging.Formatter(' %(asctime)s - %(name)s - [%(levelname)s] - %(message)s')
            fileHandler.setFormatter(formatter)
            logger.addHandler(fileHandler)

        return logger