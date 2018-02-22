import time, signal, logging
from datetime import timedelta
from unittest import TestCase
from nose.tools import TimeExpired
from testconfig import config
from framework.api.client import Client
from framework.utils.utils import Utils
from testconfig import config

client_id = config['main']['client_id']
client_secret = config['main']['client_secret']

class TestcasesBase(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lg = self.logger()

    @classmethod
    def setUpClass(cls):
        cls.api= Client(client_id=client_id, client_secret=client_secret)
        cls.utils = Utils()
        cls.whoami = config['main']['username']
  
    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self._testID = self._testMethodName
        self.CLEANUP = {'users':[], 'accounts':[]}
        self._startTime = time.time()
        self.lg.info('====== Testcase [{}] is started ======'.format(self._testID))
        self.user_api = Client()
        def timeout_handler(signum, frame):
            raise TimeExpired('Timeout expired before end of test %s' % self._testID)

        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(540)

    def tearDown(self):
        self._endTime = time.time()
        self._duration = int(self._endTime - self._startTime)
        for accountId in self.CLEANUP['accounts']:
            self.api.cloudbroker.accounts.delete(accountId)
        
        for user in self.CLEANUP['users']:
            self.api.cloudbroker.user.delete(user)
            
        self.lg.info('Testcase [{}] is ended, Duration: {} seconds'.format(self._testID, self._duration))

    def logger(self):
        logger = logging.getLogger('OVC')
        if not logger.handlers:
            fileHandler = logging.FileHandler('testsuite.log', mode='w')
            formatter = logging.Formatter(' %(asctime)s - %(name)s - [%(levelname)s] - %(message)s')
            fileHandler.setFormatter(formatter)
            logger.addHandler(fileHandler)

        return logger