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

__author__ = 'yfauser'

from tests.config import *
from nsxramlclient.client import NsxClient

s = NsxClient(nsxraml_file, nsxmanager, nsx_username, nsx_password, debug=True)

def create_edge():
    edge_template = s.extract_resource_body_schema('nsxEdges', 'create')

    s.view_body_dict(edge_template)

    appliance_props = edge_template['edge']['appliances']['appliance'].copy()
    appliance_props['datastoreId'] = 'datastore-3003'
    appliance_props['resourcePoolId'] = 'resgroup-4087'

    vnic1 = edge_template['edge']['vnics']['vnic'][0].copy()
    vnic1['portgroupId'] = 'dvportgroup-2595'
    vnic1.pop('addressGroups')

    cli_settings = edge_template['edge']['cliSettings'].copy()

    new_edge = {}
    new_edge.update({'edge': {'appliances': {'appliance': appliance_props,
                                             'applianceSize': 'compact'},
                              'datacenterMoid': 'datacenter-2',
                              'vnics': {'vnic': vnic1},
                              'type': 'gatewayservices',
                              'cliSettings': cli_settings,
                              'name': 'test'}})

    s.view_body_dict(new_edge)

    create_response = s.create('nsxEdges', request_body_dict=new_edge)
    s.view_response(create_response)

create_edge()

