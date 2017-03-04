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


def query_routes(session, edge_id='edge-1'):
    response = session.read('routingConfig', uri_parameters={'edgeId': edge_id})
    session.view_response(response)


def query_static_routes(session, edge_id='edge-1'):
    response = session.read('routingConfigStatic', uri_parameters={'edgeId': edge_id})
    session.view_response(response)


def query_global_routes(session, edge_id='edge-1'):
    response = session.read('routingGlobalConfig', uri_parameters={'edgeId': edge_id})
    session.view_response(response)


def configure_static_route(session, edge_id='edge-1'):
    static_spec = session.extract_resource_body_schema('routingConfigStatic', 'update')

    static_spec['staticRouting']['staticRoutes']['route']['description'] = 'route1'
    static_spec['staticRouting']['staticRoutes']['route']['vnic'] = '0'
    static_spec['staticRouting']['staticRoutes']['route']['network'] = '172.16.1.12/22'
    static_spec['staticRouting']['staticRoutes']['route']['nextHop'] = '172.16.1.14'
    static_spec['staticRouting']['staticRoutes']['route']['mtu'] = '1500'
    static_spec['staticRouting']['defaultRoute']['description'] = 'defaultRoute'
    static_spec['staticRouting']['defaultRoute']['vnic'] = '0'
    static_spec['staticRouting']['defaultRoute']['gatewayAddress'] = '172.16.1.12'
    static_spec['staticRouting']['defaultRoute']['mtu'] = '1500'

    response = session.update('routingConfigStatic', uri_parameters={'edgeId': edge_id}, request_body_dict=static_spec)

    session.view_response(response)


def configure_global_route(session, edge_id='edge-1'):
    global_spec = session.extract_resource_body_schema('routingGlobalConfig', 'update')

    global_spec['routingGlobalConfig']['routerId'] = '1.1.1.1'
    global_spec['routingGlobalConfig']['logging']['enable'] = 'false'
    global_spec['routingGlobalConfig']['logging']['logLevel'] = 'info'
    global_spec['routingGlobalConfig']['ipPrefixes']['ipPrefix']['name'] = 'RAMLTest'
    global_spec['routingGlobalConfig']['ipPrefixes']['ipPrefix']['ipAddress'] = '10.112.196.160/24'

    response = session.update('routingGlobalConfig', uri_parameters={'edgeId': edge_id}, request_body_dict=global_spec)

    session.view_response(response)


def delete_routes(session, edge_id='edge-1'):
    response = session.delete('routingConfig', uri_parameters={'edgeId': edge_id})
    session.view_response(response)


def delete_static_routes(session, edge_id='edge-1'):
    response = session.delete('routingConfigStatic', uri_parameters={'edgeId': edge_id})
    session.view_response(response)


def main():
    session = NsxClient(nsxraml_file, nsxmanager, nsx_username, nsx_password, debug=True)

    query_routes(session)

    query_static_routes(session)

    query_global_routes(session)

    configure_static_route(session)

    configure_global_route(session)

    delete_routes(session)

    delete_static_routes(session)


if __name__ == "__main__":
    main()

