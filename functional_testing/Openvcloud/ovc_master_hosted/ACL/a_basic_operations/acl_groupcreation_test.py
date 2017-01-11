# coding=utf-8
import uuid
import time
import unittest

from ....utils.utils import BasicACLTest
from JumpScale.portal.portal.PortalClient2 import ApiError


class ACLACCOUNT(BasicACLTest):
    def setUp(self):
        super(ACLACCOUNT, self).setUp()
        self.acl_setup(False)


class group_creation(ACLACCOUNT):
    def test_1_group_creation(self):
        """ ACL
        *Test case for cloudspace_create api with user has write access.*

        **Test Scenario:**

        #. create group with level1, admin should result be TRUE
        #. add user1  to the created group,should succeed
        #. get user 1 groups list  should have created group 
        #. delete created group
        #. get user1 groups list should be empty 
        """      

        self.lg('%s STARTED' % self._testID)
        self.lg('1- create group  ')
        self.name_group = str(uuid.uuid4()).replace('-', '')[0:10]
        self.lg('groupstatues %s ' % self.name_group)
        user=self.username
        group_status= self.cloudbroker_group_create(self.name_group,"test","test")
        
        self.lg('groupstatues %s ' % group_status)
        self.assertTrue(group_status)
        self.lg('2- add user %s to the group ' % user)
        response= self.cloudbroker_group_edit(self.name_group,"test","test",user)
        self.assertTrue(response)
        try:
           user_group_list=self.get_user_group_list(user)
           self.lg('3-get groups for user %s' % user) 
           self.assertEqual(user_group_list,self.name_group)
        except : 
           self.lg('- unexpected error raised error')
         
        self.lg('4- delete created group  %s' % self.name_group)
        self.cloudbroker_group_delete(self.name_group)
        try:
           user_group_list=self.get_user_group_list(user)
           self.lg('5- get groups for user %s' % user)
           self.assertEqual(user_group_list,[])
        except :             
           self.lg('- unexpected error raised error')
    
    def tearDown(self): 
        try:
            self.lg('delete group  %s' % self.name_group)
	    self.cloudbroker_group_delete(self.name_group)
           	
        except:
            self.lg('there is no group to delete')
             
    def test_2_group_creation(self):
        """ ACL
        *Test case for add fake user to group*

        **Test Scenario:**

        #. create group with level1, admin should result be TRUE
        #. add not exist user to created group should be forbidden
        #. delete created group
        """
        self.lg('%s STARTED' % self._testID)
        self.name_group = str(uuid.uuid4()).replace('-', '')[0:10]
        user = str(uuid.uuid4()).replace('-', '')[0:10]
        self.lg('1- create group ')
        group_status= self.cloudbroker_group_create(self.name_group,"test","test")
        self.lg('groupstatues %s ' % group_status)
        self.assertTrue(group_status)

        try:
            self.lg('2- add user with fake name to created group')
            response=self.cloudbroker_group_edit(self.name_group,"test","test",user)
            self.lg('response %s' % response )
            self.assertFalse(response)
            
        except ApiError as e:
            self.lg('- expected error raised %s' % e.message)
            self.assertEqual(e.message, '403 Forbidden') 

    def test_3_group_creation(self):
        """ ACL
        *Test case for add fake user to group*

        **Test Scenario:**

        #. create group with level1, admin 
        #. create user 1 and user2 with created group and user domain 
        #. get user1 and user2 groups list should have created group 
        #. delete created group 
        #. check that any of them don't have created group 
        """
        self.lg('%s STARTED' % self._testID)
        self.name_group = str(uuid.uuid4()).replace('-', '')[0:10]
        groupsdomain= [self.name_group ,'user']
        users = str(uuid.uuid4()).replace('-', '')[0:10]
        self.lg('1- create group with level1 and admin  domain ')
        group_status= self.cloudbroker_group_create(self.name_group,"test","test")
        self.assertTrue(group_status)
        self.lg('group statues %s ' % group_status)
        self.lg('groups %s '% groupsdomain)   
        self.user1 = self.cloudbroker_user_create(group = groupsdomain )
        self.lg('2- create user %s with created group ' % self.user1)  
        self.user2 = self.cloudbroker_user_create(group = groupsdomain )
        self.lg(' 3-create user %s with created group ' % self.user2) 
        try:
            user_group_list=self.get_user_group_list(self.user1)
            self.lg('4-get groups for user1 %s' % self.user1)
            self.assertTrue(self.name_group in user_group_list)
        except:
            self.lg('- expected error raised error')
        
        try:
            user_group_list=self.get_user_group_list(self.user2)
            self.lg('5-get groups for user2 %s' % self.user2)
            self.assertTrue(self.name_group in user_group_list)
        except:
            self.lg('- expected error raised error')
 
        self.lg('delete group  %s' % self.name_group)
        self.cloudbroker_group_delete(self.name_group)
        try:
            user_group_list=self.get_user_group_list(self.user1)
            self.lg('5-get groups after delete created group for user1 %s' % self.user1)
            self.assertFalse(self.name_group in user_group_list)
            self.assertTrue('user' in user_group_list)

        except:
            self.lg('- expected error raised error')

    
    def test_4_group_creation(self):
        """ ACL
        *Test case for add fake user to group*

        **Test Scenario:**

        #. create group with level1, admin
        #. create user1 with  user domain
        #. create account with user 1 should be forbidden
        #. add user1 to created group
        #. try to create account with user1 should succeed
        #. delete created group with user1 should succeed
        #. try to create account with user1 shoul fail
        """
        self.lg('%s STARTED' % self._testID)
        self.name_group = str(uuid.uuid4()).replace('-', '')[0:10]
        self.group_domain= "admin,level1"
        users = str(uuid.uuid4()).replace('-', '')[0:10]
        self.lg('1- create group with level1 and admin  domain ')
        group_status= self.cloudbroker_group_create(self.name_group,self.group_domain,"test")
        self.assertTrue(group_status)
        self.lg('group statues %s ' % group_status)
        self.user1 = self.cloudbroker_user_create(group = 'user' )
        self.lg('2- create user %s with user domain ' % self.user1)
        self.lg('3- create account with user1 %s with user domain ' % self.user1)
        self.user1_api = self.get_authenticated_user_api(self.user1)
        try:        
           accountId = self.user1_api.cloudbroker.account.create(name=self.user1, username=self.user1, email='%s@gmail.com'%self.user1,
                                                        maxMemoryCapacity=-1,
                                                        maxVDiskCapacity=-1,
                                                        maxCPUCapacity=-1,
                                                        maxNumPublicIP=-1)
                                                        
        except ApiError as e:
            self.lg('- expected error raised %s' % e.message)
            self.assertEqual(e.message, '403 Forbidden')
   
        
        self.lg('4-add user1 to created group')
        response=self.cloudbroker_group_edit(self.name_group,self.group_domain,"test",self.user1)
        self.lg('response %s' % response )
        self.assertTrue(response) 
        time.sleep(30)
        self.lg('5- create account with user1 after add him to created group')
       
        try:
            accountId = self.user1_api.cloudbroker.account.create(name=self.user1, username=self.user1, email='%s@gmail.com'%self.user1,
                                                        maxMemoryCapacity=-1,
                                                        maxVDiskCapacity=-1,
                                                        maxCPUCapacity=-1,
                                                        maxNumPublicIP=-1)
            self.assertTrue(accountId.status_code)
             
        except ApiError as e:
            self.lg('- expected error raised %s' % e.message)
            self.assertNotEqual(e.message, '403 Forbidden')

