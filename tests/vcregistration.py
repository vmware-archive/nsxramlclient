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

s = NsxClient(nsxraml_file, nsxmanager, nsx_username, nsx_password, debug=False)

def vc_registration():
    vc_reg = s.extract_resource_body_example('vCenterConfig', 'update')

    vc_reg['vcInfo']['ipAddress'] = '172.17.100.60'
    vc_reg['vcInfo']['userName'] = 'administrator@vsphere.local'
    vc_reg['vcInfo']['assignRoleToUser'] = 'true'
    vc_reg['vcInfo']['password'] = 'vmware'
    vc_reg['vcInfo']['certificateThumbprint'] = 'B1:22:F5:FD:BA:7A:C0:91:1A:66:D6:A6:A0:B6:82:23:C6:30:97:7E'

    s.view_body_dict(vc_reg)

    s.update('vCenterConfig', request_body_dict=vc_reg)

    vc_reg_response = s.read('vCenterConfig')
    s.view_response(vc_reg_response)

def sso_registration_set():
    sso_reg = s.extract_resource_body_example('ssoConfig', 'create')

    sso_reg['ssoConfig']['ssoAdminUsername'] = 'administrator@vsphere.local'
    sso_reg['ssoConfig']['ssoAdminUserpassword'] = 'vmware'
    sso_reg['ssoConfig']['ssoLookupServiceUrl'] = 'https://172.17.100.60:7444/lookupservice/sdk'
    sso_reg['ssoConfig']['certificateThumbprint'] = '33:80:F0:58:DB:D4:59:A2:46:14:83:14:2C:48:C3:29:70:25:BE:31'

    s.view_body_dict(sso_reg)

    sso_reg_response = s.create('ssoConfig', request_body_dict=sso_reg)
    s.view_response(sso_reg_response)

def sso_registration_read():
    sso_reg = s.read('ssoConfig')
    s.view_response(sso_reg)
    sso_status = s.read('ssoStatus')
    s.view_response(sso_status)

def sso_delete_registration():
    resp = s.delete('ssoConfig')
    s.view_response(resp)

vc_registration()
sso_registration_set()
sso_registration_read()
sso_delete_registration()



