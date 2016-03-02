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


TRANSPORT_ZONE = 'TZ1'

client_session = NsxClient(nsxraml_file, nsxmanager, nsx_username, nsx_password, debug=True)


# find the objectId of the Scope with the name of the Transport Zone
vdn_scopes = client_session.read('vdnScopes', 'read')['body']
vdn_scope_dict_list = [scope_dict for scope_dict in vdn_scopes['vdnScopes'].items()]
vdn_scope = [scope[1]['objectId'] for scope in vdn_scope_dict_list if scope[1]['name'] == TRANSPORT_ZONE][0]

# get a template dict for the lswitch create
lswitch_create_dict = client_session.extract_resource_body_schema('logicalSwitches', 'create')
client_session.view_body_dict(lswitch_create_dict)

# fill the details for the new lswitch in the body dict
lswitch_create_dict['virtualWireCreateSpec']['controlPlaneMode'] = 'UNICAST_MODE'
lswitch_create_dict['virtualWireCreateSpec']['name'] = 'Emanuele'
lswitch_create_dict['virtualWireCreateSpec']['tenantId'] = 'Tenant1'

# create new lswitch
new_ls = client_session.create('logicalSwitches', uri_parameters={'scopeId': vdn_scope},
                               request_body_dict=lswitch_create_dict)
client_session.view_response(new_ls)

# list all logical switches
all_lswitches = client_session.read('logicalSwitchesGlobal')
client_session.view_response(all_lswitches)

# list all logical switches in transport Zone
tz_lswitches = client_session.read('logicalSwitches', uri_parameters={'scopeId': vdn_scope})
client_session.view_response(tz_lswitches)

# Read the properties of the new logical switch
new_ls_props = client_session.read('logicalSwitch', uri_parameters={'virtualWireID': new_ls['objectId']})
client_session.view_response(new_ls_props)

time.sleep(5)

# update the properties of the new logical switch (name)
updated_ls_dict = new_ls_props['body']
updated_ls_dict['virtualWire']['name'] = 'ThisIsANewName'
update_resp = client_session.update('logicalSwitch', uri_parameters={'virtualWireID': new_ls['objectId']},
                                    request_body_dict=updated_ls_dict)

time.sleep(5)

# delete new logical created ealier
#client_session.delete('logicalSwitch', uri_parameters={'virtualWireID': new_ls['objectId']})

#TODO: test moving a VM to the new logical switch
# move a VM to a logical switch
vm_attach_body_dict = client_session.extract_resource_body_schema('logicalSwitchVmAttach', 'read')
client_session.view_body_dict(vm_attach_body_dict)

#vm_attach_body_dict['com.vmware.vshield.vsm.inventory.dto.VnicDto']['objectId'] = ''
#vm_attach_body_dict['com.vmware.vshield.vsm.inventory.dto.VnicDto']['portgroupId'] = new_ls['objectId']
#vm_attach_body_dict['com.vmware.vshield.vsm.inventory.dto.VnicDto']['vnicUuid'] = ''



