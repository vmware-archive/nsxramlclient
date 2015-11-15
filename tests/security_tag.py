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


def create_security_tag(session, name, object_type='TestTag', type_name='SecurityTagTest',
                        description='RAMLclient test security tag'):
    security_tag_spec = session.extract_resource_body_schema('securityTag', 'create')

    security_tag_spec['securityTag']['name'] = name
    security_tag_spec['securityTag']['objectTypeName'] = object_type
    security_tag_spec['securityTag']['type']['typeName'] = type_name
    security_tag_spec['securityTag']['description'] = description

    create_response = session.create('securityTag', request_body_dict=security_tag_spec)

    session.view_response(create_response)

    return create_response['objectId'], create_response['body']


def get_security_tags(session):
    response = session.read('securityTag')
    session.view_response(response)


def get_security_tag_by_id(session, security_tag_id):
    response = session.read('securityTag', uri_parameters={'tagId': security_tag_id})
    session.view_response(response)


def attach_security_tag(session, security_tag_id):
    response = session.update('securityTagVM', uri_parameters={'tagId': security_tag_id, 'vmMoid': 'vm-288'})
    session.view_response(response)


def detach_security_tag(session, security_tag_id):
    response = session.delete('securityTagVM', uri_parameters={'tagId': security_tag_id, 'vmMoid': 'vm-288'})
    session.view_response(response)


def delete_security_tag(session, security_tag_id):
    del_response = session.delete('securityTagDelete', uri_parameters={'tagId': security_tag_id})
    session.view_response(del_response)


def main():
    session = NsxClient(nsxraml_file, nsxmanager, nsx_username, nsx_password, debug=True)
    
    security_tag_id, job_id_resp = create_security_tag(session, 'RAMLTag')
    
    get_security_tags(session)
    
    get_security_tag_by_id(session, security_tag_id)
    
    attach_security_tag(session, security_tag_id)
    
    detach_security_tag(session, security_tag_id)
    
    delete_security_tag(session, security_tag_id)


if __name__ == "__main__":
    main()

