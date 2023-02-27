#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible_collections.equinix.cloud.plugins.module_utils import (
    utils,
)

from ansible_collections.equinix.cloud.plugins.module_utils.metal import (
    metal_client,
    api_routes,
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
    'always_pxe': 'always_pxe',
    'billing_cycle': 'billing_cycle',
    'customdata': 'customdata',
    'facility': 'facility.code',
    'hardware_reservation_id': optional_str('hardware_reservation_id'),
    'hostname': 'hostname',
    'id': 'id',
    'ip_addresses': ip_address_getter,
    'ipxe_script_url': optional_str('ipxe_script_url'),
    'locked': 'locked',
    'metal_state': optional_str('state'),
    'metro': 'metro.code',
    'operating_system': 'operating_system.slug',
    'plan': 'plan.slug',
    'project_id': 'project.id',
    'spot_instance': optional_bool('spot_instance'),
    'spot_price_max': optional_float('spot_price_max'),
    'ssh_keys': 'ssh_keys',
    'ssh_keys': 'ssh_keys',
    'tags': 'tags',
    'userdata': 'userdata',
}

METAL_PROJECT_RESPONSE_ATTRIBUTE_MAP = {
    'backend_transfer_enabled': 'backend_transfer_enabled',
    'customdata': 'customdata',
    'description': optional_str('description'),
    'id': 'id',
    'name': 'name',
    'organization_id': 'organization.id',
    'payment_method_id': 'payment_method.id',
}

METAL_IP_RESERVATION_RESPONSE_ATTRIBUTE_MAP = {
    'address_family': 'address_family',
    'customdata': 'customdata',
    'details': optional_str('details'),
    'id': 'id',
    'management': 'management',
    'metro': find_metro,
    'netmask': 'netmask',
    'network': 'network',
    'project_id': 'project.id',
    'public': 'public',
    'quantity': 'quantity',
    'quantity': cidr_to_quantity('cidr'),
    'tags': 'tags',
    'type': 'type',
}

LIST_KEYS = ['projects', 'devices', 'ip_addresses']


def get_assignment_address(resource: dict):
    addr = resource.get('address')
    cidr = resource.get('cidr')
    return "{0}/{1}".format(addr, cidr)


METAL_IP_ASSIGNMENT_RESPONSE_ATTRIBUTE_MAP = {
    'id': 'id',
    # 'customdata': 'customdata',
    'management': 'management',
    'address': get_assignment_address,
    'cidr': 'cidr',
    'address_family': 'address_family',
    'public': 'public',
    'network': 'network',
    'netmask': 'netmask',
    'device_id': 'assigned_to.id',
    'metro': find_metro,
}


def get_attribute_mapper(resource_type):
    """
    Returns attribute mapper for the given resource type.
    """
    device_resources = set(['metal_device', 'metal_project_device'])
    project_resources = set(['metal_project', 'metal_organization_project'])
    ip_reservation_resources = set(['metal_ip_reservation', 'metal_available_ip'])
    ip_assignment_resources = set(['metal_ip_assignment'])
    if resource_type in device_resources:
        return METAL_DEVICE_RESPONSE_ATTRIBUTE_MAP
    elif resource_type in project_resources:
        return METAL_PROJECT_RESPONSE_ATTRIBUTE_MAP
    elif resource_type in ip_reservation_resources:
        return METAL_IP_RESERVATION_RESPONSE_ATTRIBUTE_MAP
    elif resource_type in ip_assignment_resources:
        return METAL_IP_ASSIGNMENT_RESPONSE_ATTRIBUTE_MAP
    else:
        raise NotImplementedError("No mapper for resource type %s" % resource_type)


def call(resource_type, action, equinix_metal_client, params={}):
    """
    This function wraps the API call and returns the response.
    """
    metal_client.raise_if_missing_equinix_metal()
    conf = api_routes.get_routes(equinix_metal_client).get((resource_type, action))
    if conf is None:
        raise NotImplementedError("No API call for resource type %s and action %s" % (resource_type, action))

    import q
    q(conf)
    call = api_routes.build_api_call(conf, params)
    q(call.describe())
    response = call.do()
    if response is not None:
        import q
        q(action, resource_type, response.to_dict())

    if action == action.DELETE:
        return None
    attribute_mapper = get_attribute_mapper(resource_type)
    if action == action.LIST:
        if resource_type == 'metal_available_ip':
            return response.to_dict()['available']
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
    return_dict = response.to_dict()
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
