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


__author__ = 'cmullaney'

from tests.config import *
from nsxramlclient.client import NsxClient
import time

client_session = NsxClient(nsxraml_file, nsxmanager, nsx_username, nsx_password, debug=True)

macset_dict = client_session.extract_resource_body_example('macsetScopeCreate', 'create')
macset_dict['macset']['name'] = 'test0'

# CREATE macset on scope
newmacset_return = client_session.create('macsetScopeCreate', uri_parameters={'scopeId': 'globalroot-0'},
                                         request_body_dict=macset_dict)

# READ macset by ID
newmacset = dict(client_session.read('macset', uri_parameters={'macsetId': newmacset_return['objectId']})['body'])

# UPDATE macset by ID
newmacset['macset']['name'] = 'test1'
newmacset['macset']['revision'] = '1'
newmacset['macset']['value'] = '44:55:66:77:88:99'

time.sleep(10)

client_session.update('macset', uri_parameters={'macsetId': newmacset_return['objectId']},
                      request_body_dict=newmacset)

# READ macsets on scope
client_session.read('macsetScopeRead', uri_parameters={'scopeId': 'globalroot-0'})

time.sleep(10)

# DELETE macset by ID
client_session.delete('macset', uri_parameters={'macsetId': newmacset_return['objectId']})
