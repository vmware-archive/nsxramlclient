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


def get_vdnscopes(session):
    scope_response = session.read('vdnScopes')
    session.view_response(scope_response)
    return scope_response['objectId']


def get_vdnscope(session, vdn_scope):
    scope_response = session.read('vdnScope', uri_parameters={'scopeId': vdn_scope})
    session.view_response(scope_response)
    return scope_response['objectId']


def create_vdnscope(session, name, cluster_moid_list, description='created by nsxramlclient',
                    control_plane_mode='UNICAST_MODE'):
    vdn_create_spec = session.extract_resource_body_schema('vdnScopes', 'create')
    vdn_create_spec['vdnScope']['clusters']['cluster']['cluster']['objectId'] = cluster_moid_list[0]
    vdn_create_spec['vdnScope']['name'] = name
    vdn_create_spec['vdnScope']['description'] = description
    vdn_create_spec['vdnScope']['controlPlaneMode'] = control_plane_mode

    vdn_scope = session.create('vdnScopes', request_body_dict=vdn_create_spec)['objectId']

    if len(cluster_moid_list) > 1:
        for cluster in cluster_moid_list[1:]:
            vdn_edit_spec = session.extract_resource_body_schema('vdnScope', 'create')
            vdn_edit_spec['vdnScope']['objectId'] = vdn_scope
            vdn_edit_spec['vdnScope']['clusters']['cluster']['cluster']['objectId'] = cluster
            session.create('vdnScope', uri_parameters={'scopeId': vdn_scope},
                           query_parameters_dict={'action': 'expand'},
                           request_body_dict=vdn_edit_spec)

    return vdn_scope


def shrink_vdn_scope(session, vdn_scope, cluster_moid_list):
    for cluster in cluster_moid_list:
        vdn_edit_spec = session.extract_resource_body_schema('vdnScope', 'create')
        vdn_edit_spec['vdnScope']['objectId'] = vdn_scope
        vdn_edit_spec['vdnScope']['clusters']['cluster']['cluster']['objectId'] = cluster
        session.create('vdnScope', uri_parameters={'scopeId': vdn_scope}, query_parameters_dict={'action': 'shrink'},
                       request_body_dict=vdn_edit_spec)


def update_vdnscope_attributes(session, vdn_scope, new_name='Updated the name', new_desc='And updated description',
                               control_plane_mode='HYBRID_MODE'):
    vdn_update_spec = session.extract_resource_body_schema('vdnScopeAttribUpdate', 'update')
    vdn_update_spec['vdnScope']['name'] = new_name
    vdn_update_spec['vdnScope']['description'] = new_desc
    vdn_update_spec['vdnScope']['objectId'] = vdn_scope
    vdn_update_spec['vdnScope']['controlPlaneMode'] = control_plane_mode
    scope_update_resp = session.update('vdnScopeAttribUpdate', uri_parameters={'scopeId': vdn_scope},
                                       request_body_dict=vdn_update_spec)
    session.view_response(scope_update_resp)


def delete_vdn_scope(session, vdn_scope):
    scope_response = session.delete('vdnScope', uri_parameters={'scopeId': vdn_scope})
    session.view_response(scope_response)


def main():
    s = NsxClient(nsxraml_file, nsxmanager, nsx_username, nsx_password, debug=True)

    created_scope = create_vdnscope(s, 'TZ1', ['domain-c26', 'domain-c28'])

    get_vdnscopes(s)

    get_vdnscope(s, created_scope)

    shrink_vdn_scope(s, created_scope, ['domain-c28'])

    update_vdnscope_attributes(s, created_scope)

    get_vdnscope(s, created_scope)

    #delete_vdn_scope(s, created_scope)

if __name__ == "__main__":
    main()
