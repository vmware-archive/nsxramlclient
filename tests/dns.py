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


def configure_dns(session, edge_id='edge-1', ipaddr='10.117.0.1', listener='192.168.100.1'):
    config_spec = session.extract_resource_body_example('edgeDns', 'update')
    config_spec['dns']['enabled'] = 'true'
    config_spec['dns']['dnsServers']['ipAddress'] = ipaddr
    config_spec['dns']['cacheSize'] = '128'
    config_spec['dns']['listeners']['ipAddress'] = listener
    config_spec['dns']['logging']['logLevel'] = 'info'
    config_spec['dns']['logging']['enable'] = 'false'

    update_response = session.update('edgeDns', uri_parameters={'edgeId': edge_id}, request_body_dict=config_spec)
    session.view_response(update_response)


def retrieve_dns(session, edge_id='edge-1'):
    response = session.read('edgeDns', uri_parameters={'edgeId': edge_id})
    session.view_response(response)


def retrieve_dns_stats(session, edge_id='edge-1'):
    response = session.read('edgeDnsStats', uri_parameters={'edgeId': edge_id})
    session.view_response(response)


def delete_dns(session, edge_id='edge-1'):
    response = session.delete('edgeDns', uri_parameters={'edgeId': edge_id})
    session.view_response(response)


def main():
    session = NsxClient(nsxraml_file, nsxmanager, nsx_username, nsx_password, debug=True)
    configure_dns(session)
    retrieve_dns(session)
    retrieve_dns_stats(session)
    delete_dns(session)
    
    
if __name__ == "__main__":
    main()

