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


def create_configuration(session):
    configure_spec = session.extract_resource_body_schema('dfwDrafts', 'create')

    configure_spec['firewallDraft']['@name'] = 'RAMLDraft'
    configure_spec['firewallDraft']['description'] = 'Test Draft created with RAML'
    configure_spec['firewallDraft']['preserve'] = 'true'
    configure_spec['firewallDraft']['mode'] = 'userdefined'
    configure_spec['firewallDraft']['config']['contextId'] = 'globalroot-0'
    configure_spec['firewallDraft']['config']['layer3Sections']['section']['@name'] = "Default Section Layer3"
    configure_spec['firewallDraft']['config']['layer3Sections']['section']['rule']['@id'] = '1001'
    configure_spec['firewallDraft']['config']['layer3Sections']['section']['rule']['@disabled'] = 'false'
    configure_spec['firewallDraft']['config']['layer3Sections']['section']['rule']['@logged'] = 'false'
    configure_spec['firewallDraft']['config']['layer3Sections']['section']['rule']['name'] = 'Default Rule'
    configure_spec['firewallDraft']['config']['layer3Sections']['section']['rule']['action'] = 'allow'
    configure_spec['firewallDraft']['config']['layer3Sections']['section']['rule']['precedence'] = 'default'
    configure_spec['firewallDraft']['config']['layer2Sections']['section']['@name'] = "Default Section Layer2"
    configure_spec['firewallDraft']['config']['layer2Sections']['section']['rule']['@id'] = '1003'
    configure_spec['firewallDraft']['config']['layer2Sections']['section']['rule']['@disabled'] = 'false'
    configure_spec['firewallDraft']['config']['layer2Sections']['section']['rule']['@logged'] = 'false'
    configure_spec['firewallDraft']['config']['layer2Sections']['section']['rule']['name'] = 'Default Rule'
    configure_spec['firewallDraft']['config']['layer2Sections']['section']['rule']['action'] = 'allow'
    configure_spec['firewallDraft']['config']['layer2Sections']['section']['rule']['precedence'] = 'default'

    response = session.create('dfwDrafts', request_body_dict=configure_spec)

    session.view_response(response)

    return response['body']['firewallDraft']['@id']


def get_configuration(session, object_id):
    response = session.read('dfwDraft', uri_parameters={'draftID': object_id})
    session.view_response(response)


def get_configurations(session):
    response = session.read('dfwDrafts')
    session.view_response(response)


def delete_configuration(session, object_id):
    response = session.delete('dfwDraft', uri_parameters={'draftID': object_id})
    session.view_response(response)


def delete_configurations(session):
    response = session.delete('dfwDrafts')
    session.view_response(response)


def main():
    session = NsxClient(nsxraml_file, nsxmanager, nsx_username, nsx_password, debug=True)

    configuration_id = create_configuration(session)

    get_configuration(session, configuration_id)

    get_configurations(session)

    delete_configuration(session, configuration_id)

    delete_configurations(session)


if __name__ == "__main__":
    main()

