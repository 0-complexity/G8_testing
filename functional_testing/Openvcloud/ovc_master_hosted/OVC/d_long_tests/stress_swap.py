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
        self.execute_command_on_physical_node(command='apt-get install -y stress-ng', nodeid=nodeId)
        time.sleep(60)
        self.execute_command_on_physical_node(command='stress-ng --vm-method rowhammer -r 500', nodeid=nodeId)
        time.sleep(600)

        response_data = self.api.system.health.getDetailedStatus(nid=nodeId)
        for data in response_data['System Load']['data']:
            if 'Swap' in data['msg']:
                self.assertEqual("ERROR", data["status"])
                break
        else:
            self.fail(" [x] There is no Swap sensor!. ")
