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

# TODO Add code to save the techsupport log to a file
# TODO Add code to test and save the snapshot log to a file

__author__ = 'yfauser'

from tests.config import *
from nsxramlclient.client import NsxClient
import time


s = NsxClient(nsxraml_file, nsxmanager, nsx_username, nsx_password, debug=False)


def create_controller():
    controller_spec = s.extract_resource_body_schema('nsxControllers', 'create')

    controller_spec['controllerSpec']['datastoreId'] = 'datastore-37'
    controller_spec['controllerSpec']['networkId'] = 'dvportgroup-36'
    controller_spec['controllerSpec']['resourcePoolId'] = 'domain-c26'
    controller_spec['controllerSpec']['ipPoolId'] = 'ipaddresspool-2'
    controller_spec['controllerSpec']['password'] = 'VMware1!VMware1!'

    create_response = s.create('nsxControllers', request_body_dict=controller_spec)

    s.view_response(create_response)

    return create_response['objectId'], create_response['body']


def read_all_controllers():
    response = s.read('nsxControllers')
    s.view_response(response)


def wait_for_controller(job_id):
    status_poll_count = 0
    while status_poll_count < 20:
        response = s.read('nsxControllerJob', uri_parameters={'jobId': job_id})
        s.view_response(response)
        status = response['body']['controllerDeploymentInfo']['status']
        if status == 'Success':
            return True
        elif status == 'Failure':
            raise Exception('Controller deployment failed')
        else:
            time.sleep(30)

    raise Exception('Timeout waiting for controller to be deployed')


def delete_controller(controller_id, force=False):
        removal_response = s.delete('nsxController', uri_parameters={'controllerId': controller_id},
                                    query_parameters_dict={'forceRemoval': force})
        s.view_response(removal_response)


def cluster_config():
    config_read = s.read('nsxControllerCluster')
    s.view_response(config_read)
    config = config_read['body']
    config['controllerConfig']['sslEnabled'] = False
    config_response = s.update('nsxControllerCluster', request_body_dict=config)
    s.view_response(config_response)
    config_read = s.read('nsxControllerCluster')
    s.view_response(config_read)


def controller_techsupport(controller_id):
    response = s.read('nsxControllerLogs', uri_parameters={'controllerId': controller_id})
    s.view_response(response)


def set_controller_syslog(controller_id):
    syslog_spec = s.extract_resource_body_schema('nsxControllerSyslog', 'create')
    syslog_spec['controllerSyslogServer']['syslogServer'] = '172.17.100.129'
    s.view_body_dict(syslog_spec)
    set_response = s.create('nsxControllerSyslog', uri_parameters={'controllerId': controller_id},
                            request_body_dict=syslog_spec)
    s.view_response(set_response)


def delete_controller_syslog(controller_id):
    del_response = s.delete('nsxControllerSyslog', uri_parameters={'controllerId': controller_id})
    s.view_response(del_response)


def get_controller_syslog(controller_id):
    response = s.read('nsxControllerSyslog', uri_parameters={'controllerId': controller_id})
    s.view_response(response)


def update_controller_credentials():
    password_spec = s.extract_resource_body_schema('nsxControllerPassword', 'update')
    password_spec['controllerCredential']['apiPassword'] = 'VMware-12345!'
    s.view_body_dict(password_spec)
    response = s.update('nsxControllerPassword', request_body_dict=password_spec)
    s.view_response(response)


controller1_id, job_id_resp = create_controller()
wait_for_controller(job_id_resp)
#controller2_id, job_id_resp = create_controller()
#wait_for_controller(job_id_resp)
#controller3_id, job_id_resp = create_controller()
#wait_for_controller(job_id_resp)
read_all_controllers()
update_controller_credentials()
cluster_config()
controller_techsupport(controller1_id)
set_controller_syslog(controller1_id)
get_controller_syslog(controller1_id)
delete_controller_syslog(controller1_id)
#delete_controller(controller3_id, force=True)
#delete_controller(controller2_id, force=True)
delete_controller(controller1_id, force=True)

