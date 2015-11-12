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


def create_monitor(session, edge_id='edge-1'):
    monitor_spec = session.extract_resource_body_schema('lbMonitors', 'create')

    monitor_spec['monitor']['type'] = 'http'
    monitor_spec['monitor']['interval'] = '5'
    monitor_spec['monitor']['timeout'] = '15'
    monitor_spec['monitor']['maxRetries'] = '3'
    monitor_spec['monitor']['method'] = 'GET'
    monitor_spec['monitor']['url'] = '/'
    monitor_spec['monitor']['name'] = 'http-monitor-2'

    create_response = session.create('lbMonitors', uri_parameters={'edgeId': edge_id},
                                     request_body_dict=monitor_spec)

    session.view_response(create_response)

    return create_response['objectId']


def get_monitor_by_id(session, object_id, edge_id='edge-1'):
    response = session.read('lbMonitor', uri_parameters={'edgeId': edge_id, 'monitorID': object_id})
    session.view_response(response)


def get_monitors(session, edge_id='edge-1'):
    response = session.read('lbMonitors', uri_parameters={'edgeId': edge_id})
    session.view_response(response)


def update_monitor(session, object_id, edge_id='edge-1'):
    monitor_spec = session.extract_resource_body_schema('lbMonitor', 'update')

    monitor_spec['monitor']['type'] = 'http'
    monitor_spec['monitor']['interval'] = '5'
    monitor_spec['monitor']['timeout'] = '10'
    monitor_spec['monitor']['maxRetries'] = '4'
    monitor_spec['monitor']['method'] = 'GET'
    monitor_spec['monitor']['url'] = '/'
    monitor_spec['monitor']['name'] = 'http-monitor-2'

    response = session.update('lbMonitor', uri_parameters={'edgeId': edge_id, 'monitorID': object_id},
                              request_body_dict=monitor_spec)

    session.view_response(response)


def delete_monitor_by_id(session, object_id, edge_id='edge-1'):
    response = session.delete('lbMonitor', uri_parameters={'edgeId': edge_id, 'monitorID': object_id})

    session.view_response(response)


def delete_monitors(session, edge_id='edge-1'):
    response = session.delete('lbMonitors', uri_parameters={'edgeId': edge_id})

    session.view_response(response)


def main():
    session = NsxClient(nsxraml_file, nsxmanager, nsx_username, nsx_password, debug=True)

    object_id = create_monitor(session)

    get_monitor_by_id(session, object_id)

    get_monitors(session)

    update_monitor(session, object_id)

    delete_monitor_by_id(session, object_id)

    delete_monitors(session)


if __name__ == "__main__":
    main()

