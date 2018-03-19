import logging, time
from utils import Utils
from unittest import TestCase
from testconfig import config
from minio import Minio

class TestcasesBase(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log = self.logger()

    @classmethod
    def setUpClass(cls):
        cls.utils = Utils()
        cls._url = config['minio']['url']
        cls._access_key = config['minio']['access_key']
        cls._secret_key = config['minio']['secret_key']
        cls.minio = Minio(cls._url, access_key=cls._access_key, secret_key=cls._secret_key, secure=False)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self._testID = self._testMethodName
        self._startTime = time.time()
        self.CLEANUP = {'buckets':[]}
        self.log.info('====== Testcase [{}] is started ======'.format(self._testID))

    def tearDown(self):
        self._endTime = time.time()
        self._duration = int(self._endTime - self._startTime)
        self.log.info('Testcase [{}] is ended, Duration: {} seconds'.format(self._testID, self._duration))

        for bucket_name in self.CLEANUP['buckets']:
            self.log.info('[TearDown] Deleting bucket {}'.format(bucket_name))
            if self.minio.bucket_exists(bucket_name):
                objects = self.minio.list_objects(bucket_name, recursive=True) 
                for error in self.minio.remove_objects(bucket_name, [obj.object_name for obj in objects]):
                    self.log.error(error)
                self.minio.remove_bucket(bucket_name) 

    def logger(self):
        logger = logging.getLogger('Minio')
        if not logger.handlers:
            fileHandler = logging.FileHandler('testsuite.log', mode='w')
            formatter = logging.Formatter(' %(asctime)s - %(name)s - [%(levelname)s] - %(message)s')
            fileHandler.setFormatter(formatter)
            logger.addHandler(fileHandler)

        return logger