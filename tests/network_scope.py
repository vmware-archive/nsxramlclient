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


def create_network_scope(session):
    network_scope_spec = session.extract_resource_body_schema('vdnScopes', 'create')

    network_scope_spec['vdnScope']['name'] = 'TestVdnScope'
    network_scope_spec['vdnScope']['clusters']['cluster']['cluster']['objectId'] = 'domain-c7'
    network_scope_spec['vdnScope']['description'] = 'Some test description'
    network_scope_spec['vdnScope']['controlPlaneMode'] = 'UNICAST_MODE'

    create_response = session.create('vdnScopes', request_body_dict=network_scope_spec)

    session.view_response(create_response)

    return create_response['objectId'], create_response['body']


def get_network_scope(session):
    response = session.read('vdnScopes')
    session.view_response(response)


def get_scope_by_id(session, scope_id):
    response = session.read('vdnScopes', uri_parameters={'scopeId': scope_id})
    session.view_response(response)


def update_scope_by_id(session, scope_id):
    network_scope_spec = session.extract_resource_body_schema('vdnScopeAttribUpdate', 'update')
    network_scope_spec['vdnScope']['name'] = 'TestVdnScope'
    network_scope_spec['vdnScope']['clusters']['cluster']['cluster']['objectId'] = 'domain-c7'
    network_scope_spec['vdnScope']['objectId'] = scope_id
    network_scope_spec['vdnScope']['description'] = 'Updated description'

    update_response = session.update('vdnScopeAttribUpdate', uri_parameters={'scopeId': scope_id}, request_body_dict=
                                     network_scope_spec)

    session.view_response(update_response)


def delete_network_scope(session, scope_id):
    del_response = session.delete('vdnScope', uri_parameters={'scopeId': scope_id})
    session.view_response(del_response)


def main():
    session = NsxClient(nsxraml_file, nsxmanager, nsx_username, nsx_password, debug=False)
    scope_id, job_id_resp = create_network_scope(session)
    get_network_scope(session)
    get_scope_by_id(session, scope_id)
    update_scope_by_id(session, scope_id)
    delete_network_scope(session, scope_id)


if __name__ == "__main__":
    main()

