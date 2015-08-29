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

def readAllconfig():
    # Test read all dfw config

    all_dfw_config = client_session.read('dfwConfig')
    client_session.view_response(all_dfw_config)

def readByFilters():

    # Test read only specific parts by supplying filters
    l3_dfw_config = client_session.read('dfwConfig', query_parameters_dict={'ruleType': 'LAYER3'})
    client_session.view_response(l3_dfw_config)

    l3_dfw_config_id = client_session.read('dfwConfig', query_parameters_dict={'ruleType': 'LAYER3',
                                                                               'ruleId': '5969'})
    client_session.view_response(l3_dfw_config_id)

    edge_fw_config = client_session.read('dfwConfig', query_parameters_dict={'ruleType': 'LAYER3',
                                                                             'edgeId': 'edge-1028'})
    client_session.view_response(edge_fw_config)

    l3_dfw_by_section_name = client_session.read('dfwL3Section', query_parameters_dict={'name':
                                                                                            'Default Section Layer3'})
    client_session.view_response(l3_dfw_by_section_name)

    l2_dfw_by_section_name = client_session.read('dfwL2Section', query_parameters_dict={'name':
                                                                                            'Default Section Layer2'})
    client_session.view_response(l2_dfw_by_section_name)

def readByIds():

    l3_dfw_by_section_id = client_session.read('dfwL3SectionId', uri_parameters={'sectionId': '1300'})
    print l3_dfw_by_section_id
    client_session.view_response(l3_dfw_by_section_id)

    l2_dfw_by_section_id = client_session.read('dfwL2SectionId', uri_parameters={'sectionId': '1014'})
    client_session.view_response(l2_dfw_by_section_id)

def createNewL3Section():

    l3section_bdict = client_session.extract_resource_body_schema('dfwL3Section', 'create')

    service_dict = l3section_bdict['section']['rule'][0]['services']
    service_dict['service']['destinationPort'] = 80
    service_dict['service']['protocol'] = 6
    service_dict['service']['subProtocol'] = 6

    source_dict = l3section_bdict['section']['rule'][0]['sources']['source'][0]

    source_dict['isValid'] = 'true'
    source_dict['name'] = 'MySource'
    source_dict['type'] = 'Ipv4Address'
    source_dict['value'] = '10.10.10.1'

    destination_dict = l3section_bdict['section']['rule'][0]['destinations']['destination'][0]

    destination_dict['isValid'] = 'true'
    destination_dict['name'] = 'MyDestination'
    destination_dict['type'] = 'Ipv4Address'
    destination_dict['value'] = '20.20.20.1'


    l3section_bdict['section']['@name'] = 'CreatedByRamlClient'
    l3section_bdict['section']['rule'][0]['@logged'] = 'false'
    l3section_bdict['section']['rule'][0]['name'] = 'RuleCreatedByRamlClient'
    l3section_bdict['section']['rule'][0]['action'] = 'DENY'
    l3section_bdict['section']['rule'][0]['services'] = service_dict
    l3section_bdict['section']['rule'][0]['sources']['source'][0] = source_dict
    l3section_bdict['section']['rule'][0]['destinations']['destination'][0] = destination_dict
    l3section_bdict['section']['rule'][0]['appliedToList']['appliedTo']['isValid'] = 'true'
    l3section_bdict['section']['rule'][0]['appliedToList']['appliedTo']['name'] = 'DISTRIBUTED_FIREWALL'
    l3section_bdict['section']['rule'][0]['appliedToList']['appliedTo']['type'] = 'DISTRIBUTED_FIREWALL'
    l3section_bdict['section']['rule'][0]['appliedToList']['appliedTo']['value'] = 'DISTRIBUTED_FIREWALL'

    l3section_bdict['section']['rule'][0]['sources']['source'].pop(1)
    l3section_bdict['section']['rule'][0]['destinations']['destination'].pop(1)
    l3section_bdict['section']['rule'].pop(1)

    client_session.view_body_dict(l3section_bdict)

    new_section = client_session.create('dfwL3Section', request_body_dict=l3section_bdict)
    client_session.view_response(new_section)

def updateL3Section(section_name):

    l3_dfw_by_name_response = client_session.read('dfwL3Section', query_parameters_dict={'name': section_name})
    client_session.view_response(l3_dfw_by_name_response)

    etag_value = l3_dfw_by_name_response['Etag']
    l3_dfw_section_update = l3_dfw_by_name_response['body']

    l3_dfw_section_update['section']['@name'] = 'FirstUpdateByRamlClient'

    update_response = client_session.update('dfwL3SectionName', uri_parameters={'sectionName': section_name},
                                            additional_headers={'If-match': etag_value},
                                            request_body_dict=l3_dfw_section_update)
    client_session.view_response(update_response)

    time.sleep(10)

    l3_dfw_by_section_response = client_session.read('dfwL3Section',
                                                     query_parameters_dict={'name': 'FirstUpdateByRamlClient'})
    client_session.view_response(l3_dfw_by_section_response)

    etag_value = l3_dfw_by_section_response['Etag']
    l3_dfw_section_update = l3_dfw_by_section_response['body']
    section_id = l3_dfw_section_update['section']['@id']

    l3_dfw_section_update['section']['@name'] = 'CreatedByRamlClient'

    update_response = client_session.update('dfwL3SectionId', uri_parameters={'sectionId': section_id},
                                            additional_headers={'If-match': etag_value},
                                            request_body_dict=l3_dfw_section_update)
    client_session.view_response(update_response)

def L3Rules(section_name):

    l3_dfw_by_name_response = client_session.read('dfwL3Section', query_parameters_dict={'name': section_name})
    section_id = l3_dfw_by_name_response['body']['section']['@id']
    etag_value = l3_dfw_by_name_response['Etag']

    l3_rule_dict = client_session.extract_resource_body_schema('dfwL3Rules', 'create')

    l3_rule_dict['rule'].pop('services')
    l3_rule_dict['rule']['destinations']['destination'].pop(1)
    l3_rule_dict['rule']['sources']['source'].pop(1)

    l3_rule_dict['rule']['destinations']['destination'][0]['isValid'] = 'true'
    l3_rule_dict['rule']['destinations']['destination'][0]['name'] = 'AddedRuleDest'
    l3_rule_dict['rule']['destinations']['destination'][0]['type'] = 'Ipv4Address'
    l3_rule_dict['rule']['destinations']['destination'][0]['value'] = '11.11.11.1'

    l3_rule_dict['rule']['sources']['source'][0]['isValid'] = 'true'
    l3_rule_dict['rule']['sources']['source'][0]['name'] = 'AddedRuleSource'
    l3_rule_dict['rule']['sources']['source'][0]['type'] = 'Ipv4Address'
    l3_rule_dict['rule']['sources']['source'][0]['value'] = '12.12.12.1'

    l3_rule_dict['rule']['appliedToList']['appliedTo']['isValid'] = 'true'
    l3_rule_dict['rule']['appliedToList']['appliedTo']['name'] = 'DISTRIBUTED_FIREWALL'
    l3_rule_dict['rule']['appliedToList']['appliedTo']['type'] = 'DISTRIBUTED_FIREWALL'
    l3_rule_dict['rule']['appliedToList']['appliedTo']['value'] = 'DISTRIBUTED_FIREWALL'

    l3_rule_dict['rule']['@logged'] = 'false'
    l3_rule_dict['rule']['name'] = 'RuleCreatedByRamlClient'
    l3_rule_dict['rule']['action'] = 'DENY'

    l3_dfw_rule_create_response = client_session.create('dfwL3Rules',
                                                        uri_parameters={'sectionId': section_id},
                                                        additional_headers={'If-match': etag_value},
                                                        request_body_dict=l3_rule_dict)
    client_session.view_response(l3_dfw_rule_create_response)

    new_rule_id = l3_dfw_rule_create_response['objectId']

    l3_dfw_rule_read_response = client_session.read('dfwL3Rule', uri_parameters={'sectionId': section_id,
                                                                                 'ruleId': new_rule_id})
    client_session.view_response(l3_dfw_rule_read_response)

    updated_rule = l3_dfw_rule_read_response['body']
    etag_value = l3_dfw_rule_read_response['Etag']

    updated_rule['rule']['name'] = 'UpdatedByRAMLClient'

    l3_dfw_rule_update_response = client_session.update('dfwL3Rule', uri_parameters={'sectionId': section_id,
                                                                                     'ruleId': new_rule_id},
                                                        additional_headers={'If-match': etag_value},
                                                        request_body_dict=updated_rule)
    client_session.view_response(l3_dfw_rule_update_response)
    time.sleep(10)

    l3_dfw_rule_read_response = client_session.read('dfwL3Rule', uri_parameters={'sectionId': section_id,
                                                                                 'ruleId': new_rule_id})
    etag_value = l3_dfw_rule_read_response['Etag']


    delete_response = client_session.delete('dfwL3Rule', uri_parameters={'sectionId': section_id,
                                                                         'ruleId': new_rule_id},
                                            additional_headers={'If-match': etag_value})
    client_session.view_response(delete_response)

def deleteL3Sections(section_name):
    l3_dfw_by_name_response = client_session.read('dfwL3Section', query_parameters_dict={'name': section_name})
    client_session.view_response(l3_dfw_by_name_response)

    section_id = l3_dfw_by_name_response['body']['section']['@id']

    delete_response = client_session.delete('dfwL3SectionId', uri_parameters={'sectionId': section_id})

    client_session.view_response(delete_response)

def createNewL2Section():

    l2section_bdict = client_session.extract_resource_body_schema('dfwL2Section', 'create')

    source_dict = l2section_bdict['section']['rule'][0]['sources']['source'][0]

    source_dict['isValid'] = 'true'
    source_dict['name'] = 'TestLS'
    source_dict['type'] = 'VirtualWire'
    source_dict['value'] = 'virtualwire-1289'

    destination_dict = l2section_bdict['section']['rule'][0]['destinations']['destination'][0]

    destination_dict['isValid'] = 'true'
    destination_dict['name'] = 'TestLS'
    destination_dict['type'] = 'VirtualWire'
    destination_dict['value'] = 'virtualwire-1289'


    l2section_bdict['section']['@name'] = 'CreatedByRamlClient'
    l2section_bdict['section']['rule'][0]['@logged'] = 'false'
    l2section_bdict['section']['rule'][0]['name'] = 'RuleCreatedByRamlClient'
    l2section_bdict['section']['rule'][0]['action'] = 'DENY'
    l2section_bdict['section']['rule'][0].pop('services')
    l2section_bdict['section']['rule'][0]['sources']['source'][0] = source_dict
    l2section_bdict['section']['rule'][0]['destinations']['destination'][0] = destination_dict
    l2section_bdict['section']['rule'][0]['appliedToList']['appliedTo']['isValid'] = 'true'
    l2section_bdict['section']['rule'][0]['appliedToList']['appliedTo']['name'] = 'DISTRIBUTED_FIREWALL'
    l2section_bdict['section']['rule'][0]['appliedToList']['appliedTo']['type'] = 'DISTRIBUTED_FIREWALL'
    l2section_bdict['section']['rule'][0]['appliedToList']['appliedTo']['value'] = 'DISTRIBUTED_FIREWALL'

    l2section_bdict['section']['rule'][0]['sources']['source'].pop(1)
    l2section_bdict['section']['rule'][0]['destinations']['destination'].pop(1)
    l2section_bdict['section']['rule'].pop(1)

    client_session.view_body_dict(l2section_bdict)

    new_section = client_session.create('dfwL2Section', request_body_dict=l2section_bdict)
    client_session.view_response(new_section)

def L2Rules(section_name):

    l2_dfw_by_name_response = client_session.read('dfwL2Section', query_parameters_dict={'name': section_name})
    section_id = l2_dfw_by_name_response['body']['section']['@id']
    etag_value = l2_dfw_by_name_response['Etag']

    l2_rule_dict = client_session.extract_resource_body_schema('dfwL3Rules', 'create')

    l2_rule_dict['rule'].pop('services')
    l2_rule_dict['rule']['destinations']['destination'].pop(1)
    l2_rule_dict['rule']['sources']['source'].pop(1)

    l2_rule_dict['rule']['destinations']['destination'][0]['isValid'] = 'true'
    l2_rule_dict['rule']['destinations']['destination'][0]['name'] = 'TestLS'
    l2_rule_dict['rule']['destinations']['destination'][0]['type'] = 'VirtualWire'
    l2_rule_dict['rule']['destinations']['destination'][0]['value'] = 'virtualwire-1289'

    l2_rule_dict['rule']['sources']['source'][0]['isValid'] = 'TestLS'
    l2_rule_dict['rule']['sources']['source'][0]['name'] = 'AddedRuleSource'
    l2_rule_dict['rule']['sources']['source'][0]['type'] = 'VirtualWire'
    l2_rule_dict['rule']['sources']['source'][0]['value'] = 'virtualwire-1289'

    l2_rule_dict['rule']['appliedToList']['appliedTo']['isValid'] = 'true'
    l2_rule_dict['rule']['appliedToList']['appliedTo']['name'] = 'DISTRIBUTED_FIREWALL'
    l2_rule_dict['rule']['appliedToList']['appliedTo']['type'] = 'DISTRIBUTED_FIREWALL'
    l2_rule_dict['rule']['appliedToList']['appliedTo']['value'] = 'DISTRIBUTED_FIREWALL'

    l2_rule_dict['rule']['@logged'] = 'false'
    l2_rule_dict['rule']['name'] = 'RuleCreatedByRamlClient'
    l2_rule_dict['rule']['action'] = 'DENY'

    l2_dfw_rule_create_response = client_session.create('dfwL2Rules',
                                                        uri_parameters={'sectionId': section_id},
                                                        additional_headers={'If-match': etag_value},
                                                        request_body_dict=l2_rule_dict)
    client_session.view_response(l2_dfw_rule_create_response)

    new_rule_id = l2_dfw_rule_create_response['objectId']

    l2_dfw_rule_read_response = client_session.read('dfwL2Rule', uri_parameters={'sectionId': section_id,
                                                                                 'ruleId': new_rule_id})
    client_session.view_response(l2_dfw_rule_read_response)

    updated_rule = l2_dfw_rule_read_response['body']
    etag_value = l2_dfw_rule_read_response['Etag']

    updated_rule['rule']['name'] = 'UpdatedByRAMLClient'

    l2_dfw_rule_update_response = client_session.update('dfwL2Rule', uri_parameters={'sectionId': section_id,
                                                                                     'ruleId': new_rule_id},
                                                        additional_headers={'If-match': etag_value},
                                                        request_body_dict=updated_rule)
    client_session.view_response(l2_dfw_rule_update_response)
    time.sleep(10)

    l2_dfw_rule_read_response = client_session.read('dfwL2Rule', uri_parameters={'sectionId': section_id,
                                                                                 'ruleId': new_rule_id})
    etag_value = l2_dfw_rule_read_response['Etag']


    delete_response = client_session.delete('dfwL2Rule', uri_parameters={'sectionId': section_id,
                                                                         'ruleId': new_rule_id},
                                            additional_headers={'If-match': etag_value})
    client_session.view_response(delete_response)

def updateL2Section(section_name):

    l2_dfw_by_name_response = client_session.read('dfwL2Section', query_parameters_dict={'name': section_name})
    client_session.view_response(l2_dfw_by_name_response)

    etag_value = l2_dfw_by_name_response['Etag']
    l3_dfw_section_update = l2_dfw_by_name_response['body']

    l3_dfw_section_update['section']['@name'] = 'FirstUpdateByRamlClient'

    update_response = client_session.update('dfwL2SectionName', uri_parameters={'sectionName': section_name},
                                            additional_headers={'If-match': etag_value},
                                            request_body_dict=l3_dfw_section_update)
    client_session.view_response(update_response)

    time.sleep(10)

    l2_dfw_by_section_response = client_session.read('dfwL2Section',
                                                     query_parameters_dict={'name': 'FirstUpdateByRamlClient'})
    client_session.view_response(l2_dfw_by_section_response)

    etag_value = l2_dfw_by_section_response['Etag']
    l3_dfw_section_update = l2_dfw_by_section_response['body']
    section_id = l3_dfw_section_update['section']['@id']

    l3_dfw_section_update['section']['@name'] = 'CreatedByRamlClient'

    update_response = client_session.update('dfwL2SectionId', uri_parameters={'sectionId': section_id},
                                            additional_headers={'If-match': etag_value},
                                            request_body_dict=l3_dfw_section_update)
    client_session.view_response(update_response)

def deleteL2Sections(section_name):
    l2_dfw_by_name_response = client_session.read('dfwL2Section', query_parameters_dict={'name': section_name})
    client_session.view_response(l2_dfw_by_name_response)

    section_id = l2_dfw_by_name_response['body']['section']['@id']

    delete_response = client_session.delete('dfwL2SectionId', uri_parameters={'sectionId': section_id})

    client_session.view_response(delete_response)


readAllconfig()
readByFilters()
readByIds()
createNewL3Section()
L3Rules('CreatedByRamlClient')
updateL3Section('CreatedByRamlClient')
deleteL3Sections('CreatedByRamlClient')
createNewL2Section()
L2Rules('CreatedByRamlClient')
updateL2Section('CreatedByRamlClient')
deleteL2Sections('CreatedByRamlClient')





