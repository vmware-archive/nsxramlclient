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

s = NsxClient(nsxraml_file, nsxmanager, nsx_username, nsx_password, debug=False)


def ippool_add():
    new_ip_pool = s.extract_resource_body_example('ipPools', 'create')

    new_ip_pool['ipamAddressPool']['ipRanges']['ipRangeDto']['startAddress'] = '172.17.100.65'
    new_ip_pool['ipamAddressPool']['ipRanges']['ipRangeDto']['endAddress'] = '172.17.100.67'
    new_ip_pool['ipamAddressPool']['gateway'] = '172.17.100.1'
    new_ip_pool['ipamAddressPool']['prefixLength'] = '24'
    new_ip_pool['ipamAddressPool']['dnsServer1'] = '172.17.100.11'
    new_ip_pool['ipamAddressPool']['dnsServer2'] = '172.17.100.12'
    new_ip_pool['ipamAddressPool']['name'] = 'pynsxramlclient'

    s.view_body_dict(new_ip_pool)

    create_resp = s.create('ipPools', uri_parameters={'scopeId': 'globalroot-0'}, request_body_dict=new_ip_pool)

    s.view_response(create_resp)
    return create_resp['objectId']


def query_ippool(objectId):
    ippool_list_resp = s.read('ipPools', uri_parameters={'scopeId': 'globalroot-0'})
    s.view_response(ippool_list_resp)

    ippool_read_resp = s.read('ipPool', uri_parameters={'poolId': objectId})
    s.view_response(ippool_read_resp)
    return ippool_read_resp['body']


def update_ippool(objectId, body_dict):
    body_dict['ipamAddressPool']['name'] = 'updatedBypynsxramlclient'
    revission = int(body_dict['ipamAddressPool']['revision'])
    revission += 1
    body_dict['ipamAddressPool']['revision'] = str(revission)
    update_resp = s.update('ipPool', uri_parameters={'poolId': objectId}, request_body_dict=body_dict)
    s.view_response(update_resp)

def allocate_next_ip(objectId):
    body_dict = s.extract_resource_body_example('ipPoolAllocate', 'create')
    body_dict['ipAddressRequest']['allocationMode'] = 'ALLOCATE'
    allocate_response = s.create('ipPoolAllocate', uri_parameters={'poolId': objectId}, request_body_dict=body_dict)
    s.view_response(allocate_response)
    return allocate_response['body']['allocatedIpAddress']['ipAddress']


def allocate_specific_ip(objectId, ip):
    body_dict = s.extract_resource_body_example('ipPoolAllocate', 'create')
    body_dict['ipAddressRequest']['allocationMode'] = 'RESERVE'
    body_dict['ipAddressRequest']['ipAddress'] = ip
    allocate_response = s.create('ipPoolAllocate', uri_parameters={'poolId': objectId}, request_body_dict=body_dict)
    s.view_response(allocate_response)
    return allocate_response['body']['allocatedIpAddress']['ipAddress']


def read_all_allocations_in_pool(objectId):
    list_ips_resp = s.read('ipPoolAllocate', uri_parameters={'poolId': objectId})
    s.view_response(list_ips_resp)


def release_ips(objectId, list_of_ips):
    for ip in list_of_ips:
        release_response = s.delete('ipAddressRelease', uri_parameters={'poolId': objectId, 'ipAddress': ip})
        s.view_response(release_response)

def ippool_delete(objectId):
    delete_resp = s.delete('ipPool', uri_parameters={'poolId': objectId})
    s.view_response(delete_resp)

ippool_object_id = ippool_add()
ippool_source_body_dict = query_ippool(ippool_object_id)
update_ippool(ippool_object_id, ippool_source_body_dict)
allocated_ips = []
allocated_ips.append(allocate_next_ip(ippool_object_id))
allocated_ips.append(allocate_specific_ip(ippool_object_id, '172.17.100.67'))
read_all_allocations_in_pool(ippool_object_id)
time.sleep(10)
release_ips(ippool_object_id, allocated_ips)
time.sleep(10)
ippool_delete(ippool_object_id)