#!/usr/bin/env python
# coding=utf-8
#
# Copyright © 2015 VMware, Inc. All Rights Reserved.
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

from tests.config import *
from nsxramlclient.client import NsxClient


__author__ = 'shrirang'


def create_virtualserver(session, edge_id='edge-1', app_profile='applicationProfile-4', pool_id = 'pool-5'):
    virtualserver_spec = session.extract_resource_body_schema('virtualServers', 'create')

    virtualserver_spec['virtualServer']['name'] = 'http_vip_2'
    virtualserver_spec['virtualServer']['description'] = 'http virtualServer 2'
    virtualserver_spec['virtualServer']['enabled'] = 'true'
    virtualserver_spec['virtualServer']['ipAddress'] = '10.117.35.172'
    virtualserver_spec['virtualServer']['protocol'] = 'http'
    virtualserver_spec['virtualServer']['port'] = '443'
    virtualserver_spec['virtualServer']['connectionLimit'] = '123'
    virtualserver_spec['virtualServer']['connectionRateLimit'] = '123'
    virtualserver_spec['virtualServer']['applicationProfileId'] = app_profile
    virtualserver_spec['virtualServer']['defaultPoolId'] = pool_id
    virtualserver_spec['virtualServer']['enableServiceInsertion'] = 'false'
    virtualserver_spec['virtualServer']['accelerationEnabled'] = 'true'

    create_response = session.create('virtualServers', uri_parameters={'edgeId': edge_id},
                                     request_body_dict=virtualserver_spec)

    session.view_response(create_response)

    return create_response['objectId']


def get_virtualserver_by_id(session, object_id, edge_id='edge-1'):
    response = session.read('virtualServer', uri_parameters={'edgeId': edge_id, 'virtualserverID': object_id})
    session.view_response(response)


def get_virtualservers(session, edge_id='edge-1'):
    response = session.read('virtualServers', uri_parameters={'edgeId': edge_id})
    session.view_response(response)


def delete_virtualserver_by_id(session, object_id, edge_id='edge-1'):
    response = session.delete('virtualServer', uri_parameters={'edgeId': edge_id, 'virtualserverID': object_id})

    session.view_response(response)


def delete_virtualservers(session, edge_id='edge-1'):
    response = session.delete('virtualServers', uri_parameters={'edgeId': edge_id})

    session.view_response(response)


def main():
    session = NsxClient(nsxraml_file, nsxmanager, nsx_username, nsx_password, debug=True)

    object_id = create_virtualserver(session)

    get_virtualserver_by_id(session, object_id)

    get_virtualservers(session)

    delete_virtualserver_by_id(session, object_id)

    delete_virtualservers(session)


if __name__ == "__main__":
    main()

