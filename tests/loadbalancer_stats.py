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


def get_loadbalancer_stats(session, edge_id='edge-1'):
    response = session.read('lbStatistics', uri_parameters={'edgeId': edge_id})
    session.view_response(response)


def update_loadbalancer_acc_mode(session, edge_id='edge-1'):
    response = session.create('lbAcceleration', uri_parameters={'edgeId': edge_id},
                              query_parameters_dict={'enable': 'true'})
    session.view_response(response)


def update_loadbalancer_mem_cond(session, edge_id='edge-3'):
    response = session.create('lbAcceleration', uri_parameters={'edgeId': edge_id},
                              query_parameters_dict={'enable': 'true'})
    session.view_response(response)


def main():
    session = NsxClient(nsxraml_file, nsxmanager, nsx_username, nsx_password, debug=True)

    get_loadbalancer_stats(session)

    update_loadbalancer_acc_mode(session)

    update_loadbalancer_mem_cond(session)


if __name__ == "__main__":
    main()

