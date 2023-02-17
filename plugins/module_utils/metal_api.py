#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from typing import List, Union, Optional, Callable
import inspect

from ansible_collections.equinix.cloud.plugins.module_utils import (
    metal_client,
    metal_api_routes,
    utils,
)


def optional(key: str):
    return lambda resource: utils.dict_get(resource, key)


def find_metro(resource):
    m = utils.dict_get(resource, 'metro.code')
    if m is not None:
        return m
    m = utils.dict_get(resource, 'facility.metro.code')
    return m


def optional_str(key: str):
    return lambda resource: resource.get(key, '')


def optional_bool(key: str):
    return lambda resource: resource.get(key, False)


def optional_float(key: str):
    return lambda resource: resource.get(key, 0.0)


def cidr_to_quantity(key: str):
    return lambda resource: 2 ** (32 - resource.get(key))


def ip_address_getter(resource: dict):
    pick_keys = ['address', 'address_family', 'public']
    return [dict((k, ip[k]) for k in pick_keys) for ip in resource.get('ip_addresses', [])]


# Following are the mappings of the API response attributes to the
# Ansible module attributes. The values are either a string with the
# attribute name or a function which takes the resource dict and returns
# the value for the module attribute.

METAL_DEVICE_RESPONSE_ATTRIBUTE_MAP = {
    'id': 'id',
    'project_id': 'project.id',
    'facility': 'facility.code',
    'metro': 'metro.code',
    'always_pxe': 'always_pxe',
    'billing_cycle': 'billing_cycle',
    'customdata': 'customdata',
    'hardware_reservation_id': optional_str('hardware_reservation_id'),
    'hostname': 'hostname',
    'ip_addresses': ip_address_getter,
    'ipxe_script_url': optional_str('ipxe_script_url'),
    'locked': 'locked',
    'metal_state': optional_str('state'),
    'tags': 'tags',
    'operating_system': 'operating_system.slug',
    'plan': 'plan.slug',
    'spot_instance': optional_bool('spot_instance'),
    'spot_price_max': optional_float('spot_price_max'),
    'ssh_keys': 'ssh_keys',
    'userdata': 'userdata',
    'ssh_keys': 'ssh_keys',
}

METAL_PROJECT_RESPONSE_ATTRIBUTE_MAP = {
    'id': 'id',
    'name': 'name',
    'description': optional_str('description'),
    'organization_id': 'organization.id',
    'payment_method_id': 'payment_method.id',
    'customdata': 'customdata',
    'backend_transfer_enabled': 'backend_transfer_enabled',
}

METAL_IP_RESERVATION_RESPONSE_ATTRIBUTE_MAP = {
    'id': 'id',
    'customdata': 'customdata',
    'metro': find_metro,
    'project_id': 'project.id',
    'quantity': 'quantity',
    'type': 'type',
    'address_family': 'address_family',
    'public': 'public',
    'management': 'management',
    'network': 'network',
    'netmask': 'netmask',
    'quantity': cidr_to_quantity('cidr'),
    'details': 'details',
    'tags': 'tags',
}

LIST_KEYS = ['projects', 'devices', 'ip_addresses']


def get_assignment_address(resource: dict):
    addr = resource.get('address')
    cidr = resource.get('cidr')
    return "{0}/{1}".format(addr, cidr)


METAL_IP_ASSIGNMENT_RESPONSE_ATTRIBUTE_MAP = {
    'id': 'id',
    'customdata': 'customdata',
    'management': 'management',
    'address': get_assignment_address,
}


def get_attribute_mapper(resource_type):
    """
    Returns attribute mapper for the given resource type.
    """
    device_resources = set(['metal_device', 'metal_device_metro',
                            'metal_project_device', 'metal_device_facility'])
    project_resources = set(['metal_project', 'metal_organization_project'])
    ip_resources = set(['metal_ip_reservation'])
    if resource_type in device_resources:
        return METAL_DEVICE_RESPONSE_ATTRIBUTE_MAP
    elif resource_type in project_resources:
        return METAL_PROJECT_RESPONSE_ATTRIBUTE_MAP
    elif resource_type in ip_resources:
        return METAL_IP_RESERVATION_RESPONSE_ATTRIBUTE_MAP
    else:
        raise NotImplementedError("No mapper for resource type %s" % resource_type)


def call(resource_type, action, client, metal_python_client, body_params={}, url_params={}):
    """
    This function wraps the API call and returns the response.
    """
    metal_client.raise_if_missing_equinixmetalpy()
    conf = metal_api_routes.get_configs(metal_python_client).get((resource_type, action))
    if conf is None:
        raise NotImplementedError("No API call for resource type %s and action %s" % (resource_type, action))

    import q
    q(conf)
    if type(conf) is utils.MPSpecs:
        q("MPApiCall")
        united_params = {**body_params, **url_params}
        call = MPApiCall(conf, united_params)
        q(call.describe())
        response = call.do()
    else:
        q("Old ApiCall")
        call = ApiCall(conf, client, body_params, url_params)
        response = call.do()
        metal_client.raise_if_error(response, call.describe())
    # explore response here
    if response is not None:
        import q
        q(action, resource_type)
        # q(response.serialize())
        # q(response.additional_properties)

    if action == action.DELETE:
        return None
    attribute_mapper = get_attribute_mapper(resource_type)
    if action == action.LIST:
        return [response_to_ansible_dict(r, attribute_mapper)
                for r in find_list_in_response(response)]
    return response_to_ansible_dict(response, attribute_mapper)


def find_list_in_response(response):
    for k in LIST_KEYS:
        if hasattr(response, k):
            return getattr(response, k)


def href_to_id(href):
    return href.split('/')[-1]


def add_id_from_href(v):
    if ('href' in v) & ('id' not in v):
        v['id'] = href_to_id(v['href'])


def populate_ids_from_hrefs(response):
    if "as_dict" in dir(response):
        return_dict = response.as_dict()
    elif "to_dict" in dir(response):
        return_dict = response.to_dict()
    else:
        raise NotImplementedError("No as_dict or to_dict method for response object")
    if return_dict == {}:
        return_dict = response.additional_properties.copy()

    for v in return_dict.values():
        if type(v) is dict:
            if ('href' in v) & ('id' not in v):
                add_id_from_href(v)
        if type(v) is list:
            for i in v:
                if type(i) is dict:
                    add_id_from_href(i)
    return return_dict


def get_dotted_value(_dict, key):
    keys = key.split(".")
    for k in keys:
        if k in _dict:
            if _dict[k] is None:
                return None
            _dict = _dict[k]
        else:
            return None
    return _dict


def response_to_ansible_dict(response, attribute_mapper):
    return_dict = {}
    if response is None:
        return {}
    response_dict = populate_ids_from_hrefs(response)
    if attribute_mapper is None:
        return response_dict()
    for k, v in attribute_mapper.items():
        # k is key in ansible module
        # v is key in API response dict
        # response_dict[v] is value in API response dict
        if callable(v):
            return_dict[k] = v(response_dict)
        elif "." in v:
            dv = get_dotted_value(response_dict, v)
            if dv is None:
                raise Exception("attribute '{0}' (to map to '{1}') not found in response_dict: {2}".format(v, k, response_dict))
            return_dict[k] = dv
        elif k in response_dict:
            return_dict[k] = response_dict[v]
        else:
            raise Exception("attribute '{0}' (to map to '{1}') not found in response_dict: {2}".format(k, v, response_dict))
    return return_dict


class ApiCall(object):
    """
    A class representing an API call. It holds the configuration of the
    API call (ApiCallConfig) and the module parameters which are parsed
    into URL params and body params.

    API call body (if necessary) is created from the module parameters.
    """

    def __init__(self,
                 conf: utils.Specs,
                 client,
                 body_params: Optional[dict] = {},
                 url_params: Optional[dict] = {},
                 ):
        self.conf = conf
        self.client = client
        self.request_model_instance = None
        self.path_vars = []
        self.url_params = url_params
        if self.conf.params_parser:
            self.path_vars, body_params = self.conf.params_parser.parse(body_params)
        relevant_body_params = {k: v for k, v in body_params.items() if k not in utils.SKIPPED_PARAMS}
        if self.conf.request_model_class is not None:
            self.request_model_instance = self.conf.request_model_class.from_dict(
                relevant_body_params)

    def do(self):
        arg_list = self.path_vars
        if type(self.conf) is utils.Specs:
            arg_list = [self.client] + self.path_vars
        if self.request_model_instance is not None:
            arg_list.append(self.request_model_instance)
        #_D('arg_list: {0}'.format(arg_list))
        import q
        q(arg_list)
        result = self.conf.func(*arg_list, params=self.url_params)
        return result

    def describe(self):
        return "{0} to {1}".format(self.conf.func.__name__, self.path_vars)


class MPApiCall(object):
    """
    A class representing an API call. It holds the configuration of the
    API call (ApiCallConfig) and the module parameters which are parsed
    into URL params and body params.

    API call body (if necessary) is created from the module parameters.
    """

    def __init__(self,
                 conf: utils.MPSpecs,
                 params: Optional[dict] = {},
                 ):
        # make sure that only relevant params go to request model.
        # PROBLEM: name in project list - neopouzivas se to, ani to neni vygenerovane
        self.conf = conf
        passed_params = set(params.keys())
        self.sdk_kwargs = self.conf.params_parser.parse(params)
        unused_params = passed_params - set(self.sdk_kwargs.keys()) - set(utils.SKIPPED_PARAMS)
        self.path_kwargs = self.sdk_kwargs.copy()
        if self.conf.request_model_class is not None:
            body_params = {k: v for k, v in params.items() if k not in utils.SKIPPED_PARAMS}
            unused_params = unused_params - set(body_params.keys())
            request_model_instance = self.conf.request_model_class.from_dict(body_params)
            self.sdk_kwargs[self.conf.request_model_arg] = request_model_instance
        if unused_params:
            raise Exception("Unused params: {0}".format(unused_params))

    def do(self):
        result = self.conf.func(**self.sdk_kwargs)
        return result

    def describe(self):
        return "{0} to {1}".format(self.conf.func.__name__, self.path_kwargs)
