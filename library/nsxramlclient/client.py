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

import re
import pprint

import pyraml.parser
from lxml import etree as et

import http_session
import xmloperations


class NsxClient(object):
    def __init__(self, raml_file, nsxmanager, nsx_username, nsx_password, debug=None, verify=None,
                 suppress_warnings=None):
        """
        :param raml_file: This mandatory parameter is a RAML File used as the basis of all URL compossitions and
                          to extract body schemas and convert them into python dictionaries
        :param nsxmanager: This mandatory parameter is either the hostname or IP Address of the NSX Manager
        :param nsx_username: This mandatory parameter is the Username on NSX Manager used to do API Calls
        :param nsx_password: This mandatory parameter is the Password of the User used to do API Calls
        :param debug: Optional: If set to True, the client will print extensive HTTP session information to stdout.
               Default: False
        :param verify: Optional: If set to True, the client will strictly verify the certificate passed by NSX Manager.
               Default: False
        :param suppress_warnings: Optional: If set to True, the client will print out a warning if NSX Manager uses
               a self signed certificate. Default: True
        :return: Returns a NsxClient Session Object
        """
        self._nsx_raml_file = raml_file
        self._nsxraml = NsxRaml(self._nsx_raml_file, nsxmanager)
        self._nsx_username = nsx_username
        self._nsx_password = nsx_password
        self._debug = debug
        self._verify = verify
        if suppress_warnings:
            self._suppress_warnings = suppress_warnings
        else:
            self._suppress_warnings = True
        self._httpsession = http_session.Session(self._nsx_username, self._nsx_password, self._debug, self._verify,
                                                 self._suppress_warnings)

    def read(self, searched_resource, uri_parameters=None, request_body_dict=None, query_parameters_dict=None,
             additional_headers=None):
        """
        This method is used to read a resource using the GET HTTP Method
        :param searched_resource: A valid display name in the RAML file matching the resource
        :param uri_parameters: A dictionary with the URI Parameters expected by the resource
        :param request_body_dict: A dictionary containing the body parameter in the format
               {'baseObject': {nested parameters}}. You can use extract_resource_body_schema to create it
        :param query_parameters_dict: A dictionary containing optional or mandatory query parameters
        :param additional_headers: a dictionary of additional Headers to send in your request, e.g. if-match used
               with the dfw calls
        :return: This method returns a dictionary containing the received header and body data
        """
        return self._request(searched_resource, 'get', uri_parameters, request_body_dict, query_parameters_dict,
                             additional_headers)

    def create(self, searched_resource, uri_parameters=None, request_body_dict=None, query_parameters_dict=None,
               additional_headers=None):
        """
        This method is used to create a resource using the POST HTTP Method
        :param searched_resource: A valid display name in the RAML file matching the resource
        :param uri_parameters: A dictionary with the URI Parameters expected by the resource
        :param request_body_dict: A dictionary containing the body parameter in the format
               {'baseObject': {nested parameters}}. You can use extract_resource_body_schema to create it
        :param query_parameters_dict: A dictionary containing optional or mandatory query parameters
        :param additional_headers: a dictionary of additional Headers to send in your request, e.g. if-match used
               with the dfw calls
        :return: This method returns a dictionary containing the received header and body data
        NOTE: The _resource_url and _request_body are constructed and passed by the decorator function
        """
        return self._request(searched_resource, 'post', uri_parameters, request_body_dict, query_parameters_dict,
                             additional_headers)

    def update(self, searched_resource, uri_parameters=None, request_body_dict=None, query_parameters_dict=None,
               additional_headers=None):
        """
        This method is used to update a resource using the PUT HTTP Method
        :param searched_resource: A valid display name in the RAML file matching the resource
        :param uri_parameters: A dictionary with the URI Parameters expected by the resource
        :param request_body_dict: A dictionary containing the body parameter in the format
               {'baseObject': {nested parameters}}. You can use extract_resource_body_schema to create it
        :param query_parameters_dict: A dictionary containing optional or mandatory query parameters
        :param additional_headers: a dictionary of additional Headers to send in your request, e.g. if-match used
               with the dfw calls
        :return: This method returns a dictionary containing the received header and body data
        NOTE: The _resource_url and _request_body are constructed and passed by the decorator function
        """
        return self._request(searched_resource, 'put', uri_parameters, request_body_dict, query_parameters_dict,
                             additional_headers)

    def delete(self, searched_resource, uri_parameters=None, request_body_dict=None, query_parameters_dict=None,
               additional_headers=None):
        """
        This method is used to delete a resource using the DELETE HTTP Method
        :param searched_resource: A valid display name in the RAML file matching the resource
        :param uri_parameters: A dictionary with the URI Parameters expected by the resource
        :param request_body_dict: A dictionary containing the body parameter in the format
               {'baseObject': {nested parameters}}. You can use extract_resource_body_schema to create it
        :param query_parameters_dict: A dictionary containing optional or mandatory query parameters
        :param additional_headers: a dictionary of additional Headers to send in your request, e.g. if-match used
               with the dfw calls
        :return: This method returns a dictionary containing the received header and body data
        NOTE: The _resource_url and _request_body are constructed and passed by the decorator function
        """
        return self._request(searched_resource, 'delete', uri_parameters, request_body_dict, query_parameters_dict,
                             additional_headers)

    def _request(self, searched_resource, method, uri_parameters=None, request_body_dict=None,
                 query_parameters_dict=None, additional_headers=None):
        found_res_object = self._nsxraml.find_resource_recursively(searched_resource)
        assert found_res_object, 'The searched displayName could not be found in RAML File'

        self._nsxraml.check_resource_methods_by_displayname(searched_resource, method)
        resource_url = self._nsxraml.contruct_resource_url(searched_resource, uri_parameters)
        query_parameters = self._nsxraml.get_method_mandatory_query_parameters(searched_resource, method)

        if request_body_dict:
            request_body = xmloperations.dict_to_xml(request_body_dict)
        else:
            request_body = None

        if query_parameters_dict:
            resource_url = self._nsxraml.add_query_parameter_url(resource_url, searched_resource, method,
                                                                 query_parameters_dict)
        else:
            assert not query_parameters, 'missing mandatory query parameter {}'.format(query_parameters)

        mandatory_add_headers = self._nsxraml.get_method_mandatory_add_headers(searched_resource, method)

        if additional_headers:
            assert set(mandatory_add_headers).issubset(set(additional_headers.keys())), \
                'missing mandatory additonal headers {}'.format(mandatory_add_headers)
            headers = additional_headers
        else:
            assert mandatory_add_headers is None, 'missing mandatory additonal headers {}'.format(mandatory_add_headers)
            headers = None

        response = self._httpsession.do_request(method, resource_url, data=request_body, headers=headers)

        # TODO: Add a check for mandatory body attributes (if needed)

        return response

    def view_resource_body_schema(self, searched_resource, method):
        xml_schema_result = self._nsxraml.get_xml_schema_by_displayname(searched_resource, method)
        print et.tostring(xml_schema_result, pretty_print=True)

    def extract_resource_body_schema(self, searched_resource, method):
        xml_schema_result = self._nsxraml.get_xml_schema_by_displayname(searched_resource, method)
        return xmloperations.xml_to_dict(xml_schema_result)

    @staticmethod
    def view_response(ordered_dict):
        pretty_printer = pprint.PrettyPrinter()
        print 'HTTP status code:\n{}\n'.format(ordered_dict['status'])
        if ordered_dict['location']:
            print 'HTTP location header:\n{}\n'.format(ordered_dict['location'])
        if ordered_dict['objectId']:
            print 'NSX Object Id:\n{}\n'.format(ordered_dict['objectId'])
        if ordered_dict['Etag']:
            print 'Etag Header:\n{}\n'.format(ordered_dict['Etag'])
        if ordered_dict['body']:
            print 'HTTP Body Content:'
            pretty_printer.pprint(ordered_dict['body'])

    @staticmethod
    def view_body_dict(body_dict):
        pretty_printer = pprint.PrettyPrinter()
        pretty_printer.pprint(body_dict)

    def view_resource_display_names(self):
        output_text = []
        for display_name, details in sorted(self._nsxraml.list_all_resources().items()):
            output_text.append('Displayname:     {}\nDescription:     {}\nSupports:        {}\n'.format(display_name,
                                                                                                        details[0],
                                                                                                        details[1]))
            if details[2]:
                output_text.append('uriParameters:   {}\n'.format(details[2]))
            if details[3]:
                output_text.append('queryParameters: {}\n'.format(details[3]))
            if details[4]:
                output_text.append('Add. Headers:    {}\n'.format(details[4]))

            output_text.append('\n')

        print ''.join(output_text)

    def read_all_pages(self, searched_resource, uri_parameters=None, request_body_dict=None,
                       query_parameters_dict=None, additional_headers=None):
        supported_objects = ['virtualWires']
        first_page = self._request(searched_resource, 'get', uri_parameters, request_body_dict, query_parameters_dict,
                                   additional_headers)['body']
        first_key = first_page.keys()[0]
        assert first_key in supported_objects, 'unsupported object {}, currently only {} ' \
                                               'are supported'.format(first_key, supported_objects)
        if first_key == 'virtualWires':
            paging_info = first_page['virtualWires']['dataPage']['pagingInfo']
            total_count = int(paging_info['totalCount'])
            page_size = int(paging_info['pageSize'])
            start_index = int(paging_info['startIndex'])
            if not query_parameters_dict:
                query_parameters_dict = {'pagesize': paging_info['pageSize'], 'startindex': paging_info['startIndex']}
            if total_count == 0:
                return []
            elif total_count == 1:
                return [first_page['virtualWires']['dataPage']['virtualWire']]
            elif page_size >= total_count:
                return first_page['virtualWires']['dataPage']['virtualWire']

            collected_values = first_page['virtualWires']['dataPage']['virtualWire']
            for page_start_index in range(start_index+page_size, total_count, page_size):
                query_parameters_dict['startindex'] = str(page_start_index)
                sub_page = self._request(searched_resource, 'get', uri_parameters, request_body_dict,
                                         query_parameters_dict, additional_headers)['body']
                if isinstance(sub_page['virtualWires']['dataPage']['virtualWire'], dict):
                    collected_values.append(sub_page['virtualWires']['dataPage']['virtualWire'])
                if isinstance(sub_page['virtualWires']['dataPage']['virtualWire'], list):
                    collected_values.extend(sub_page['virtualWires']['dataPage']['virtualWire'])

            return collected_values

    @staticmethod
    def normalize_list_return(input_object):
        if not input_object:
            return []
        elif isinstance(input_object, dict):
            return [input_object]
        elif isinstance(input_object, list):
            return input_object
        else:
            return []


class NsxRaml(object):
    def __init__(self, raml_file, nsxmanager):
        self._nsxraml = pyraml.parser.load(raml_file)
        self._base_uri = re.sub('\{nsxmanager\}', nsxmanager, self._nsxraml.baseUri)

    def find_resource_recursively(self, display_name, raml_resource_root=None):
        # this method runs through the base raml file recursively until it finds the first
        # occurrence of the searched displayName in the resource
        if raml_resource_root:
            searched_tuples = raml_resource_root.resources.items()
        else:
            searched_tuples = self._nsxraml.resources.items()

        for resource_tuple in searched_tuples:
            if resource_tuple[1].displayName == str(display_name):
                return resource_tuple
            elif resource_tuple[1].resources:
                recursive_result = self.find_resource_recursively(display_name, raml_resource_root=resource_tuple[1])
                if recursive_result:
                    return recursive_result

    def contruct_resource_url(self, display_name, uri_parameters):
        found_resource = self.find_resource_recursively(display_name)
        resource_url_data = self._get_resource_url_data(found_resource)
        resource_url = self._base_uri + resource_url_data['constructed_url']

        if len(resource_url_data['uri_parameters']) > 0:
            assert uri_parameters, 'The resource requires dict uri_parameters to be passed as kwarg'
            try:
                resource_uri_params = [uri_parameter for uri_parameter in uri_parameters
                                       if resource_url_data['uri_parameters'][uri_parameter].required]
            except KeyError:
                raise Exception('one of the passed URI parameter could not be found in RAMl File')

            for uri_parameter in resource_uri_params:
                assert uri_parameter in uri_parameters.keys(), \
                    'one required URI parameter is missing in the passed URI parameters, ' \
                    'required parameters are {}'.format(resource_uri_params)
                resource_url = re.sub('\{' + uri_parameter + '\}', uri_parameters[uri_parameter], resource_url)

        return resource_url

    def _get_resource_url_data(self, resource, res_url_data=None):
        # this method runs through the base raml file backwards recursively to construct the
        # url of the resource and collect all uri parameters back to the root
        if not res_url_data:
            res_url_data = {'constructed_url': '', 'uri_parameters': {}, 'query_parameters': {}}
        if resource[1].parentResource:
            try:
                resource[1].parentResource.displayName
            except:
                raise Exception('The parent resource of {} is missing a display '
                                'name in the RAMl File'.format(resource[0]))
            parent_display_name = resource[1].parentResource.displayName
            parent_resource = self.find_resource_recursively(parent_display_name, self._nsxraml)
            res_url_data['constructed_url'] = resource[0] + res_url_data['constructed_url']
            if resource[1].uriParameters:
                res_url_data['uri_parameters'].update(resource[1].uriParameters)
            return self._get_resource_url_data(parent_resource, res_url_data)
        else:
            res_url_data['constructed_url'] = resource[0] + res_url_data['constructed_url']
            if resource[1].uriParameters:
                res_url_data['uri_parameters'].update(resource[1].uriParameters)
            return res_url_data

    def check_resource_methods_by_displayname(self, display_name, method):
        found_res_object = self.find_resource_recursively(display_name)
        assert method in found_res_object[1].methods, 'The resource does not have a {} method in the ' \
                                                      'RAML File'.format(method.upper())

    def get_method_mandatory_query_parameters(self, display_name, method):
        found_res_object = self.find_resource_recursively(display_name)
        if found_res_object[1].methods[method].queryParameters:
            return [parameter for parameter in found_res_object[1].methods[method].queryParameters.keys() if
                    found_res_object[1].methods[method].queryParameters[parameter].required]

    def get_method_mandatory_add_headers(self, display_name, method):
        found_res_object = self.find_resource_recursively(display_name)
        if found_res_object[1].methods[method].headers:
            return [header for header in found_res_object[1].methods[method].headers.keys() if
                    found_res_object[1].methods[method].headers[header].required]

    def add_query_parameter_url(self, url, display_name, method, query_parameters_dict):
        found_res_object = self.find_resource_recursively(display_name)
        mandatory_query_parameters = [parameter for parameter in
                                      found_res_object[1].methods[method].queryParameters.keys() if
                                      found_res_object[1].methods[method].queryParameters[parameter].required]
        missing_mandatory_qparameters = [parameter for parameter in mandatory_query_parameters if
                                         parameter not in query_parameters_dict.keys()]
        assert len(missing_mandatory_qparameters) == 0, 'Missing required query ' \
                                                        'parameters : {}'.format(missing_mandatory_qparameters)

        url = '{}?'.format(url)
        for query_parameter in query_parameters_dict.keys():
            url = '{}&{}={}'.format(url, query_parameter, query_parameters_dict[query_parameter])
        return url

    def get_xml_schema_by_displayname(self, display_name, method):
        method_options = {'read': 'get', 'create': 'post', 'delete': 'delete', 'update': 'put'}
        matched_resource = self.find_resource_recursively(display_name)

        assert matched_resource, 'The searched displayName could not be found in RAML File'
        assert method_options[method] in matched_resource[1].methods, 'the resource does not support ' \
                                                                      'the {} method'.format(method)
        assert matched_resource[1].methods[method_options[method]].body, 'the resource does not have a ' \
                                                                         'body schema in the RAML File'

        matched_resource_body = matched_resource[1].methods[method_options[method]].body

        base_et_element = type(et.Element('base'))

        if isinstance(matched_resource_body['application/xml'].schema, base_et_element):
            return matched_resource_body['application/xml'].schema
        elif isinstance(matched_resource_body['application/xml'].schema, str):
            assert matched_resource_body['application/xml'].schema in self._nsxraml.schemas.keys(), \
                'the external schema {} could not be found in the schema list of the RAML File'.format(
                    matched_resource_body['application/xml'].schema)
            assert isinstance(self._nsxraml.schemas[matched_resource_body['application/xml'].schema],
                              base_et_element), 'the external schema {} is likely ' \
                                                'misformated'.format(matched_resource_body['application/xml'].schema)

            return self._nsxraml.schemas[matched_resource_body['application/xml'].schema]

    @staticmethod
    def _collect_resource_details(resource_tuple):
        method_options = {'read': 'get', 'create': 'post', 'delete': 'delete', 'update': 'put'}
        if resource_tuple[1].methods:
            supported_methods = [key for key in resource_tuple[1].methods]
            supported_operations = [operation[0] for operation in method_options.items()
                                    if operation[1] in supported_methods]
            method_items = [method_item for method_item in resource_tuple[1].methods.items()]

            try:
                query_parameters = [rmethod[1].queryParameters.keys() for rmethod in method_items if
                                    rmethod[1].queryParameters][0]
            except IndexError:
                query_parameters = None

            try:
                resource_add_headers = [rmethod[1].headers.keys() for rmethod in method_items if
                                        rmethod[1].headers][0]
            except IndexError:
                resource_add_headers = None

        else:
            supported_operations = None
            query_parameters = None
            resource_add_headers = None

        if resource_tuple[1].uriParameters:
            resource_uri_parameters = [uri_parameter for uri_parameter in resource_tuple[1].uriParameters]
        else:
            resource_uri_parameters = None

        return supported_operations, resource_uri_parameters, query_parameters, resource_add_headers

    def list_all_resources(self, raml_resource_root=None, display_names_dict=None):
        if display_names_dict is None:
            display_names_dict = {}

        if raml_resource_root:
            scanned_tuples = raml_resource_root.resources.items()
        else:
            scanned_tuples = self._nsxraml.resources.items()

        for resource_tuple in scanned_tuples:
            if resource_tuple[1].resources:
                resources_details = self._collect_resource_details(resource_tuple)
                display_names_dict[resource_tuple[1].displayName] = (resource_tuple[1].description,
                                                                     resources_details[0], resources_details[1],
                                                                     resources_details[2], resources_details[3])
                display_names_dict = self.list_all_resources(raml_resource_root=resource_tuple[1],
                                                             display_names_dict=display_names_dict)
            else:
                resources_details = self._collect_resource_details(resource_tuple)
                display_names_dict[resource_tuple[1].displayName] = (resource_tuple[1].description,
                                                                     resources_details[0], resources_details[1],
                                                                     resources_details[2], resources_details[3])

        return display_names_dict
