#!/usr/bin/python3
import requests, os, json
import uuid, random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(dest="env", help="environment url")
parser.add_argument(dest="env_location", help="the environment location")
parser.add_argument(dest="port", help="environment port")
parser.add_argument(dest="client_id", help="client id of itsyouonline user")
parser.add_argument(dest="client_secret", help="secert id of itsyouonline user")
parser.add_argument(dest="username", help="itsyouonline user name")
args = parser.parse_args()

class BaseResource(object):
    def __init__(self, session, url):
        self._url = url
        self._method = 'POST'
        self._session = session

    def __getattr__(self, item):
        url = os.path.join(self._url, item)
        resource = BaseResource(self._session, url)
        setattr(self, item, resource)
        return resource

    def __call__(self, **kwargs):
        response = self._session.request(self._method, self._url, kwargs)
        return response


class Client(BaseResource):
    def __init__(self):
        # Generate the jwt
        session = requests.Session()

        jwt = self._generate_jwt(args.client_id, args.client_secret)
        session.headers['Authorization'] = 'Bearer {}'.format(jwt)

        # Generate the url
        url = "https://{}:{}/restmachine".format(args.env, args.port)

        super(Client, self).__init__(session, url)

    def _generate_jwt(self, client_id, client_secret):
        params = {
            'grant_type': 'client_credentials',
            'response_type': 'id_token',
            'client_id': client_id,
            'client_secret': client_secret
        }
        response = requests.post('https://itsyou.online/v1/oauth/access_token', params=params)
        response.raise_for_status()
        return response.content.decode('utf-8')


class ovc_methods(Client):
    def __init__(self):
        self.api_client = Client()
    
    def create_vm(self, cloudspaceId=None, **kwargs):
        if not cloudspaceId:
            data, response = self.create_cloudspace()
            cloudspaceId = response.json()
        data = {
                'cloudspaceId': cloudspaceId,
                'name': self.random_string(),
                'description': self.random_string(),
                'datadisks': [],
                'userdata': ''
                 }
        response = self.api_client.cloudapi.images.list()
        response.raise_for_status()

        image = random.choice([x for x in response.json() if x["type"].startswith(('Window', 'Linux'))])
        data['imageId'] = image['id']
        response.raise_for_status()

        response = self.api_client.cloudapi.sizes.list(cloudspaceId=cloudspaceId)
        response.raise_for_status()
        sizes = response.json()
        basic_sizes = [512, 1024, 4096, 8192, 16384, 2048]
        for _ in range(len(sizes)):
            size = random.choice(sizes)
            if size["memory"] in basic_sizes:
                break                
        data['disksize'] = random.choice(size['disks'])
        data['sizeId'] = size['id']

        data.update(** kwargs)

        return data, self.api_client.cloudbroker.machine.create(**data)

    def create_cloudspace(self, accountId=None, access='ARCXDU', **kwargs ):
        if not accountId:
            data, response = self.create_account()
            accountId = response.json()
        location = self.get_environment()['locationCode']
        data = {
                'accountId': accountId,
                'location': location,
                'access': access,
                'name': self.random_string(),
                'maxMemoryCapacity': -1,
                'maxVDiskCapacity': -1,
                'maxCPUCapacity': -1,
                'maxNetworkPeerTransfer': -1,
                'maxNumPublicIP': -1,
                'allowedVMSizes': [],
                'privatenetwork': ''
             }
        data.update(** kwargs)
        return data, self.api_client.cloudapi.cloudspaces.create(** data)

    def create_account(self, access='ARCXDU', **kwargs):
        data = {
            'name': self.random_string(),
            'username': args.username,
            'access': access,
            'maxMemoryCapacity': -1,
            'maxVDiskCapacity': -1,
            'maxCPUCapacity': -1,
            'maxNetworkPeerTransfer': -1,
            'maxNumPublicIP': -1,
               }
        data.update(** kwargs)
        return data, self.api_client.cloudbroker.account.create(** data)

    def get_environment(self):
        locations = (self.api_client.cloudapi.locations.list()).json()
        for location in locations:
            if args.env_location == location['locationCode']:
                return location
        else:
            raise Exception("can't find the %s environment location in grid" % args.env_location)

    def random_string(self, length=10):
        return str(uuid.uuid4()).replace('-', '')[0:length]

x=ovc_methods()
print(x.create_vm())