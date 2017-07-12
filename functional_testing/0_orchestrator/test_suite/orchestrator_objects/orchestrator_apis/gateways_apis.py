from test_suite.orchestrator_objects.orchestrator_apis import *


class GatewayAPI:
    def __init__(self, orchestrator_client):
        self.orchestrator_client = orchestrator_client
        self.createdGw = []

    @catch_exception_decoration
    def list_nodes_gateways(self, nodeid):
        return self.orchestrator_client.nodes.ListGateways(nodeid=nodeid)

    @catch_exception_decoration
    def get_nodes_gateway(self, nodeid, gwname):
        return self.orchestrator_client.nodes.GetGateway(nodeid=nodeid, gwname=gwname)

    @catch_exception_decoration
    def post_nodes_gateway(self, nodeid, data):
        response = self.orchestrator_client.nodes.CreateGW(nodeid=nodeid, data=data)
        if response.status_code == 201:
            self.createdGw.append({"node": nodeid, "name": data["name"]})
        return response

    @catch_exception_decoration
    def update_nodes_gateway(self, nodeid, gwname, data):
        return self.orchestrator_client.nodes.UpdateGateway(nodeid=nodeid, gwname=gwname, data=data)

    @catch_exception_decoration
    def delete_nodes_gateway(self, nodeid, gwname):
        response = self.orchestrator_client.nodes.DeleteGateway(nodeid=nodeid, gwname=gwname)
        if response.status_code == 204:
            self.createdGw.remove({"node": nodeid, "name": gwname})
        return response

    @catch_exception_decoration
    def list_nodes_gateway_forwards(self, nodeid, gwname):
        return self.orchestrator_client.nodes.GetGWForwards(nodeid=nodeid, gwname=gwname)

    @catch_exception_decoration
    def post_nodes_gateway_forwards(self, nodeid, gwname, data):
        return self.orchestrator_client.nodes.CreateGWForwards(nodeid=nodeid, gwname=gwname, data=data)

    @catch_exception_decoration
    def delete_nodes_gateway_forward(self, nodeid, gwname, forwardid):
        return self.orchestrator_client.nodes.DeleteGWForward(nodeid=nodeid, gwname=gwname, forwardid=forwardid)

    @catch_exception_decoration
    def list_nodes_gateway_dhcp_hosts(self, nodeid, gwname, interface):
        return self.orchestrator_client.nodes.ListGWDHCPHosts(nodeid=nodeid, gwname=gwname, interface=interface)

    @catch_exception_decoration
    def post_nodes_gateway_dhcp_host(self, nodeid, gwname, interface, data):
        return self.orchestrator_client.nodes.AddGWDHCPHost(nodeid=nodeid, gwname=gwname, interface=interface,
                                                            data=data)

    @catch_exception_decoration
    def delete_nodes_gateway_dhcp_host(self, nodeid, gwname, interface, macaddress):
        return self.orchestrator_client.nodes.DeleteDHCPHost(nodeid=nodeid, gwname=gwname, interface=interface,
                                                             macaddress=macaddress)

    @catch_exception_decoration
    def get_nodes_gateway_advanced_http(self, nodeid, gwname):
        return self.orchestrator_client.nodes.GetGWHTTPConfig(nodeid=nodeid, gwname=gwname)

    @catch_exception_decoration
    def post_nodes_gateway_advanced_http(self, nodeid, gwname, data):
        return self.orchestrator_client.nodes.SetGWHTTPConfig(nodeid=nodeid, gwname=gwname, data=data)

    @catch_exception_decoration
    def get_nodes_gateway_advanced_firewall(self, nodeid, gwname):
        return self.orchestrator_client.nodes.GetGWFWConfig(nodeid=nodeid, gwname=gwname)

    @catch_exception_decoration
    def post_nodes_gateway_advanced_firewall(self, nodeid, gwname, data):
        return self.orchestrator_client.nodes.SetGWFWConfig(nodeid=nodeid, gwname=gwname, data=data)

    @catch_exception_decoration
    def post_nodes_gateway_start(self, nodeid, gwname):
        return self.orchestrator_client.nodes.StartGateway(nodeid=nodeid, gwname=gwname, data={})

    @catch_exception_decoration
    def post_nodes_gateway_stop(self, nodeid, gwname):
        return self.orchestrator_client.nodes.StopGateway(nodeid=nodeid, gwname=gwname, data={})

    @catch_exception_decoration
    def list_nodes_gateway_httpproxies(self, nodeid, gwname):
        return self.orchestrator_client.nodes.ListHTTPProxies(nodeid=nodeid, gwname=gwname)

    @catch_exception_decoration
    def get_nodes_gateway_httpproxy(self, nodeid, gwname, proxyid):
        return self.orchestrator_client.nodes.GetHTTPProxy(nodeid=nodeid, gwname=gwname, proxyid=proxyid)

    @catch_exception_decoration
    def get_nodes_gateway_httpproxy(self, nodeid, gwname, proxyid):
        return self.orchestrator_client.nodes.GetHTTPProxy(nodeid=nodeid, gwname=gwname, proxyid=proxyid)

    @catch_exception_decoration
    def post_nodes_gateway_httpproxy(self, nodeid, gwname, data):
        return self.orchestrator_client.nodes.CreateHTTPProxies(nodeid=nodeid, gwname=gwname, data=data)

    @catch_exception_decoration
    def delete_nodes_gateway_httpproxy(self, nodeid, gwname, proxyid):
        return self.orchestrator_client.nodes.DeleteHTTPProxies(nodeid=nodeid, gwname=gwname, proxyid=proxyid)