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


def test_segment_pools():
    ### Test Segment ID Pool Operations

    # Get all configured Segment Pools
    get_segment_resp = client_session.read('vdnSegmentPools')
    client_session.view_response(get_segment_resp)

    # Add a Segment Pool
    segments_create_body = client_session.extract_resource_body_example('vdnSegmentPools', 'create')
    client_session.view_body_dict(segments_create_body)

    segments_create_body['segmentRange']['begin'] = '11002'
    segments_create_body['segmentRange']['end'] = '11003'
    segments_create_body['segmentRange']['name'] = 'legacy'

    create_response = client_session.create('vdnSegmentPools', request_body_dict=segments_create_body)
    client_session.view_response(create_response)

    time.sleep(5)

    # Update the new Segment Pool:
    update_segment_body = client_session.extract_resource_body_example('vdnSegmentPool', 'update')
    update_segment_body['segmentRange']['name'] = 'PythonTest'
    update_segment_body['segmentRange']['end'] = '11005'
    client_session.update('vdnSegmentPool', uri_parameters={'segmentPoolId': create_response['objectId']},
                          request_body_dict=update_segment_body)

    time.sleep(5)

    # Display a specific Segment pool (the new one)
    specific_segement_resp = client_session.read('vdnSegmentPool', uri_parameters={'segmentPoolId':
                                                                                    create_response['objectId']})
    client_session.view_response(specific_segement_resp)

    time.sleep(5)

    # Delete new Segment Pool
    client_session.delete('vdnSegmentPool', uri_parameters={'segmentPoolId': create_response['objectId']})

def test_mcast_pools():
    ### Test Multicast Pool Operations

    # Add a multicast Pool
    mcastpool_create_body = client_session.extract_resource_body_example('vdnMulticastPools', 'create')
    client_session.view_body_dict(mcastpool_create_body)

    mcastpool_create_body['multicastRange']['desc'] = 'Test'
    mcastpool_create_body['multicastRange']['begin'] = '235.0.0.0'
    mcastpool_create_body['multicastRange']['end'] = '235.1.1.1'
    mcastpool_create_body['multicastRange']['name'] = 'legacy'

    create_response = client_session.create('vdnMulticastPools', request_body_dict=mcastpool_create_body)
    client_session.view_response(create_response)

    # Get all configured Multicast Pools
    get_mcast_pools = client_session.read('vdnMulticastPools')
    client_session.view_response(get_mcast_pools)

    time.sleep(5)

    # Update the newly created mcast pool
    mcastpool_update_body = client_session.extract_resource_body_example('vdnMulticastPool', 'update')
    mcastpool_update_body['multicastRange']['end'] = '235.3.1.1'
    mcastpool_update_body['multicastRange']['name'] = 'Python'

    update_response = client_session.update('vdnMulticastPool', uri_parameters={'multicastAddresssRangeId':
                                                                              create_response['objectId']},
                                                                              request_body_dict=mcastpool_update_body)
    client_session.view_response(update_response)

    # display a specific Multicast Pool
    get_mcast_pool = client_session.read('vdnMulticastPool', uri_parameters={'multicastAddresssRangeId':
                                                                              create_response['objectId']})
    client_session.view_response(get_mcast_pool)

    # Delete new mcast pool
    client_session.delete('vdnMulticastPool', uri_parameters={'multicastAddresssRangeId': create_response['objectId']})


#test_segment_pools()
#test_mcast_pools()

