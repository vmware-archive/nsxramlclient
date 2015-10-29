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


def get_ospf(session, edge_id = 'edge-1'):
    response = session.read('routingOSPF', uri_parameters={'edgeId': edge_id})

    session.view_response(response)

    return response['body']


def delete_ospf(session, edge_id = 'edge-1'):
    del_response = session.delete('routingOSPF', uri_parameters={'edgeId': edge_id})

    session.view_response(del_response)


def create_ospf(session, config, edge_id = 'edge-1'):
    create_response = session.update('routingOSPF', uri_parameters={'edgeId': edge_id},  request_body_dict =  config)

    session.view_response(create_response)


def main():
    session = NsxClient(nsxraml_file, nsxmanager, nsx_username, nsx_password, debug=True)
    ospf_config = get_ospf(session)
    delete_ospf(session)
    create_ospf(session, ospf_config)


if __name__ == "__main__":
    main()


