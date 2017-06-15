from zeroos.orchestrator import client as apiclient
from testconfig import config

class GridPyclientBase(object):
    def __init__(self):
        self.config = config['main']
        self.api_base_url = self.config['api_base_url']

        # Get JWT
        client_id = config['client_id']
        client_secret = config['client_secret']
        user_of_organization = config['user_of_organization']
        cls = apiclient.oauth2_client_itsyouonline.Oauth2ClientItsyouonline()
        response = cls.get_access_token(client_id, client_secret, scope=['organization:memberOf:%s' % user_of_organization],
                                        audience=[])
        JWT = response.token

        # Create client object
        self.api_client = apiclient.APIClient(self.api_base_url)
        self.api_client.set_auth_header("Bearer %s" % JWT)
