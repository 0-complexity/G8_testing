from zeroos.orchestrator import client as apiclient
from zeroos.orchestrator.client import oauth2_client_itsyouonline
from testconfig import config

class GridPyclientBase(object):
    def __init__(self):
        self.config = config['main']
        self.api_base_url = self.config['api_base_url']

        # Get JWT
        client_id = self.config['client_id']
        client_secret = self.config['client_secret']
        user_of_organization = self.config['user_of_organization']
        cls = oauth2_client_itsyouonline.Oauth2ClientItsyouonline()
        response = cls.get_access_token(client_id, client_secret, scopes=['user:memberof:%s' % user_of_organization], audiences=[])
        JWT = response.token

        # Create client object
        self.api_client = apiclient.APIClient(self.api_base_url)
        self.api_client.set_auth_header("Bearer %s" % JWT)
