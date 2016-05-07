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


def create_application_rule(session, edge_id='edge-1'):
    app_rule_spec = session.extract_resource_body_example('appRules', 'create')

    app_rule_spec['applicationRule']['name'] = 'raml_test'
    app_rule_spec['applicationRule']['script'] = 'acl vmware_page url_beg /vmware redirect ' \
                                                 'location https://www.vmware.com/ if vmware_page'

    create_response = session.create('appRules', uri_parameters={'edgeId': edge_id},
                                     request_body_dict=app_rule_spec)

    session.view_response(create_response)

    return create_response['objectId']


def application_rule_by_id(session, object_id, edge_id='edge-1'):
    response = session.read('appRule', uri_parameters={'edgeId': edge_id, 'appruleID': object_id})
    session.view_response(response)


def application_rule(session, edge_id='edge-1'):
    response = session.read('appRules', uri_parameters={'edgeId': edge_id})
    session.view_response(response)


def update_application_rule(session, object_id, edge_id='edge-1'):
    app_rule_spec = session.extract_resource_body_example('appRule', 'update')

    app_rule_spec['applicationRule']['name'] = 'raml_test'
    app_rule_spec['applicationRule']['script'] = 'acl vmware_page_new url_beg /vmware redirect ' \
                                                 'location https://www.vmware.com/ if vmware_page_new'
    response = session.update('appRule', uri_parameters={'edgeId': edge_id, 'appruleID': object_id},
                              request_body_dict=app_rule_spec)

    session.view_response(response)


def delete_application_rule_by_id(session, object_id, edge_id='edge-1'):
    response = session.delete('appRule', uri_parameters={'edgeId': edge_id, 'appruleID': object_id})

    session.view_response(response)


def delete_application_rule(session, edge_id='edge-1'):
    response = session.delete('appRules', uri_parameters={'edgeId': edge_id})

    session.view_response(response)


def main():
    session = NsxClient(nsxraml_file, nsxmanager, nsx_username, nsx_password, debug=True)

    object_id = create_application_rule(session)

    application_rule_by_id(session, object_id)

    application_rule(session)

    update_application_rule(session, object_id)

    delete_application_rule_by_id(session, object_id)

    delete_application_rule(session)


if __name__ == "__main__":
    main()

