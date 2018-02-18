from framework.api.cloudapi.accounts import Accounts
from framework.api.cloudapi.cloudspaces import Cloudspaces
from framework.api.cloudapi.disks import Disks
from framework.api.cloudapi.externalnetwork import ExternalNetwork
from framework.api.cloudapi.images import Images
from framework.api.cloudapi.locations import Locations
from framework.api.cloudapi.machines import Machines
from framework.api.cloudapi.portforwarding import Portforwarding
from framework.api.cloudapi.sizes import Sizes
from framework.api.cloudapi.users import Users

class Cloudapi:
    def __init__(self):
        self.accounts = Accounts()
        self.cloudspaces = Cloudspaces()
        self.disks = Disks()
        self.externalnetwork = ExternalNetwork()
        self.images = Images()
        self.locations = Locations()
        self.machines = Machines()
        self.portforwarding = Portforwarding()
        self.sizes = Sizes()
        self.users = Users()
