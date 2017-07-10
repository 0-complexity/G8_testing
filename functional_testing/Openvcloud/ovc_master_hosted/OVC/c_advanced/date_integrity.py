import random

from ....utils.utils import BasicACLTest

from JumpScale.portal.portal.PortalClient2 import ApiError
from JumpScale.baselib.http_client.HttpClient import HTTPError

class AdvancedTests(BasicACLTest):

    def setUp(self):
        super(AdvancedTests, self).setUp()
        self.default_setup()
        """
        self.create_default_cloudspace= create_default_cloudspace
        self.location = self.get_location()['locationCode']
        self.account_owner = self.username
        self.lg('- create account for :%s' % self.account_owner)
        self.account_id = self.cloudbroker_account_create(self.account_owner, self.account_owner,
                                                          self.email)

        self.account_owner_api = self.get_authenticated_user_api(self.account_owner)

	if self.create_default_cloudspace:
		self.lg('- create default cloudspace for :%s' % self.account_owner)
		self.cloudspace_id = self.cloudapi_cloudspace_create(account_id=self.account_id,
                                                             location=self.location,
                                                             access=self.account_owner,
                                                             api=self.account_owner_api,
                                                             name='default')
        """

    def test001_Network_configuration(self):
        """ OVC-020
        *Test case for validate deleted cloudspace with running machines get destroyed.*

        **Test Scenario:**

        #. Create 3+ vm's possible with different images on new cloudspace, should succeed

        """
        ## Notes
        ## um using python2 not 3 as in new fio

        self.lg('%s STARTED' % self._testID)

        cloudspace_id = self.cloudapi_cloudspace_create(self.account_id,
                                                        self.location,
                                                        self.account_owner)

        cloudspace_publicport = 1000
        # cloudspace = self.api.cloudapi.cloudspaces.get(cloudspaceId=cloudspace_id)
        storagenodes = self.api.system.gridmanager.getNodes(roles='storagenode')
        storagenodes_ids = [6, 7]

        for sn_id in storagenodes_ids:
            machine_id = self.cloudapi_create_machine(cloudspace_id=cloudspace_id,
                                                      size_id=size['id'],
                                                      image_id=image['id'],
                                                      disksize=disksize, stackid=sn_id)


        # Get cloupdspace ip
        self.lg("")

        self.lg('%s ENDED' % self._testID)
