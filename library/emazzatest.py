from nsxramlclient.client import NsxClient
import argparse
import ConfigParser


def logical_switch_create(client_session, transport_zone, logical_switch_name, control_plane_mode='UNICAST_MODE'):
    # find the objectId of the Scope with the name of the Transport Zone
    vdn_scopes = client_session.read('vdnScopes', 'read')['body']
    vdn_scope_dict_list = [scope_dict for scope_dict in vdn_scopes['vdnScopes'].items()]
    vdn_scope = [scope[1]['objectId'] for scope in vdn_scope_dict_list if scope[1]['name'] == transport_zone][0]

    # get a template dict for the lswitch create
    lswitch_create_dict = client_session.extract_resource_body_schema('logicalSwitches', 'create')
    # client_session.view_body_dict(lswitch_create_dict)

    # fill the details for the new lswitch in the body dict
    lswitch_create_dict['virtualWireCreateSpec']['controlPlaneMode'] = control_plane_mode
    lswitch_create_dict['virtualWireCreateSpec']['name'] = logical_switch_name
    lswitch_create_dict['virtualWireCreateSpec']['tenantId'] = ''

    # create new lswitch
    new_ls = client_session.create('logicalSwitches', uri_parameters={'scopeId': vdn_scope},
                                   request_body_dict=lswitch_create_dict)
    # client_session.view_response(new_ls)
    logical_switch_id = new_ls['objectId']
    print "Logical Switch %s has the ID %s." % (logical_switch_name, logical_switch_id)
    return logical_switch_id

def logical_switch_delete (client_session, logical_switch_name):
    # Find Logical Switch ID
    # TODO works only for the first 20 LS
    all_lswitches = client_session.read('logicalSwitchesGlobal', 'read')['body']['virtualWires']['dataPage']
    all_switches_dict_list = [scope_dict for scope_dict in all_lswitches['virtualWire']]
    logical_switch_id = [scope['objectId'] for scope in all_switches_dict_list if scope['name'] == logical_switch_name][0]

 # Delete the LS
    client_session.delete('logicalSwitch', uri_parameters={'virtualWireID': logical_switch_id})
    print "Logical Switch %s with the ID %s has been deleted." % (logical_switch_name, logical_switch_id)
    return True

def logical_switch_read (client_session, logical_switch_name):
    # Find Logical Switch ID
    # TODO works only for the first 20 LS
    all_lswitches = client_session.read('logicalSwitchesGlobal', 'read')['body']['virtualWires']['dataPage']
    all_switches_dict_list = [scope_dict for scope_dict in all_lswitches['virtualWire']]
    logical_switch_id = [scope['objectId'] for scope in all_switches_dict_list if scope['name'] == logical_switch_name][0]

 # Read the LS
    print "Logical Switch %s has the ID %s." % (logical_switch_name, logical_switch_id)
    return logical_switch_id

def logical_switch_list (client_session):
    # Find Logical Switch ID
    # TODO works only for the first 20 LS
    all_lswitches = client_session.read('logicalSwitchesGlobal', 'read')['body']['virtualWires']['dataPage']
    all_switches_dict_list = [scope_dict for scope_dict in all_lswitches['virtualWire']]
    logical_switch_id = [scope['objectId'] for scope in all_switches_dict_list if scope['name'] == logical_switch_name][0]
    logical_switch_name = [scope['objectId'] for scope in all_switches_dict_list if scope['name'] == logical_switch_name][0]

def main():
    parser = argparse.ArgumentParser(description="nsxv function for logical switch '%(prog)s @params.conf'.",
                                     fromfile_prefix_chars='@')
    parser.add_argument("-i",
                        "--ini",
                        help="nsx configuration file",
                        default="nsx.ini")
    parser.add_argument("-v",
                        "--verbose",
                        help="increase output verbosity",
                        action="store_true")
    parser.add_argument("-t",
                        "--transport_zone",
                        help="nsx transport zone")
    parser.add_argument("-n",
                        "--name",
                        help="logical switch name")
    args = parser.parse_args()

    if args.verbose:
        debug = True
    else:
        debug = False

    config = ConfigParser.ConfigParser()
    config.read(args.ini)

    if args.transport_zone:
        transport_zone = args.transport_zone
    else:
        transport_zone = config.get('defaults', 'transport_zone')

    # print ('test "{}"'.format(transport_zone))
    session = NsxClient(config.get('nsxraml', 'nsxraml_file'), config.get('nsxv', 'nsx_manager'),
                        config.get('nsxv', 'nsx_username'), config.get('nsxv', 'nsx_password'), debug=debug)

    logical_switch_create(session, transport_zone, args.name)


if __name__ == "__main__":
    main()
