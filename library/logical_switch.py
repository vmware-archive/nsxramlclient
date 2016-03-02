from nsxramlclient.client import NsxClient
import time
import argparse
import ConfigParser

def logical_switch_create(client_session,transport_zone,logical_switch_name,control_plane_mode='UNICAST_MODE'):
    # find the objectId of the Scope with the name of the Transport Zone
    vdn_scopes = client_session.read('vdnScopes', 'read')['body']
    vdn_scope_dict_list = [scope_dict for scope_dict in vdn_scopes['vdnScopes'].items()]
    vdn_scope = [scope[1]['objectId'] for scope in vdn_scope_dict_list if scope[1]['name'] == transport_zone][0]

    # get a template dict for the lswitch create
    lswitch_create_dict = client_session.extract_resource_body_schema('logicalSwitches', 'create')
    #client_session.view_body_dict(lswitch_create_dict)

    # fill the details for the new lswitch in the body dict
    lswitch_create_dict['virtualWireCreateSpec']['controlPlaneMode'] = control_plane_mode
    lswitch_create_dict['virtualWireCreateSpec']['name'] = logical_switch_name
    lswitch_create_dict['virtualWireCreateSpec']['tenantId'] = ''

    # create new lswitch
    new_ls = client_session.create('logicalSwitches', uri_parameters={'scopeId': vdn_scope},
                                   request_body_dict=lswitch_create_dict)
    #client_session.view_response(new_ls)

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
        transport_zone = config.get('defaults','transport_zone')

    #print ('test "{}"'.format(transport_zone))
    session = NsxClient(config.get('nsxraml','nsxraml_file'), config.get('nsxv','nsx_manager'),
                        config.get('nsxv','nsx_username'), config.get('nsxv','nsx_password'), debug=debug)

    logical_switch_create(session,transport_zone,args.name)


if __name__ == "__main__":
    main()