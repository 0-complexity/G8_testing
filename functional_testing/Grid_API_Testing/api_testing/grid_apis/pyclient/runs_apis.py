from api_testing.grid_apis.grid_pyclient_base import GridPyclientBase
from requests import HTTPError

class RunsAPI(GridPyclientBase):
    def __init__(self):
        super().__init__()

    def wait_on_run(self, runid):
        try:
            response = self.api_client.WaitOnRun(runid=runid)
        except HTTPError as e:
            response = e.response
        finally:
            return response

    def get_run_status(self, runid):
        try:
            response = self.api_client.GetRunState(runid=runid)
        except HTTPError as e:
            response = e.response
        finally:
            return response