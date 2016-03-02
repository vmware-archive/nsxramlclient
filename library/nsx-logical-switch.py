from nsxramlclient.client import NsxClient
from tabulate import tabulate
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
    return logical_switch_id

def _logical_switch_create(client_session, **kwargs):
    transport_zone = kwargs['transport_zone']
    logical_switch_name = kwargs['logical_switch_name']
    print 'Logical Switch {} has the ID {}'.format(logical_switch_name,
                                                    logical_switch_create(client_session,
                                                                          transport_zone,
                                                                          logical_switch_name))

def logical_switch_delete(client_session, logical_switch_name):
    # Find Logical Switch ID
    # TODO works only for the first 20 LS
    all_lswitches = client_session.read('logicalSwitchesGlobal', 'read')['body']['virtualWires']['dataPage']
    all_switches_dict_list = [scope_dict for scope_dict in all_lswitches['virtualWire']]
    try:
        logical_switch_id = [scope['objectId'] for scope in all_switches_dict_list if
                             scope['name'] == logical_switch_name][0]
    except IndexError:
        return False, None
 # Delete the LS
    client_session.delete('logicalSwitch', uri_parameters={'virtualWireID': logical_switch_id})
    return True, logical_switch_id

def _logical_switch_delete (client_session, **kwargs):
    logical_switch_name = kwargs['logical_switch_name']
    result = logical_switch_delete(client_session, logical_switch_name)
    if result[0]:
        print 'Logical Switch {} with the ID {} has been deleted'.format (logical_switch_name, result[1])
    else:
        print 'Logical Switch deletion failed'

def logical_switch_read (client_session, logical_switch_name):
    # Find Logical Switch ID
    # TODO works only for the first 20 LS
    all_lswitches = client_session.read('logicalSwitchesGlobal', 'read')['body']['virtualWires']['dataPage']
    all_switches_dict_list = [scope_dict for scope_dict in all_lswitches['virtualWire']]
    try:
        logical_switch_id = [scope['objectId'] for scope in all_switches_dict_list if
                             scope['name'] == logical_switch_name][0]
    except IndexError:
        return None
    return logical_switch_id

def _logical_switch_read (client_session, **kwargs):
    logical_switch_name = kwargs['logical_switch_name']
    result = logical_switch_read(client_session, logical_switch_name)
    if result:
        print 'Logical Switch {} has the ID {}'.format(logical_switch_name, result)
    else:
        print 'Logical Switch {} not found'.format(logical_switch_name)

def logical_switch_list (client_session):
    # Find Logical Switch ID
    # TODO works only for the first 20 LS
    all_lswitches = client_session.read('logicalSwitchesGlobal', 'read')['body']['virtualWires']['dataPage']
    all_switches_dict_list = [scope_dict for scope_dict in all_lswitches['virtualWire']]
    switch_list = []
    for scope in all_switches_dict_list:
        switch_list.append((scope['name'],scope['objectId']))
    return switch_list

def _logical_switch_list_print(client_session, **kwargs):
    print tabulate(logical_switch_list (client_session), headers=["LS name","LS ID"],tablefmt="psql")

def main():
    parser = argparse.ArgumentParser(description="nsxv function for logical switch '%(prog)s @params.conf'.",
                                     fromfile_prefix_chars='@')
    parser.add_argument("command", help="create: create a new logical switch"
                                        "read: return the virtual wire id of a logical switch"
                                        "delete: delete a logical switch"
                                        "list: return a list of all logical switches")
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
    client_session = NsxClient(config.get('nsxraml', 'nsxraml_file'), config.get('nsxv', 'nsx_manager'),
                        config.get('nsxv', 'nsx_username'), config.get('nsxv', 'nsx_password'), debug=debug)

    try:
        command_selector = {
            'list': _logical_switch_list_print,
            'create': _logical_switch_create,
            'delete': _logical_switch_delete,
            'read': _logical_switch_read,
            }
        command_selector[args.command](client_session, transport_zone=transport_zone, logical_switch_name=args.name)
    except KeyError:
        print('Unknown command')
        parser.print_help()

if __name__ == "__main__":
    main()
