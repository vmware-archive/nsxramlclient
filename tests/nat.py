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


def configure_nat(session, edgeid='edge-1', oadd='10.112.196.116', tadd='172.16.1.10', oport=3389, tport=3389):
    nat_spec = session.extract_resource_body_example('edgeNat', 'update')

    nat_spec['nat']['natRules']['natRule']['ruleTag'] = 65538
    nat_spec['nat']['natRules']['natRule']['action'] = 'dnat'
    nat_spec['nat']['natRules']['natRule']['vnic'] = 0
    nat_spec['nat']['natRules']['natRule']['originalAddress'] = oadd
    nat_spec['nat']['natRules']['natRule']['translatedAddress'] = tadd
    nat_spec['nat']['natRules']['natRule']['loggingEnabled'] = 'true'
    nat_spec['nat']['natRules']['natRule']['enabled'] = 'true'
    nat_spec['nat']['natRules']['natRule']['description'] = 'Created with RAML'
    nat_spec['nat']['natRules']['natRule']['protocol'] = 'tcp'
    nat_spec['nat']['natRules']['natRule']['translatedPort'] = oport
    nat_spec['nat']['natRules']['natRule']['originalPort'] = tport

    create_response = session.update('edgeNat', uri_parameters={'edgeId': edgeid}, request_body_dict=nat_spec)

    session.view_response(create_response)


def append_nat(session, edgeid='edge-1', oadd='10.112.196.117', tadd='172.16.1.11', oport=3390, tport=3390):
    nat_spec = session.extract_resource_body_example('edgeNatRules', 'create')

    nat_spec['natRules']['natRule']['action'] = 'dnat'
    nat_spec['natRules']['natRule']['vnic'] = 0
    nat_spec['natRules']['natRule']['originalAddress'] = oadd
    nat_spec['natRules']['natRule']['translatedAddress'] = tadd
    nat_spec['natRules']['natRule']['loggingEnabled'] = 'true'
    nat_spec['natRules']['natRule']['enabled'] = 'true'
    nat_spec['natRules']['natRule']['description'] = 'Created with RAML'
    nat_spec['natRules']['natRule']['protocol'] = 'tcp'
    nat_spec['natRules']['natRule']['translatedPort'] = oport
    nat_spec['natRules']['natRule']['originalPort'] = tport

    create_response = session.create('edgeNatRules', uri_parameters={'edgeId': edgeid}, request_body_dict=nat_spec)

    session.view_response(create_response)


def update_nat(session, rule_id, edgeid='edge-1', oadd='10.112.196.118', tadd='172.16.1.12', oport=3391, tport=3391):
    nat_spec = session.extract_resource_body_example('edgeNatRule', 'update')

    nat_spec['natRule']['action'] = 'dnat'
    nat_spec['natRule']['vnic'] = 0
    nat_spec['natRule']['originalAddress'] = oadd
    nat_spec['natRule']['translatedAddress'] = tadd
    nat_spec['natRule']['loggingEnabled'] = 'true'
    nat_spec['natRule']['enabled'] = 'true'
    nat_spec['natRule']['description'] = 'Updated NAT config'
    nat_spec['natRule']['protocol'] = 'tcp'
    nat_spec['natRule']['translatedPort'] = oport
    nat_spec['natRule']['originalPort'] = tport

    create_response = session.update('edgeNatRule', uri_parameters={'edgeId': edgeid, 'ruleID': rule_id},
                                     request_body_dict=nat_spec)

    session.view_response(create_response)


def query_nat(session, edgeid='edge-1'):
    response = session.read('edgeNat', uri_parameters={'edgeId': edgeid})
    session.view_response(response)


def delete_nat(session, edgeid='edge-1'):
    del_response = session.delete('edgeNat', uri_parameters={'edgeId': edgeid})
    session.view_response(del_response)


def main():
    session = NsxClient(nsxraml_file, nsxmanager, nsx_username, nsx_password, debug=True)
    configure_nat(session)
    append_nat(session)
    query_nat(session)

    rule_id = raw_input('Enter RuleID as seen in above output: ')
    update_nat(session, rule_id)
    delete_nat(session)


if __name__ == "__main__":
    main()

