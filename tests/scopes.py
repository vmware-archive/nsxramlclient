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

from nsxramlclient.client import NsxClient
from config import *

client_session = NsxClient(nsxraml_file, nsxmanager, nsx_username, nsx_password, debug=False)

# Get specific scope Information
response_scope1 = client_session.read('vdnScope', uri_parameters={'scopeId': 'vdnscope-1'})
client_session.view_response(response_scope1)

# Get all scopes
response_all_scopes = client_session.read('vdnScopes')
client_session.view_response(response_all_scopes)

# Add a scope
create_body = client_session.extract_resource_body_schema('vdnScopes', 'create')
client_session.view_body_dict(create_body)

create_body['vdnScope']['clusters']['cluster']['cluster']

#create_response = client_session.create('vdnScopes', request_body_dict=create_body)

#TODO: Complete the tests for Scopes

