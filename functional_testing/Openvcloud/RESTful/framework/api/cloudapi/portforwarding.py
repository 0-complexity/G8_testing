import random
from framework.api import api_client

class Portforwarding:
    def __init__(self):
        self._api = api_client

    def list(self, cloudspaceId, **kwargs):
        return self._api.cloudapi.portforwarding.list(cloudspaceId=cloudspaceId, **kwargs)

    def create(self, cloudspaceId, machineId, publicIp, **kwargs):
        publicPort = kwargs.get('publicPort', random.randint(1000, 30000))
        localPort = kwargs.get('localPort', random.randint(1000, 30000))
        protocol = kwargs.get('protocol', random.choice(['udp', 'tcp']))
        return self._api.cloudapi.portforwarding.create(
            cloudspaceId=cloudspaceId,
            machineId=machineId,
            publicIp=publicIp,
            publicPort=publicPort,
            localPort=localPort,
            protocol=protocol
        )

    def delete(self, cloudspaceId, id):
        return self._api.cloudapi.portforwarding.delete(cloudspaceId=cloudspaceId, id=id)

    def deleteByPort(self, cloudspaceId, publicIp, publicPort, protocol):
        return self._api.cloudapi.portforwarding.deleteByPort(
            cloudspaceId=cloudspaceId,
            publicIp=publicIp,
            publicPort=publicPort,
            protocol=protocol
        )

    def update(self, cloudspaceId, machineId, id, publicIp, **kwargs):
        publicPort = kwargs.get('publicPort', random.randint(1000, 30000))
        localPort = kwargs.get('localPort', random.randint(1000, 30000))
        protocol = kwargs.get('protocol', random.choice(['udp', 'tcp']))
        return self._api.cloudapi.portforwarding.update(
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
        return self._api.cloudapi.portforwarding.update(
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