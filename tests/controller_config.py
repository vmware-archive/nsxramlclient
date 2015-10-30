#!/usr/bin/env python

# coding=utf-8
#
# Copyright 2015 VMware, Inc. All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
# to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions
# of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

# TODO Add code to save the techsupport log to a file
# TODO Add code to test and save the snapshot log to a file


__author__ = 'shrirang'

from tests.config import *
from nsxramlclient.client import NsxClient
import time


def cluster_information(session):
    response = session.read('nsxControllerCluster')
    session.view_response(response)


def cluster_update(session, opt = 'true'):
    config_spec = session.extract_resource_body_schema('nsxControllerCluster', 'update')
    config_spec['controllerConfig']['sslEnabled'] = opt
    update_response = session.update('nsxControllerCluster', request_body_dict=config_spec)
    session.view_response(update_response)


def query_syslog(session, controller_id):
    response = session.read('nsxControllerSyslog', uri_parameters={'controllerId': controller_id})
    session.view_response(response)
    return response


def del_syslog(session, controller_id):
    response = session.delete('nsxControllerSyslog', uri_parameters={'controllerId': controller_id})


def create_syslog(session, controller_id, controller):
    create_response = session.create('nsxControllerSyslog', uri_parameters={'controllerId': controller_id},  request_body_dict =  controller['body'])

    session.view_response(create_response)


def main():
    excep = False

    controller = dict()

    session = NsxClient(nsxraml_file, nsxmanager, nsx_username, nsx_password, debug=True)

    cluster_information(session)

    cluster_update(session, 'true')

    # Check if syslog config already present
    try:
        controller = query_syslog(session, 'controller-1')
    except:
        excep = True
        controller = {'status': 200, 'body': {'controllerSyslogServer': {'syslogServer': '10.135.14.236', 'protocol': 'UDP', 'port': '514', 'level': 'INFO'}}, 'Etag': None, 'location': None, 'objectId': None}
    
    if excep:
        # If syslog does not present test create/list/delete
        create_syslog(session, 'controller-1', controller)
        query_syslog(session, 'controller-1')
        del_syslog(session, 'controller-1')
    else:
        # Else delete and recreate same config
        del_syslog(session, 'controller-1')
        create_syslog(session, 'controller-1', controller)


if __name__ == "__main__":
    main()

