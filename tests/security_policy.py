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

# TODO: Add tests for 'hierarchy', 'securityActionVM', 'securityActionSecGroup, 'vmApplicableSecurityAction'
# TODO: Add tests for 'serviceComposerDFWSynch', 'secGroupPolicies'

__author__ = 'yfauser'

from tests.config import *
from nsxramlclient.client import NsxClient
from distutils.util import strtobool
import sys


def user_yes_no_query(question):
    sys.stdout.write('%s [y/n]\n' % question)
    while True:
        try:
            return strtobool(raw_input().lower())
        except ValueError:
            sys.stdout.write('Please respond with \'y\' or \'n\'.\n')


def get_sg_group_id(session, sec_group_name):
    all_sec_groups = session.read('secGroupScope', uri_parameters={'scopeId': 'globalroot-0'})['body']
    if type(all_sec_groups['list']['securitygroup']) is dict:
        if all_sec_groups['list']['securitygroup']['name'] == sec_group_name:
            return all_sec_groups['list']['securitygroup']['objectId']
    elif type(all_sec_groups['list']['securitygroup']) is list:
        for sg in all_sec_groups['list']['securitygroup']:
            if sg['name'] == sec_group_name:
                return sg['objectId']


def sec_empty_policy_create(session):
    policy_create_dict = session.extract_resource_body_example('securityPolicy', 'create')
    session.view_body_dict(policy_create_dict)

    policy_create_dict['securityPolicy']['name'] = 'TestPolicy'
    policy_create_dict['securityPolicy']['description'] = 'TestPolicy created by nsxramlclient'
    policy_create_dict['securityPolicy']['precedence'] = 1
    policy_create_dict['securityPolicy'].pop('actionsByCategory')

    create_response = session.create('securityPolicy', request_body_dict=policy_create_dict)
    session.view_response(create_response)

    return create_response['objectId']


def sec_policy_read(session, objectid='all'):
    response = session.read('securityPolicyID', uri_parameters={'ID': objectid})
    session.view_response(response)

    return response['body']


def sec_policy_add_fw_rule(session, objectid):
    policy_config = session.read('securityPolicyID', uri_parameters={'ID': objectid})['body']
    policy_create_dict = session.extract_resource_body_example('securityPolicy', 'create')
    fw_action = policy_create_dict['securityPolicy']['actionsByCategory']['action']
    fw_action['@class'] = 'firewallSecurityAction'
    fw_action['category'] = 'firewall'
    fw_action['action'] = 'reject'
    fw_action['actionType'] = 'reject'
    fw_action['direction'] = 'outbound'
    fw_action['logged'] = 'true'
    fw_action['isEnabled'] = 'true'
    fw_action['name'] = 'TestRule1'
    fw_action['scope'] = {'id': 'globalroot-0', 'name': 'Global', 'objectTypeName': 'GlobalRoot'}
    fw_action.pop('applications')

    policy_config['securityPolicy'].update({'actionsByCategory': {'category': 'firewall',
                                                                  'action': fw_action}})

    session.view_body_dict(policy_config)

    update_resp = session.update('securityPolicyID', uri_parameters={'ID': objectid}, request_body_dict=policy_config)
    session.view_response(update_resp)


def sec_policy_attach_sec_group(session, secgroupid, secpolicyid):
    policy_config = session.read('securityPolicyID', uri_parameters={'ID': secpolicyid})['body']
    session.view_body_dict(policy_config)
    policy_config['securityPolicy']['securityGroupBinding'] = {'objectId': secgroupid}
    session.view_body_dict(policy_config)
    update_resp = session.update('securityPolicyID', uri_parameters={'ID': secpolicyid},
                                 request_body_dict=policy_config)
    session.view_response(update_resp)


def sec_policy_delete(session, objectid, force='true'):
    response = session.delete('securityPolicyID', uri_parameters={'ID': objectid},
                              query_parameters_dict={'force': force})
    session.view_response(response)


def sec_policy_retrieve_action(session, objectid):
    response = session.read('securityActions', uri_parameters={'ID': objectid})
    session.view_response(response)

    return response['body']


def main():
    s = NsxClient(nsxraml_file, nsxmanager, nsx_username, nsx_password, debug=True)

    new_sec_policy_id = sec_empty_policy_create(s)
    sec_policy_read(s)
    sec_policy_read(s, new_sec_policy_id)
    sec_policy_retrieve_action(s, new_sec_policy_id)

    sec_policy_add_fw_rule(s, new_sec_policy_id)
    sec_group_id = get_sg_group_id(s, 'Test_SG')
    sec_policy_attach_sec_group(s, sec_group_id, new_sec_policy_id)

    user_yes_no_query('ready to delete created objects?')

    sec_policy_delete(s, new_sec_policy_id)


if __name__ == "__main__":
    main()
