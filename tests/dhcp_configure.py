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


def create_dhcp(session, edge_id='edge-1'):
    dhcp_spec = session.extract_resource_body_schema('dhcp', 'update')

    dhcp_spec['dhcp']['enabled'] = 'true'
    dhcp_spec['dhcp']['staticBindings']['staticBinding']['macAddress'] = '12:34:56:78:90:AB'
    dhcp_spec['dhcp']['staticBindings']['staticBinding']['vmId'] = 'vm-111'
    dhcp_spec['dhcp']['staticBindings']['staticBinding']['vnicId'] = '1'
    dhcp_spec['dhcp']['staticBindings']['staticBinding']['hostname'] = 'RAMLHost'
    dhcp_spec['dhcp']['staticBindings']['staticBinding']['ipAddress'] = '192.168.4.2'
    dhcp_spec['dhcp']['staticBindings']['staticBinding']['subnetMask'] = '255.255.255.0'
    dhcp_spec['dhcp']['staticBindings']['staticBinding']['defaultGateway'] = '192.168.4.1'
    dhcp_spec['dhcp']['staticBindings']['staticBinding']['domainName'] = 'eng.vmware.com'
    dhcp_spec['dhcp']['staticBindings']['staticBinding']['primaryNameServer'] = '192.168.4.1'
    dhcp_spec['dhcp']['staticBindings']['staticBinding']['secondaryNameServer'] = '4.2.2.4'
    dhcp_spec['dhcp']['staticBindings']['staticBinding']['leaseTime'] = 'infinite'
    # dhcp_spec['dhcp']['staticBindings']['staticBinding']['autoConfigDNS'] = 'true'
    # dhcp_spec['dhcp']['ipPools']['ipPool']['autoConfigDNS'] = 'true'
    dhcp_spec['dhcp']['ipPools']['ipPool']['ipRange'] = '192.168.4.192-192.168.4.220'
    dhcp_spec['dhcp']['ipPools']['ipPool']['defaultGateway'] = '192.168.4.1'
    dhcp_spec['dhcp']['ipPools']['ipPool']['subnetMask'] = '255.255.255.0'
    dhcp_spec['dhcp']['ipPools']['ipPool']['domainName'] = 'eng.vmware.com'
    dhcp_spec['dhcp']['ipPools']['ipPool']['primaryNameServer'] = '192.168.4.1'
    dhcp_spec['dhcp']['ipPools']['ipPool']['secondaryNameServer'] = '4.2.2.4'
    dhcp_spec['dhcp']['ipPools']['ipPool']['leaseTime'] = '3600'
    dhcp_spec['dhcp']['logging']['enable'] = 'false'
    dhcp_spec['dhcp']['logging']['logLevel'] = 'info'

    response = session.update('dhcp', uri_parameters={'edgeId': edge_id}, request_body_dict=dhcp_spec)

    session.view_response(response)


def get_dhcp_config(session, edge_id='edge-1'):
    response = session.read('dhcp', uri_parameters={'edgeId': edge_id})
    session.view_response(response)


def append_ip_pool(session, edge_id='edge-1'):
    ippool_spec = session.extract_resource_body_schema('dhcpPool', 'create')

    ippool_spec['ipPool']['ipRange'] = '192.168.5.192-192.168.5.220'
    ippool_spec['ipPool']['defaultGateway'] = '192.168.5.1'
    ippool_spec['ipPool']['subnetMask'] = '255.255.255.0'
    ippool_spec['ipPool']['domainName'] = 'sales.vmware.com'
    ippool_spec['ipPool']['primaryNameServer'] = '192.168.5.1'
    ippool_spec['ipPool']['secondaryNameServer'] = '4.2.2.4'
    ippool_spec['ipPool']['leaseTime'] = '3600'

    response = session.create('dhcpPool', uri_parameters={'edgeId': edge_id}, request_body_dict=ippool_spec)
    session.view_response(response)
    return response['objectId']


def delete_ip_pool(session, object_id, edge_id='edge-1'):
    response = session.delete('dhcpPoolID', uri_parameters={'edgeId': edge_id, 'poolID': object_id})
    session.view_response(response)


def append_static_binding(session, edge_id='edge-1'):
    static_spec = session.extract_resource_body_schema('dhcpStaticBinding', 'create')

    static_spec['staticBinding']['macAddress'] = '12:34:56:78:90:AD'
    static_spec['staticBinding']['vmId'] = 'vm-112'
    static_spec['staticBinding']['vnicId'] = '1'
    static_spec['staticBinding']['hostname'] = 'RAMLHostStatic'
    static_spec['staticBinding']['ipAddress'] = '192.168.5.2'
    static_spec['staticBinding']['subnetMask'] = '255.255.255.0'
    static_spec['staticBinding']['defaultGateway'] = '192.168.5.1'
    static_spec['staticBinding']['domainName'] = 'sales.vmware.com'
    static_spec['staticBinding']['primaryNameServer'] = '192.168.5.1'
    static_spec['staticBinding']['secondaryNameServer'] = '4.2.2.4'
    static_spec['staticBinding']['leaseTime'] = 'infinite'

    response = session.create('dhcpStaticBinding', uri_parameters={'edgeId': edge_id}, request_body_dict=static_spec)
    session.view_response(response)
    return response['objectId']


def delete_static_binding(session, object_id, edge_id='edge-1'):
    response = session.delete('dhcpStaticBindingID', uri_parameters={'edgeId': edge_id, 'bindingID': object_id})
    session.view_response(response)


def delete_dhcp_config(session, edge_id='edge-1'):
    response = session.delete('dhcp', uri_parameters={'edgeId': edge_id})
    session.view_response(response)


def main():
    session = NsxClient(nsxraml_file, nsxmanager, nsx_username, nsx_password, debug=True)

    create_dhcp(session)

    get_dhcp_config(session)

    ippool_id = append_ip_pool(session)

    delete_ip_pool(session, ippool_id)

    static_id = append_static_binding(session)

    delete_static_binding(session, static_id)

    delete_dhcp_config(session)


if __name__ == "__main__":
    main()

