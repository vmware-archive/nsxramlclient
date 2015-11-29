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


def create_ha(session, edge_id='edge-1'):
    ha_spec = session.extract_resource_body_schema('highAvailability', 'update')

    ha_spec['highAvailability']['vnic'] = '1'
    ha_spec['highAvailability']['ipAddresses']['ipAddress'] = '192.168.10.1/30'
    ha_spec['highAvailability']['declareDeadTime'] = '6'

    response = session.update('highAvailability', uri_parameters={'edgeId': edge_id}, request_body_dict=ha_spec)

    session.view_response(response)


def get_ha(session, edge_id='edge-1'):
    response = session.read('highAvailability', uri_parameters={'edgeId': edge_id})
    session.view_response(response)


def delete_ha(session, edge_id='edge-1'):
    response = session.delete('highAvailability', uri_parameters={'edgeId': edge_id})
    session.view_response(response)


def main():
    session = NsxClient(nsxraml_file, nsxmanager, nsx_username, nsx_password, debug=True)

    create_ha(session)

    get_ha(session)

    delete_ha(session)


if __name__ == "__main__":
    main()

