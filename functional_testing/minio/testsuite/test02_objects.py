import time, random, unittest, os
from minio.error import NoSuchBucket, BucketAlreadyOwnedByYou, InvalidBucketError, NoSuchKey
from testcase_base import *
from datetime import datetime

class ObjectsTests(TestcasesBase):
    def setUp(self):
        super().setUp()
        self.log.info('Create bucket (B1), should succeed')
        self.bucket_name = self.utils.random_string()
        self.minio.make_bucket(self.bucket_name)
        self.CLEANUP['buckets'].append(self.bucket_name)

        self.log.info('Create object (O1) in bucket (B1), should succeed')
        self.object = self.utils.create_object()        
        self.etag = self.minio.fput_object(self.bucket_name, self.object['prefix'], self.object['path'])
        self.CLEANUP['local_files'].append(self.object['path'])

    def test01_get_object(self):
        """ MIN-008
        #. Create bucket (B1), should succeed.
        #. Create object (O1) in bucket (B1), should succeed.
        #. Get object (O1), should succeed.
        #. Get non-existing object, should fail.
        """
        self.log.info('Get object (O1), should succeed')
        data = self.minio.get_object(self.bucket_name, self.object['prefix'])
        self.assertEqual(data.data.decode('utf-8'), self.object['data'])

        self.log.info('Get non-existing object, should fail')
        with self.assertRaises(NoSuchKey):
            self.minio.get_object(self.bucket_name, self.utils.random_string())

    def test02_fget_object(self):
        """ MIN-009
        #. Create bucket (B1), should succeed.
        #. Create object (O1) in bucket (B1), should succeed.
        #. Download object (O1), should succeed.
        #. Check object (O1)'s data is correct, should succeed.
        """
        self.log.info('Download object (O1), should succeed')
        file_path = '/tmp/{}'.format(self.utils.random_string())
        self.minio.fget_object(self.bucket_name, self.object['prefix'], file_path)
        self.assertTrue(os.path.exists(file_path))
        self.CLEANUP['local_files'].append(file_path)

        self.log.info('Check object (O1)\'s data is correct, should succeed')
        self.assertEqual(self.utils.get_file_md5(file_path), self.object['md5'])

        self.log.info('Get non-existing object, should fail')
        with self.assertRaises(NoSuchKey):
            self.minio.fget_object(self.bucket_name, self.utils.random_string(), file_path)

    def test03_get_partial_object(self):
        """ MIN-010
        #. Create bucket (B1), should succeed.
        #. Create object (O1) in bucket (B1), should succeed.
        #. Get partial data of object (O1), should succeed.
        #. Check that data is correct, should succeed.
        #. Get partial data of non-existing object, should fail.
        """
        self.log.info('Get partial object (O1), should succeed')
        offset = random.randint(0, 5)
        length = random.randint(5, 10)
        data = self.minio.get_partial_object(self.bucket_name, self.object['prefix'], offset, length)

        self.log.info('Check that data is correct, should succeed')
        self.assertEqual(self.object['data'][offset:offset+length], data.data.decode('utf-8'))

        self.log.info('Get partial data of non-existing object, should fail')
        with self.assertRaises(NoSuchKey):
            self.minio.get_object(self.bucket_name, self.utils.random_string())
        
    def test04_put_object(self):
        """ MIN-011
        #. Create bucket (B1), should succeed.
        #. Create file (F1).
        #. Put file (F1) to bucket (B1) as object (O1), should succeed.
        #. Download object (O1), should succeed.
        #. Check data of object (O1) is correct, should succeed.
        """
        self.log.info('Create file (F1)')
        obj = self.utils.create_object()
        self.CLEANUP['local_files'].append(obj['path'])

        self.log.info('Put file (F1) to bucket (B1) as object (O1), should succeed')
        metadata = {self.utils.random_string():self.utils.random_string()}
        etag = self.minio.put_object(self.bucket_name, obj['prefix'], obj['decr'], obj['stat'].st_size, metadata=metadata)

        self.log.info('Download object (O1), should succeed')
        file_path = '/tmp/{}'.format(self.utils.random_string())
        downloaded_obj = self.minio.fget_object(self.bucket_name, obj['prefix'], file_path)
        self.CLEANUP['local_files'].append(file_path)

        self.log.info('Check data of object (O1) is correct, should succeed')
        self.assertEqual(self.utils.get_file_md5(file_path), obj['md5'])
        self.assertEqual(downloaded_obj.etag, etag)

    def test05_fput_object(self):
        """ MIN-012
        #. Create bucket (B1), should succeed.
        #. Create file (F1).
        #. Upload file (F1) to bucket (B1) as object (O1), should succeed.
        #. Download object (O1), should succeed.
        #. Check data of object (O1) is correct, should succeed.
        """
        self.log.info('Create file (F1)')
        obj = self.utils.create_object()
        self.CLEANUP['local_files'].append(obj['path'])

        self.log.info('Upload file (F1) to bucket (B1) as object (O1), should succeed')
        metadata = {self.utils.random_string():self.utils.random_string()}
        etag = self.minio.fput_object(self.bucket_name, obj['prefix'], obj['path'], metadata=metadata)

        self.log.info('Download object (O1), should succeed')
        file_path = '/tmp/{}'.format(self.utils.random_string())
        downloaded_obj = self.minio.fget_object(self.bucket_name, obj['prefix'], file_path)
        self.CLEANUP['local_files'].append(file_path)

        self.log.info('Check data of object (O1) is correct, should succeed')
        self.assertEqual(self.utils.get_file_md5(file_path), obj['md5'])
        self.assertEqual(downloaded_obj.etag, etag)

    def test06_copy_object(self):
        """ MIN-013
        #. Create bucket (B1), should succeed.
        #. Create object (O1) in bucket (B1), should succeed.
        """
        pass

    def test07_stat_object(self):
        """ MIN-014
        #. Create bucket (B1), should succeed.
        #. Create object (O1) in bucket (B1), should succeed.
        #. Get stat of object (O1), should succeed.
        #. Get stat data of non-existing object, should fail.
        """
        self.log.info('Get stat of object (O1), should succeed')
        obj = self.minio.stat_object(self.bucket_name, self.object['prefix'])
        self.assertEqual(obj.etag, self.etag)
        self.assertEqual(obj.size, self.object['stat'].st_size)

        self.log.info('Get stat data of non-existing object, should fail')
        with self.assertRaises(NoSuchKey):
            self.minio.stat_object(self.bucket_name, self.utils.random_string())

    def test08_remove_object(self):
        """ MIN-015
        #. Create bucket (B1), should succeed.
        #. Create object (O1) in bucket (B1), should succeed.
        #. Remove object (O1), should succeed.
        #. List bucket (B1) objects, object (O1) should be gone.
        """
        self.log.info('Remove object (O1), should succeed')
        self.minio.remove_object(self.bucket_name, self.object['prefix'])

        self.log.info('List bucket (B1) objects, object (O1) should be gone')
        objects = self.minio.list_objects(self.bucket_name, recursive=True)
        self.assertNotIn(self.object['prefix'], [obj.object_name for obj in objects]) 

    def test09_remove_objects(self):
        """ MIN-016
        #. Create bucket (B1), should succeed.
        #. Create 3 object in bucket (B1).
        #. Delete all the 3 files. should succeed.
        #. List bucket (B1) objects, all the 3 objects should be gone.
        """

        self.log.info('Create 3 object files in bucket (B1)')
        objects_list = []
        for _ in range(3):
            obj = self.utils.create_object()
            self.CLEANUP['local_files'].append(obj['path'])      
            self.minio.fput_object(self.bucket_name, obj['prefix'], obj['path'])
            objects_list.append(obj['prefix'])

        self.log.info('Delete all the 3 files. should succeed')
        for error in self.minio.remove_objects(self.bucket_name, objects_list):
            self.assertFalse(error)
        
        self.log.info('List bucket (B1) objects, all the 3 objects should be gone')
        objects = self.minio.list_objects(self.bucket_name, recursive=True)
        self.assertEqual([obj.object_name for obj in objects], [self.object['prefix']]) 
        
    def test10_remove_incomplete_upload(self):
        """ MIN-017
        #. Create bucket (B1), should succeed.
        """
        pass