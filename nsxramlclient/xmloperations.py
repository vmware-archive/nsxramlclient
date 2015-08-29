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


import xml.dom.minidom as md
from collections import defaultdict
from lxml import etree as et


def pretty_xml(xml_string):
    return md.parseString(xml_string).toprettyxml()


# Thanks to K3---rnc for the great sample code used to convert XML to Dictionary in xml_to_dict
# http://stackoverflow.com/questions/7684333/converting-xml-to-dictionary-using-elementtree
def xml_to_dict(etree_object):
    return_dict = {etree_object.tag: {} if etree_object.attrib else None}
    children = list(etree_object)
    if children:
        dd = defaultdict(list)
        for dc in map(xml_to_dict, children):
            for k, v in dc.iteritems():
                dd[k].append(v)
        return_dict = {etree_object.tag: {k: v[0] if len(v) == 1 else v for k, v in dd.iteritems()}}
    if etree_object.attrib:
        return_dict[etree_object.tag].update(('@' + k, v) for k, v in etree_object.attrib.iteritems())
    if etree_object.text:
        text = etree_object.text.strip()
        if children or etree_object.attrib:
            if text:
                return_dict[etree_object.tag]['#text'] = text
        else:
            return_dict[etree_object.tag] = text
    return return_dict


def dict_to_xml(dict_to_parse):
    root_dict_key = [k for k in dict_to_parse][0]
    xml_root_object = et.Element(root_dict_key)
    parse_dict(xml_root_object, dict_to_parse[root_dict_key])
    xml_document = et.tostring(xml_root_object)
    return xml_document


def parse_dict(xml_root_object, dict_to_parse):
    for subitem in dict_to_parse.items():
        # subitem is now a tuple of key, value in the dict
        xml_subitem_name = subitem[0]
        if type(subitem[1]) in (str, int, None):
            if subitem[0][0] == '@':
                xml_root_object.set(subitem[0][1:], str(subitem[1]))
            else:
                xml_subitem = et.SubElement(xml_root_object, xml_subitem_name)
                xml_subitem.text = str(subitem[1])
        elif type(subitem[1]) is dict:
            xml_subitem = et.SubElement(xml_root_object, xml_subitem_name)
            parse_dict(xml_subitem, subitem[1])
        elif type(subitem[1]) is list:
            for embededdict in subitem[1]:
                if embededdict:
                    xml_subitem = et.SubElement(xml_root_object, xml_subitem_name)
                    parse_dict(xml_subitem, embededdict)
