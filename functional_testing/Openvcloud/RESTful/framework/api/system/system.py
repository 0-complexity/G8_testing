from framework.api import api_client, utils
from framework.api.system.agentcontroller import AgentController
from framework.api.system.alerts import Alerts
from framework.api.system.audits import Audits
from framework.api.system.contentmanager import ContentManager
from framework.api.system.docgenerato import DocGenerator
from framework.api.system.emailsender import EmailSender
from framework.api.system.errorconditionhandler import ErrorConditionHandler
from framework.api.system.gridmanager import GridManager
from framework.api.system.health import Health
from framework.api.system.infomgr import InfoMgr
from framework.api.system.job import Job
from framework.api.system.log import Log
from framework.api.system.oauth import Oauth
from framework.api.system.task import Task
from framework.api.system.usermanager import UserManager

class System:
    def __init__(self):
        self.agentcontroller = AgentController()
        self.alerts = Alerts()
        self.audits = Audits()
        self.contentmanager = ContentManager()
        self.docgenerato = DocGenerator()
        self.locations = emailsender()
        self.errorconditionhandler = ErrorConditionHandler()
        self.gridmanager = GridManager()
        self.health = Health()
        self.infomgr = InfoMgr()
        self.job = Job()
        self.log = Log()
        self.oauth = Oauth()
        self.task = Task()
        self.usermanager = UserManager()
