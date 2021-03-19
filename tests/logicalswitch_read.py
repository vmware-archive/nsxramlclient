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
from nsxramlclient.exceptions import NsxError

__author__ = 'yfauser'

TRANSPORT_ZONE = 'TZ1'

client_session = NsxClient(nsxraml_file, nsxmanager, nsx_username, nsx_password, debug=True, fail_mode='raise')

lswitch_id1 = 'virtualwire-237'
lswitch_id2 = 'virtualwire-999'
lswitch_id3 = 'blaar'

# find the objectId of the Scope with the name of the Transport Zone
vdn_scopes = client_session.read('vdnScopes', 'read')['body']
vdn_scope_dict_list = [scope_dict for scope_dict in vdn_scopes['vdnScopes'].items()]
vdn_scope = [scope[1]['objectId'] for scope in vdn_scope_dict_list if scope[1]['name'] == TRANSPORT_ZONE][0]

# Read the properties of the logical switch
new_ls_props = client_session.read('logicalSwitch', uri_parameters={'virtualWireID': lswitch_id1})
client_session.view_response(new_ls_props)

# Read the property of an not existing virtual wire ID
try:
    new_ls_props = client_session.read('logicalSwitch', uri_parameters={'virtualWireID': lswitch_id2})
    client_session.view_response(new_ls_props)
except NsxError as e:
    print("### caught exception !!!!")
    print(e.status, e.msg)


# Try to read properties using a invalid virtual wire Id
try:
    new_ls_props = client_session.read('logicalSwitch', uri_parameters={'virtualWireID': lswitch_id3})
    client_session.view_response(new_ls_props)
except NsxError as e:
    print("### caught exception !!!!")
    print(e.status, e.msg)
