import time, random, unittest
from minio.error import NoSuchBucket, BucketAlreadyOwnedByYou, InvalidBucketError, NoSuchKey
from testcase_base import *
from nose_parameterized import parameterized

class ObjectsTests(TestcasesBase):
    def setUp(self):
        super().setUp()
        self.log.info('Create bucket (B1), should succeed')
        self.bucket_name = self.utils.random_string()
        self.minio.make_bucket(self.bucket_name)
        self.CLEANUP['buckets'].append(self.bucket_name)

        self.log.info('Create object (O1) in bucket (B1), should succeed')
        self.file_path, self.object_data = self.utils.create_file()        
        self.object_name = self.utils.random_string()
        self.minio.fput_object(self.bucket_name, self.object_name, self.file_path)

    def test01_get_object(self):
        """ MIN-01
        #. Create bucket (B1), should succeed.
        #. Create object (O1) in bucket (B1), should succeed.
        #. Get object (O1), should succeed.
        #. Get non-existing object, should fail.
        """
        self.log.info('Get object (O1), should succeed')
        data = self.minio.get_object(self.bucket_name, self.object_name)
        self.assertEqual(data.data.decode('utf-8').strip(), self.object_data)

        self.log.info('Get object of non-existing bucket, should fail')
        fake_bucket_name = self.utils.random_string()
        with self.assertRaises(NoSuchBucket):
            self.minio.get_object(fake_bucket_name, self.object_name)

        self.log.info('Get non-existing object, should fail')
        fake_object_name = self.utils.random_string()
        with self.assertRaises(NoSuchKey):
            self.minio.get_object(self.bucket_name, fake_object_name)

    def test02_fget_object(self):
        """ MIN-02
        #. Create bucket (B1), should succeed.
        """
        pass

    def test03_get_partial_object(self):
        """ MIN-03
        #. Create bucket (B1), should succeed.
        """
        pass
        
    def test04_put_object(self):
        """ MIN-04
        #. Create bucket (B1), should succeed.
        """
        pass

    def test05_fput_object(self):
        """ MIN-05
        #. Create bucket (B1), should succeed.
        """
        pass

    def test06_copy_object(self):
        """ MIN-05
        #. Create bucket (B1), should succeed.
        """
        pass

    def test07_stat_object(self):
        """ MIN-07
        #. Create bucket (B1), should succeed.
        """
        pass

    def test08_remove_object(self):
        """ MIN-08
        #. Create bucket (B1), should succeed.
        """
        pass

    def test09_remove_objects(self):
        """ MIN-09
        #. Create bucket (B1), should succeed.
        """
        pass

    def test10_remove_incomplete_upload(self):
        """ MIN-10
        #. Create bucket (B1), should succeed.
        """
        pass
        
