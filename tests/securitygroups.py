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


def sec_group_create(session, name):
    new_sec_group = session.extract_resource_body_schema('secGroupGlobal', 'create')
    dynamic_member_def = new_sec_group['securitygroup']['dynamicMemberDefinition']['dynamicSet']
    exclude_member = new_sec_group['securitygroup']['excludeMember']

    dynamic_member_def['dynamicCriteria']['criteria'] = 'contains'
    dynamic_member_def['dynamicCriteria']['isValid'] = 'true'
    dynamic_member_def['dynamicCriteria']['key'] = 'VM.NAME'
    dynamic_member_def['dynamicCriteria']['value'] = 'Web'

    session.view_body_dict(new_sec_group)


def main():
    s = NsxClient(nsxraml_file, nsxmanager, nsx_username, nsx_password, debug=True)

    get_all_sec_groups(s)
    sec_group_create(s, 'newSecGroup')

if __name__ == "__main__":
    main()