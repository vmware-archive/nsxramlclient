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


def create_edge_syslog(session, edge_id='edge-1'):
    syslog_spec = session.extract_resource_body_example('syslog', 'update')

    syslog_spec['syslog']['protocol'] = 'tcp'
    syslog_spec['syslog']['serverAddresses']['ipAddress'] = '192.168.110.80'

    response = session.update('syslog', uri_parameters={'edgeId': edge_id}, request_body_dict=syslog_spec)
    session.view_response(response)


def get_edge_syslog(session, edge_id='edge-1'):
    response = session.read('syslog', uri_parameters={'edgeId': edge_id})
    session.view_response(response)


def delete_edge_syslog(session, edge_id='edge-1'):
    response = session.delete('syslog', uri_parameters={'edgeId': edge_id})
    session.view_response(response)


def main():
    session = NsxClient(nsxraml_file, nsxmanager, nsx_username, nsx_password, debug=True)

    create_edge_syslog(session)

    get_edge_syslog(session)

    delete_edge_syslog(session)


if __name__ == "__main__":
    main()

