from zeroos.directory import Client
from testconfig import config


def get_jwt():
    response = CLIENT.oauth2_client_itsyouonline.get_access_token(client_id=CLIENT_ID,
                                                                  client_secret=CLIENT_SECRET,
                                                                  scopes=['user:memberof:%s' % ORGANIZATION,
                                                                          'user:name']
                                                                  )
    return response.content.decode('utf-8')

DIRECTORY_BASE_URL = config['main']['zero_directory_url']
CLIENT_ID = config['main']['client_id']
CLIENT_SECRET = config['main']['client_secret']
ORGANIZATION = config['main']['organization']
CLIENT = Client(DIRECTORY_BASE_URL)
JWT = get_jwt()
