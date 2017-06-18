from api_testing.grid_apis.grid_pyclient_base import GridPyclientBase
from requests import HTTPError

class RunsAPI(GridPyclientBase):
    def __init__(self):
        super().__init__()

    def wait_on_run(self, runid):
        uri = self.api_base_url + '/runs/{}/wait'.format(runid)
        try:
            response = self.api_client.get(uri=uri, headers=None, params=None, content_type=None)
        except HTTPError as e:
            response = e.response
        finally:
            return response

    def get_run_status(self, runid):
        uri = self.api_base_url + '/runs/{}'.format(runid)
        try:
            response = self.api_client.get(uri=uri, headers=None, params=None, content_type=None)
        except HTTPError as e:
            response = e.response
        finally:
            return response