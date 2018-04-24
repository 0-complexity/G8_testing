#!/usr/bin/python3
from gevent import monkey
monkey.patch_all()
from optparse import OptionParser  # noqa: E402
import gevent  # noqa: E402
import signal  # noqa: E402
import time  # noqa: E402
import os  # noqa: E402
from gevent.lock import BoundedSemaphore  # noqa: E402
from js9 import j


def delete_vm(ovc, machine_id):
    with concurrency:
        print("Deleting machine {}".format(machine_id))
        ovc.api.cloudapi.machines.delete(machineId=machine_id)


def delete_cs(ovc, cloudspace_id):
    with concurrency:
        print("Deleting cloudspace {}".format(cloudspace_id))
        ovc.api.cloudapi.cloudspaces.delete(cloudspaceId=cloudspace_id)


def main(options):
    j.clients.itsyouonline.get(data={'application_id_': options.application_id, 'secret_': options.secret})
    ovc = j.clients.openvcloud.get(data = {'address': options.environment, 'account': options.username})
    

    while True:
        cloudspaces = ovc.api.cloudapi.cloudspaces.list()
        if not cloudspaces:
            break
        jobs = list()
        for cloudspace in cloudspaces:
            cloudspace_id = cloudspace['id']
            vms = ovc.api.cloudapi.machines.list(cloudspaceId=cloudspace_id)
            jobs.extend([gevent.spawn(delete_vm, ovc, vm['id']) for vm in vms if vm['name'] != 'template_vm'])
        gevent.joinall(jobs)
        jobs = list()
        for cloudspace in cloudspaces:
            cloudspace_id = cloudspace['id']
            vms = ovc.api.cloudapi.machines.list(cloudspaceId=cloudspace_id)
            jobs.extend([gevent.spawn(delete_vm, ovc, vm['id']) for vm in vms])
        gevent.joinall(jobs)
        jobs = list()
        for cloudspace in cloudspaces:
            cloudspace_id = cloudspace['id']
            vms = ovc.api.cloudapi.machines.list(cloudspaceId=cloudspace_id)
            if not vms:
                jobs.append(gevent.spawn(delete_cs, ovc, cloudspace_id))
        gevent.joinall(jobs)


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-u", "--user", dest="username", type="string",
                      help="username to login on the OVC api")
    parser.add_option("-p", "--pwd", dest="password", type="string",
                      help="password to login on the OVC api")
    parser.add_option("-e", "--env", dest="environment", type="string",
                      help="environment to login on the OVC api")
    parser.add_option("-n", "--con", dest="concurrency", default=2, type="int",
                      help="amount of concurrency to execute the job")
    parser.add_option("-appid", "--application_id", dest="application_id",
                        help="itsyouonline Application Id")
    parser.add_option("-secret", "--secret", dest="secret",
                        help="itsyouonline Secret")

    (options, args) = parser.parse_args()
    if not options.username or not options.password or not options.environment:
        parser.print_usage()
    else:
        concurrency = BoundedSemaphore(options.concurrency)
        gevent.signal(signal.SIGQUIT, gevent.kill)
        main(options)
