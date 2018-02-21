import uuid, random, os
import logging
import signal,time
from testconfig import config
from testcases import *

class Utils:
    def __init__(self):
        pass


    def setUp(self):

        self.CLEANUP = {'username': [], 'accountId': [],'groupname':[]}
        self._testID = self._testMethodName
        self._startTime = time.time()
        self._logger = logging.LoggerAdapter(logging.getLogger('openvcloud_testsuite'),
                                             {'testid': self.shortDescription() or self._testID})

        def timeout_handler(signum, frame):
            raise TimeExpired('Timeout expired before end of test %s' % self._testID)

        # adding a signal alarm for timing out the test if it took longer than 15 minutes
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(2000)

    def random_string(self, length=10):
        return str(uuid.uuid4()).replace('-', '')[0:length]

