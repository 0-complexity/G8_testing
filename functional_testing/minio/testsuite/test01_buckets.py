import time, random, unittest
from minio.error import NoSuchBucket, BucketAlreadyOwnedByYou, InvalidBucketError
from testcase_base import *

class BucketsTests(TestcasesBase):
    def setUp(self):
        super().setUp()
        self.log.info('Create bucket (B1), should succeed')
        self.bucket_name = self.utils.random_string()
        self.minio.make_bucket(self.bucket_name)
        self.CLEANUP['buckets'].append(self.bucket_name)

    def test01_make_bucket(self):
        """ MIN-001
        #. Create bucket (B1), should succeed.
        #. Create new bucket with the same name of bucket (B1), should fail.
        #. Create bucket with invalid name, should fail.
        """
        self.log.info('Create bucket (B1), should succeed')
        bucket_name = self.utils.random_string()
        self.minio.make_bucket(bucket_name)

        self.log.info('Create new bucket with the same name of bucket (B1), should fail')        
        with self.assertRaises(BucketAlreadyOwnedByYou):
            self.minio.make_bucket(self.bucket_name)

        self.log.info('Create new bucket with invalid name, should fail')        
        with self.assertRaises(InvalidBucketError):
            invalid_bucket_name = self.utils.random_string(length=2)
            self.minio.make_bucket(invalid_bucket_name)

    def test02_list_buckets(self):
        """ MIN-002
        #. Create bucket (B1), should succeed.
        #. List buckets, (B1) should be listed.
        """
        self.log.info('List buckets, (B1) should be listed')
        buckets = self.minio.list_buckets()
        self.assertIn(self.bucket_name, [bucket.name for bucket in buckets])

    def test03_bucket_exists(self):
        """ MIN-003
        #. Create bucket (B1), should succeed.
        #. Check if bucket (B1) exists, should be True.
        #. Check if non-existing bucket exists, should be False.
        """
        self.log.info('Check if bucket (B1) exists, should be True')
        self.assertTrue(self.minio.bucket_exists(self.bucket_name))

        self.log.info('Check if non-existing bucket exists, should be False')
        fake_bucket = self.utils.random_string()
        self.assertFalse(self.minio.bucket_exists(fake_bucket))

    def test04_remove_bucket(self):
        """ MIN-004
        #. Create bucket (B1), should succeed.
        #. Remove bucket (B1), should succeed.
        #. Try to remove non-existing bucket, should fail.
        """
        self.log.info('Remove bucket (B1), should succeed')
        self.minio.remove_bucket(self.bucket_name)

        self.log.info('Try to remove non-existing bucket, should fail')
        with self.assertRaises(NoSuchBucket):
            self.minio.remove_bucket(self.utils.random_string())

    def test05_list_objects(self):
        """ MIN-005
        #. Create bucket (B1), should succeed.
        #. Add object (O1) to bucket (B1), should succeed.
        #. List bucket (B1) objects, Object (O1) should be listed.
        #. List bucket (B1) objects recursively, Object (O1) should be listed.
        """
        self.log.info('Add object (O1) to bucket (B1), should succeed')        
        obj = self.utils.create_object()
        self.CLEANUP['local_files'].append(obj['path'])

        self.minio.fput_object(self.bucket_name, obj['prefix'], obj['path'])

        self.log.info('List bucket (B1) objects, Object (O1) should be listed')
        objects = self.minio.list_objects(self.bucket_name)
        self.assertIn(obj['prefix'][:obj['prefix'].find('/')+1], [obj.object_name for obj in objects])

        self.log.info('List bucket (B1) objects recursively, Object (O1) should be listed')
        objects = self.minio.list_objects(self.bucket_name, recursive=True)
        self.assertIn(obj['prefix'], [obj.object_name for obj in objects])
 
    def test06_list_objects_v2(self):
        """ MIN-006
        #. Create bucket (B1), should succeed.
        """
        pass

    def test07_list_incomplete_uploads(self):
        """ MIN-007
        #. Create bucket (B1), should succeed.
        """
        pass