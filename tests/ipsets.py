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


client_session = NsxClient(nsxraml_file, nsxmanager, nsx_username, nsx_password, debug=True)

ipset_dict = client_session.extract_resource_body_example('ipsetCreate', 'create')
ipset_dict['ipset']['name'] = 'Test'
ipset_dict['ipset']['value'] = '192.168.1.0/24'
ipset_dict['ipset']['inheritanceAllowed'] = 'True'

newipset_return = client_session.create('ipsetCreate', uri_parameters={'scopeMoref': 'globalroot-0'},
                                        request_body_dict=ipset_dict)

newipset = dict(client_session.read('ipset', uri_parameters={'ipsetId': newipset_return['objectId']})['body'])

newipset['ipset']['value'] = '10.0.0.0/16'
newipset['ipset']['inheritanceAllowed'] = 'False'

time.sleep(10)

client_session.update('ipset', uri_parameters={'ipsetId': newipset_return['objectId']}, request_body_dict=newipset)

client_session.read('ipsetList', uri_parameters={'scopeMoref': 'globalroot-0'})

time.sleep(10)

client_session.delete('ipset', uri_parameters={'ipsetId': newipset_return['objectId']})

