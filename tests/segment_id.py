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


def create_segment_id(session):
    vdnsegment_spec = session.extract_resource_body_schema('vdnSegmentPools', 'create')

    vdnsegment_spec['segmentRange']['name'] = 'TestSegmentId'
    vdnsegment_spec['segmentRange']['begin'] = '6000'
    vdnsegment_spec['segmentRange']['end'] = '6500'

    create_response = session.create('vdnSegmentPools', request_body_dict=vdnsegment_spec)
    session.view_response(create_response)
    return create_response['objectId'], create_response['body']


def get_segment_id(session):
    response = session.read('vdnSegmentPools')
    session.view_response(response)


def get_segment_id_by_id(session, segment_id):
    response = session.read('vdnSegmentPool', uri_parameters={'segmentPoolId': segment_id})
    session.view_response(response)


def delete_segment_id(session, segment_id):
    del_response = session.delete('vdnSegmentPool', uri_parameters={'segmentPoolId': segment_id})
    session.view_response(del_response)


def main():
    session = NsxClient(nsxraml_file, nsxmanager, nsx_username, nsx_password, debug=False)
    segment_id, job_id_resp = create_segment_id(session)
    get_segment_id(session)
    get_segment_id_by_id(session, segment_id)
    delete_segment_id(session, segment_id)


if __name__ == "__main__":
    main()

