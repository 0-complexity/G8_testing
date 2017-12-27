from ....utils.utils import BasicACLTest
import time


class StressSwap(BasicACLTest):
    def test01_stress_swap(self):
        """ OVC-000
        *Test case for stress swap*

        **Test Scenario:**

        #. connect to the node
        #. Install stress-ng
        #. Run "stress-ng --vm-method rowhammer -r 500"
        #. Wait for 10 minutes
        #. Get health detailed status and check the swap value
        #. Make sure that system raise the swap error
        """
        self.nodeId = self.get_nodeId_to_move_VFW_to()
        print(" [*] self.nodeId : %s " % str(self.nodeId))

        print(" [*] Install stress-ng")
        self.execute_command_on_physical_node('apt-get install -y stress-ng', self.nodeId)
        time.sleep(60)
        self.assertIn('stress-ng', self.execute_command_on_physical_node('which stress-ng', self.nodeId))

        print(" [*] Execute stress-ng --vm-method rowhammer -r 500")
        self.execute_command_on_physical_node('stress-ng --vm-method rowhammer -r 500&', self.nodeId)
        print(" [*] Wait for 10 minutes")
        time.sleep(600)

        response_data = self.api.system.health.getDetailedStatus(nid=self.nodeId)
        print(" [*] Get health details status")
        for data in response_data['System Load']['data']:
            if 'Swap' in data['msg']:
                self.assertEqual("ERROR", data["status"])
                break
        else:
            self.fail(" [x] There is no Swap sensor!. ")

    def tearDown(self):
        try:
            self.execute_command_on_physical_node('pkill -9 stress-ng', self.nodeId)
        except:
            # " There is no thing to do, cause this test case may damage the node"
            pass
        super(StressSwap, self).tearDown()
