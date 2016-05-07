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


def vxlan_prep(session, cluster_moid, dvs_moid, ipaddresspool, vlan_id=0, vmknics=1, teaming='FAILOVER_ORDER',
               mtu=1600):
    """
    :param session: nsxramlclient session
    :param cluster_moid: The moid of the cluster to configure vxlan at
    :param dvs_moid: The moid of the dvs used for the VTEP
    :param ipaddresspool: The IP addresspool used to assign the VTEP IP from
    :param vlan_id: The VLAN used for the transport Network (use 0 if no VLAN is used)
    :param vmknics: VMKernel Interfaces to configure. Defaults to 1
    :param teaming: teaming value can be one of FAILOVER_ORDER|ETHER_CHANNEL|LACP_ACTIVE|LACP_PASSIVE|
    LOADBALANCE_LOADBASED|LOADBALANCE_SRCID|LOADBALANCE_SRCMAC|LACP_V2
    :param mtu: MTU for the VTEP, defaults to 1600
    :return: Returns the last tasks jobid
    """
    vxlan_prep_dvs = session.extract_resource_body_example('nwfabricConfig', 'create')
    vxlan_prep_dvs['nwFabricFeatureConfig']['resourceConfig']['resourceId'] = dvs_moid
    vxlan_prep_dvs['nwFabricFeatureConfig']['featureId'] = 'com.vmware.vshield.vsm.vxlan'
    vxlan_prep_dvs['nwFabricFeatureConfig']['resourceConfig'].update({'configSpec':
                                                                          {'@class': 'vdsContext',
                                                                           'switch': {'objectId': dvs_moid},
                                                                           'mtu': mtu,
                                                                           'teaming': teaming},
                                                                          })

    vxlan_prep_dvs_response = session.create('nwfabricConfig', request_body_dict=vxlan_prep_dvs)
    session.view_response(vxlan_prep_dvs_response)

    vxlan_prep_cluster = session.extract_resource_body_example('nwfabricConfig', 'create')
    vxlan_prep_cluster['nwFabricFeatureConfig']['resourceConfig']['resourceId'] = cluster_moid
    vxlan_prep_cluster['nwFabricFeatureConfig']['featureId'] = 'com.vmware.vshield.vsm.vxlan'
    vxlan_prep_cluster['nwFabricFeatureConfig']['resourceConfig'].update({'configSpec':
                                                                              {'@class': 'clusterMappingSpec',
                                                                               'switch': {'objectId': dvs_moid},
                                                                               'vlanId': vlan_id,
                                                                               'vmknicCount': vmknics,
                                                                               'ipPoolId': ipaddresspool},
                                                                          })

    vxlan_prep_cluster_response = session.create('nwfabricConfig', request_body_dict=vxlan_prep_cluster)
    session.view_response(vxlan_prep_cluster_response)
    return vxlan_prep_cluster_response['objectId']


def vxlan_unprep_cluster(session, cluster_moid):
    vxlan_prep_cluster = session.extract_resource_body_example('nwfabricConfig', 'delete')
    vxlan_prep_cluster['nwFabricFeatureConfig']['resourceConfig']['resourceId'] = cluster_moid
    vxlan_prep_cluster['nwFabricFeatureConfig']['featureId'] = 'com.vmware.vshield.vsm.vxlan'

    vxlan_prep_cluster_response = session.delete('nwfabricConfig', request_body_dict=vxlan_prep_cluster)
    session.view_response(vxlan_prep_cluster_response)
    return vxlan_prep_cluster_response['objectId']

def vxlan_unprep_dvs_context(session, dvs_moid):
    vxlan_prep_dvs = session.extract_resource_body_example('nwfabricConfig', 'delete')
    vxlan_prep_dvs['nwFabricFeatureConfig']['resourceConfig']['resourceId'] = dvs_moid
    vxlan_prep_dvs['nwFabricFeatureConfig']['featureId'] = 'com.vmware.vshield.vsm.vxlan'

    vxlan_prep_dvs_response = session.delete('nwfabricConfig', request_body_dict=vxlan_prep_dvs)
    session.view_response(vxlan_prep_dvs_response)
    return vxlan_prep_dvs_response['objectId']


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
    s = NsxClient(nsxraml_file, nsxmanager, nsx_username, nsx_password, debug=True)

    vxlan_prep_response = vxlan_prep(s, 'domain-c26', 'dvs-34', 'ipaddresspool-3')
    wait_for_job_completion(s, vxlan_prep_response, completion_status='COMPLETED')

    unprep_response = vxlan_unprep_cluster(s, 'domain-c26')
    wait_for_job_completion(s, unprep_response, completion_status='COMPLETED')
    vxlan_unprep_dvs_context(s, 'dvs-34')

if __name__ == "__main__":
    main()