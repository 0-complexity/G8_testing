from framework.api import api_client, utils
from framework.api.cloudbroker.accounts import Accounts
from framework.api.cloudbroker.cloudspaces import Cloudspaces
from framework.api.cloudbroker.diagnostics import Diagnostics
from framework.api.cloudbroker.health import Health
from framework.api.cloudbroker.iaas import Iaas
from framework.api.cloudbroker.image import Image
from framework.api.cloudbroker.machine import Machine
from framework.api.cloudbroker.ovsnode import OVSNode
from framework.api.cloudbroker.qos import Qos
from framework.api.cloudbroker.user import User

class Cloudbroker:
    def __init__(self):
        self.accounts = Accounts()
        self.cloudspaces = Cloudspaces()
        self.diagnostics = Diagnostics()
        self.health = Health()
        self.iaas = Iaas()
        self.image = Image()
        self.machine = Machine()
        self.ovsnode = OVSNode()
        self.qos = Qos()
        self.user = User()
