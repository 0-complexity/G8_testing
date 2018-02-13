import random
from framework.api import api_client

class Portforwarding:
    def __init__(self):
        self._api = api_client.cloudapi.portforwarding

    def list(self, cloudspaceId, **kwargs):
        return self._api.list(cloudspaceId=cloudspaceId, **kwargs)

    def create(self, cloudspaceId, machineId, publicIp, **kwargs):
        publicPort = kwargs.get('publicPort', random.randint(1000, 30000))
        localPort = kwargs.get('localPort', random.randint(1000, 30000))
        protocol = kwargs.get('protocol', random.choice(['udp', 'tcp']))
        return self._api.create(
            cloudspaceId=cloudspaceId,
            machineId=machineId,
            publicIp=publicIp,
            publicPort=publicPort,
            localPort=localPort,
            protocol=protocol
        )

    def delete(self, cloudspaceId, id):
        return self._api.delete(cloudspaceId=cloudspaceId, id=id)

    def deleteByPort(self, cloudspaceId, publicIp, publicPort, protocol):
        return self._api.deleteByPort(
            cloudspaceId=cloudspaceId,
            publicIp=publicIp,
            publicPort=publicPort,
            protocol=protocol
        )

    def update(self, cloudspaceId, machineId, id, publicIp, **kwargs):
        publicPort = kwargs.get('publicPort', random.randint(1000, 30000))
        localPort = kwargs.get('localPort', random.randint(1000, 30000))
        protocol = kwargs.get('protocol', random.choice(['udp', 'tcp']))
        return self._api.update(
            cloudspaceId=cloudspaceId,
            machineId=machineId,
            id=id,
            publicIp=publicIp,
            publicPort=publicPort,
            localPort=localPort,
            protocol=protocol
        )

    def updateByPort(self, cloudspaceId, machineId, sourcePublicIp, sourcePublicPort, sourceProtocol, publicIp, **kwargs):
        publicPort = kwargs.get('publicPort', random.randint(1000, 30000))
        localPort = kwargs.get('localPort', random.randint(1000, 30000))
        protocol = kwargs.get('protocol', random.choice(['udp', 'tcp']))
        return self._api.update(
            cloudspaceId=cloudspaceId,
            machineId=machineId,
            sourcePublicIp=sourcePublicIp,
            sourcePublicPort=sourcePublicPort,
            sourceProtocol=sourceProtocol,
            publicIp=publicIp,
            publicPort=publicPort,
            localPort=localPort,
            protocol=protocol
        )