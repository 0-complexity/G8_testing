from testconfig import config
from framework.client.client import Client

ip = config['main']['ip']
port = int(config['main']['port'])
client_id = config['main']['client_id']
client_secret = config['main']['client_secret']
api = Client(ip, port, client_id, client_secret)
api.load_swagger()