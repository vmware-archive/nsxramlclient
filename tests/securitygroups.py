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

__author__ = 'yfauser'

from tests.config import *
from nsxramlclient.client import NsxClient
import time


def get_all_sec_groups(session):
    result = session.read('secGroupScope', uri_parameters={'scopeId': 'globalroot-0'})
    session.view_response(result)


def get_vm_in_sec_group(session, secgroupid):
    response = session.read('secGroupVMNodes', uri_parameters={'objectId': secgroupid})
    session.view_response(response)


def get_ips_in_sec_group(session, secgroupid):
    response = session.read('secGroupIPNodes', uri_parameters={'objectId': secgroupid})
    session.view_response(response)


def get_macs_in_sec_group(session, secgroupid):
    response = session.read('secGroupMacNodes', uri_parameters={'objectId': secgroupid})
    session.view_response(response)


def get_vnics_in_sec_group(session, secgroupid):
    response = session.read('secGroupVnicNodes', uri_parameters={'objectId': secgroupid})
    session.view_response(response)


def sec_group_add_member(session, secgroupid, member_moref):
    add_response = session.update('secGroupMember', uri_parameters={'objectId': secgroupid,
                                                                    'memberMoref': member_moref})
    session.view_response(add_response)


def sec_group_delete_member(session, secgroupid, member_moref):
    add_response = session.delete('secGroupMember', uri_parameters={'objectId': secgroupid,
                                                                    'memberMoref': member_moref})
    session.view_response(add_response)


def get_sec_group_valid_types(session):
    response = session.read('secGroupMemberTypes', uri_parameters={'scopeId': 'globalroot-0'})
    session.view_response(response)

    return response['body']


def get_sec_group_by_vm(session, vmid):
    response = session.read('secGroupLookupVM', uri_parameters={'virtualMachineId': vmid})
    session.view_response(response)


def get_sec_group_by_id(session, secgroupid):
    response = session.read('secGroupObject', uri_parameters={'objectId': secgroupid})
    session.view_response(response)
    return response['body']


def update_sec_group(session, secgroupid, body):
    response = session.update('secGroupUpdate', uri_parameters={'objectId': secgroupid}, request_body_dict=body)
    session.view_response(response)


def delete_sec_group(session, secgroupid):
    response = session.delete('secGroupObject', uri_parameters={'objectId': secgroupid},
                              query_parameters_dict={'force': 'true'})
    session.view_response(response)


def add_dynamic_match(session, secgroupid, criteria='VM.NAME', key='Web'):
    body_content = session.read('secGroupObject', uri_parameters={'objectId': secgroupid})['body']
    extracted_schema = session.extract_resource_body_example('secGroupCreate', 'create')
    dynamic_member_def = extracted_schema['securitygroup']['dynamicMemberDefinition']
    dynamic_member_def['dynamicSet']['dynamicCriteria']['criteria'] = 'contains'
    dynamic_member_def['dynamicSet']['dynamicCriteria']['isValid'] = 'true'
    dynamic_member_def['dynamicSet']['dynamicCriteria']['key'] = 'VM.NAME'
    dynamic_member_def['dynamicSet']['dynamicCriteria']['value'] = 'Web'
    body_content['securitygroup'].update({'dynamicMemberDefinition': dynamic_member_def})
    update_sec_group(session, secgroupid, body_content)


def empty_sec_group_create(session, name):
    new_sec_group = session.extract_resource_body_example('secGroupCreate', 'create')
    new_sec_group['securitygroup']['name'] = name
    new_sec_group['securitygroup'].pop('dynamicMemberDefinition')
    new_sec_group['securitygroup'].pop('excludeMember')
    new_sec_group['securitygroup'].pop('scope')
    new_sec_group['securitygroup'].pop('type')
    new_sec_group['securitygroup'].pop('member')
    session.view_body_dict(new_sec_group)

    create_response = session.create('secGroupCreate', uri_parameters={'scopeId': 'globalroot-0'},
                                     request_body_dict=new_sec_group)
    session.view_response(create_response)
    return create_response['body']


def main():
    s = NsxClient(nsxraml_file, nsxmanager, nsx_username, nsx_password, debug=True)

    get_sec_group_valid_types(s)

    new_sec_group = empty_sec_group_create(s, 'newSecGroup')
    print new_sec_group

    sec_group_add_member(s, new_sec_group, '503bfba4-007b-0c27-aac7-26c71c1cbcff.000')
    get_all_sec_groups(s)

    add_dynamic_match(s, new_sec_group)

    get_sec_group_by_id(s, new_sec_group)
    get_sec_group_by_vm(s, 'vm-55')
    get_vm_in_sec_group(s, new_sec_group)
    get_ips_in_sec_group(s, new_sec_group)
    get_macs_in_sec_group(s, new_sec_group)
    get_vnics_in_sec_group(s, new_sec_group)

    time.sleep(20)

    sec_group_delete_member(s, new_sec_group, '503bfba4-007b-0c27-aac7-26c71c1cbcff.000')

    time.sleep(20)

    delete_sec_group(s, new_sec_group)

if __name__ == "__main__":
    main()
