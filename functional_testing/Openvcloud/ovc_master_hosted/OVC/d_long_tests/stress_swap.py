from ....utils.utils import BasicACLTest
import time


class StressSwap(BasicACLTest):
    def test01_stress_swap(self):
        """ OVC-000
        *Test case for stress swap*

        **Test Scenario:**

        #. connect to the node
        #. Install stress-ng
        #. Run command for 10 minutes
        #. Make sure that system raise the swap error
        """
        nodeId = self.get_random_running_nodeId()
        self.execute_command_on_physical_node('apt-get install -y stress-ng', nodeId)
        time.sleep(60)
        self.assertIn('stress-ng', self.execute_command_on_physical_node('which stress-ng', nodeId))

        self.execute_command_on_physical_node('stress-ng --vm-method rowhammer -r 500', nodeId)
        time.sleep(600)

        response_data = self.api.system.health.getDetailedStatus(nid=nodeId)
        for data in response_data['System Load']['data']:
            if 'Swap' in data['msg']:
                self.assertEqual("ERROR", data["status"])
                break
        else:
            self.fail(" [x] There is no Swap sensor!. ")
