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


def cluster_prep(session, cluster_moid):
    cluster_prep_body = session.extract_resource_body_schema('nwfabricConfig', 'create')
    cluster_prep_body['nwFabricFeatureConfig']['resourceConfig']['resourceId'] = cluster_moid
    return session.create('nwfabricConfig', request_body_dict=cluster_prep_body)


def cluster_unprep(session, cluster_moid):
    cluster_prep_body = session.extract_resource_body_schema('nwfabricConfig', 'delete')
    cluster_prep_body['nwFabricFeatureConfig']['resourceConfig']['resourceId'] = cluster_moid
    return session.delete('nwfabricConfig', request_body_dict=cluster_prep_body)


def wait_for_job_completion(session, job_id, completion_status):
    status_poll_count = 0
    while status_poll_count < 20:
        response = session.read('taskFrameworkJobs', uri_parameters={'jobId': job_id})
        session.view_response(response)
        status = response['body']['jobInstances']['jobInstance']['status']
        if status == completion_status:
            return True
        else:
            time.sleep(30)
            status_poll_count += 1

    raise Exception('Timeout waiting for Job to complete')


def main():
    s = NsxClient(nsxraml_file, nsxmanager, nsx_username, nsx_password, debug=False)

    prep_response = cluster_prep(s, 'domain-c26')
    s.view_response(prep_response)
    wait_for_job_completion(s, prep_response['objectId'], completion_status='COMPLETED')

    #unprep_response = cluster_unprep(s, 'domain-c26')
    #s.view_response(unprep_response)
    #wait_for_job_completion(s, unprep_response['objectId'], completion_status='COMPLETED')


if __name__ == "__main__":
    main()
