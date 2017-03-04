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


def create_interface(session, edge_id='edge-2'):
    interface_spec = session.extract_resource_body_schema('interfaces', 'create')

    interface_spec['interfaces']['interface']['name'] = 'interface1'
    interface_spec['interfaces']['interface']['addressGroups']['addressGroup']['primaryAddress'] = '192.168.10.1'
    interface_spec['interfaces']['interface']['addressGroups']['addressGroup']['subnetMask'] = '255.255.255.0'
    interface_spec['interfaces']['interface']['mtu'] = '1500'
    interface_spec['interfaces']['interface']['type'] = 'uplink'
    interface_spec['interfaces']['interface']['isConnected'] = 'true'
    interface_spec['interfaces']['interface']['connectedToId'] = 'virtualwire-2'

    response = session.create('interfaces', uri_parameters={'edgeId': edge_id},
                              query_parameters_dict={'action': 'patch'}, request_body_dict=interface_spec)

    session.view_response(response)

    return response['objectId']


def get_interface(session, object_id, edge_id='edge-2'):
    response = session.read('interface', uri_parameters={'edgeId': edge_id, 'index': object_id})
    session.view_response(response)


def get_interfaces(session, edge_id='edge-2'):
    response = session.read('interfaces', uri_parameters={'edgeId': edge_id})
    session.view_response(response)


def delete_interface(session, object_id, edge_id='edge-2'):
    response = session.delete('interface', uri_parameters={'edgeId': edge_id, 'index': object_id})
    session.view_response(response)


def delete_interfaces(session, edge_id='edge-2'):
    response = session.delete('interfaces', uri_parameters={'edgeId': edge_id})
    session.view_response(response)


def main():
    session = NsxClient(nsxraml_file, nsxmanager, nsx_username, nsx_password, debug=True)

    interface_index = create_interface(session)

    get_interface(session, interface_index)

    get_interfaces(session)

    delete_interface(session, interface_index)

    delete_interfaces(session)


if __name__ == "__main__":
    main()

