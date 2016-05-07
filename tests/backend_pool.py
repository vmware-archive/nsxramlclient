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


def create_backend_pool(session, edge_id='edge-1'):
    backend_pool_spec = session.extract_resource_body_example('pools', 'create')

    backend_pool_spec['pool']['name'] = 'pool-tcp-snat-2'
    backend_pool_spec['pool']['description'] = 'pool-tcp-snat-2'
    backend_pool_spec['pool']['transparent'] = 'false'
    backend_pool_spec['pool']['algorithm'] = 'round-robin'
    backend_pool_spec['pool']['monitorId'] = 'monitor-5'
    backend_pool_spec['pool']['member']['ipAddress'] = '192.168.101.201'
    backend_pool_spec['pool']['member']['weight'] = '1'
    backend_pool_spec['pool']['member']['port'] = '80'
    backend_pool_spec['pool']['member']['minConn'] = '10'
    backend_pool_spec['pool']['member']['maxConn'] = '100'
    backend_pool_spec['pool']['member']['name'] = 'm5'
    backend_pool_spec['pool']['member']['monitorPort'] = '80'

    create_response = session.create('pools', uri_parameters={'edgeId': edge_id},
                                     request_body_dict=backend_pool_spec)

    session.view_response(create_response)

    return create_response['objectId']


def backend_pool_by_id(session, object_id, edge_id='edge-1'):
    response = session.read('pool', uri_parameters={'edgeId': edge_id, 'poolID': object_id})
    session.view_response(response)


def backend_pool(session, edge_id='edge-1'):
    response = session.read('pools', uri_parameters={'edgeId': edge_id})
    session.view_response(response)


def update_backend_pool(session, object_id, edge_id='edge-1'):
    backend_pool_spec = session.extract_resource_body_example('pool', 'update')

    backend_pool_spec['pool']['name'] = 'pool-tcp-snat-2'
    backend_pool_spec['pool']['description'] = 'pool-tcp-snat-2-modified'
    backend_pool_spec['pool']['transparent'] = 'false'
    backend_pool_spec['pool']['algorithm'] = 'round-robin'
    backend_pool_spec['pool']['monitorId'] = 'monitor-5'
    backend_pool_spec['pool']['member']['ipAddress'] = '192.168.101.202'
    backend_pool_spec['pool']['member']['weight'] = '1'
    backend_pool_spec['pool']['member']['port'] = '80'
    backend_pool_spec['pool']['member']['minConn'] = '10'
    backend_pool_spec['pool']['member']['maxConn'] = '100'
    backend_pool_spec['pool']['member']['name'] = 'm5'
    backend_pool_spec['pool']['member']['monitorPort'] = '80'

    response = session.update('pool', uri_parameters={'edgeId': edge_id, 'poolID': object_id},
                              request_body_dict=backend_pool_spec)

    session.view_response(response)


def delete_backend_pool_by_id(session, object_id, edge_id='edge-1'):
    response = session.delete('pool', uri_parameters={'edgeId': edge_id, 'poolID': object_id})

    session.view_response(response)


def delete_backend_pool(session, edge_id='edge-1'):
    response = session.delete('pools', uri_parameters={'edgeId': edge_id})

    session.view_response(response)


def main():
    session = NsxClient(nsxraml_file, nsxmanager, nsx_username, nsx_password, debug=True)

    object_id = create_backend_pool(session)

    backend_pool_by_id(session, object_id)

    backend_pool(session)

    update_backend_pool(session, object_id)

    delete_backend_pool_by_id(session, object_id)

    delete_backend_pool(session)


if __name__ == "__main__":
    main()

