# coding=utf-8
from ..utils.utils import BaseTest



class EnvironmentLimitTest(BaseTest):
    def test001_environment_cloudspaces_limit(self):
        """ JS-001
        *Test case for environment cloudspaces limit.*

        **Test Scenario:**

        #. start create cloudspace counter
        #. continue creating cloudspacesand count them until failed
        #. push the maximum number of created cloudspaces as the cloudspace limit
        """
        self.lg('%s STARTED' % self._testID)

        self.lg('1- start create cloudspace counter')


        self.lg('%s ENDED' % self._testID)