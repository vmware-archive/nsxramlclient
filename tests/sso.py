#!/usr/bin/env python

# coding=utf-8
#
# Copyright 2015 VMware, Inc. All Rights Reserved.
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

# TODO Add code to save the techsupport log to a file
# TODO Add code to test and save the snapshot log to a file


__author__ = 'shrirang'

from tests.config import *
from nsxramlclient.client import NsxClient
import time


def get_sso_config(session):
    response = session.read('ssoConfig')
    session.view_response(response)


def get_sso_config_status(session):
    response = session.read('ssoStatus')
    session.view_response(response)

    
def delete_sso(session):
    response = session.delete('ssoConfig')

    
def create_sso(session, ssoAdminUserpassword = 'VMware1!', 
                        ssoLookupServiceUrl = 'https://vc-l-01a.corp.local:7444/lookupservice/sdk',
                        ssoAdminUsername = 'administrator@vsphere.local'):

    sso_spec = session.extract_resource_body_schema('ssoConfig', 'create')
    
    sso_spec['ssoConfig']['ssoLookupServiceUrl'] = ssoLookupServiceUrl
    sso_spec['ssoConfig']['ssoAdminUsername'] = ssoAdminUsername
    sso_spec['ssoConfig']['ssoAdminUserpassword'] = ssoAdminUserpassword
    
    create_response = session.create('ssoConfig', request_body_dict = sso_spec)

    session.view_response(create_response)


def main():
    session = NsxClient(nsxraml_file, nsxmanager, nsx_username, nsx_password, debug=True)
    get_sso_config(session)
    get_sso_config_status(session)
    delete_sso(session)
    create_sso(session)


if __name__ == "__main__":
    main()

