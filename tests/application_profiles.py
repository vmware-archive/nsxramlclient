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


def create_application_profile(session, edge_id='edge-1', method='cookie', c_name='JSESSIONID', c_mode='insert'):
    app_profile_spec = session.extract_resource_body_schema('applicationProfiles', 'create')

    app_profile_spec['applicationProfile']['name'] = 'raml_test'
    app_profile_spec['applicationProfile']['insertXForwardedFor'] = 'true'
    app_profile_spec['applicationProfile']['sslPassthrough'] = 'true'
    app_profile_spec['applicationProfile']['persistence']['method'] = method
    app_profile_spec['applicationProfile']['persistence']['cookieName'] = c_name
    app_profile_spec['applicationProfile']['persistence']['cookieMode'] = c_mode

    create_response = session.create('applicationProfiles', uri_parameters={'edgeId': edge_id},
                                     request_body_dict=app_profile_spec)

    session.view_response(create_response)

    return create_response['objectId']


def application_profile_by_id(session, object_id, edge_id='edge-1'):
    response = session.read('applicationProfile', uri_parameters={'edgeId': edge_id, 'appProfileID': object_id})
    session.view_response(response)


def application_profiles(session, edge_id='edge-1'):
    response = session.read('applicationProfiles', uri_parameters={'edgeId': edge_id})
    session.view_response(response)


def update_application_profile(session, object_id, edge_id='edge-1'):
    app_profile_spec = session.extract_resource_body_schema('applicationProfile', 'update')

    app_profile_spec['applicationProfile']['name'] = 'raml_test'
    app_profile_spec['applicationProfile']['insertXForwardedFor'] = 'true'
    app_profile_spec['applicationProfile']['sslPassthrough'] = 'false'
    app_profile_spec['applicationProfile']['persistence']['method'] = 'cookie'
    app_profile_spec['applicationProfile']['persistence']['cookieName'] = 'JSESSIONID'
    app_profile_spec['applicationProfile']['persistence']['cookieMode'] = 'insert'

    response = session.update('applicationProfile', uri_parameters={'edgeId': edge_id, 'appProfileID': object_id},
                              request_body_dict=app_profile_spec)

    session.view_response(response)


def delete_application_profile_by_id(session, object_id, edge_id='edge-1'):
    response = session.delete('applicationProfile', uri_parameters={'edgeId': edge_id, 'appProfileID': object_id})

    session.view_response(response)


def delete_application_profiles(session, edge_id='edge-1'):
    response = session.delete('applicationProfiles', uri_parameters={'edgeId': edge_id})

    session.view_response(response)


def main():
    session = NsxClient(nsxraml_file, nsxmanager, nsx_username, nsx_password, debug=True)

    object_id = create_application_profile(session)

    application_profile_by_id(session, object_id)

    application_profiles(session)

    update_application_profile(session, object_id)

    delete_application_profile_by_id(session, object_id)

    delete_application_profiles(session)


if __name__ == "__main__":
    main()

