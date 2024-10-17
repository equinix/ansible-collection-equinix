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

def ip_count_from_mask(mask: int):
    return 2 ** (32 - mask)

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


def optional_float(key: str, default=0.0):
    return lambda resource: resource.get(key, default)

def cidr_to_quantity(key: str):
    return lambda resource: ip_count_from_mask(resource.get(key))


def ip_address_getter(resource: dict):
    pick_keys = ['address', 'address_family', 'public']
    return [dict((k, ip[k]) for k in pick_keys) for ip in resource.get('ip_addresses', [])]

def network_ports_getter(resource: dict):
    ports = resource.get('network_ports')
    result = []
    for port in ports:
        actual_port = {'id': port.get('id', ''), 'name': port.get('name')}

        bond = port.get('bond', None)
        if bond:
            actual_port['bond'] = bond.get('id', '')

        network_type = port.get('network_type', None)
        if network_type:
            actual_port['network_type'] = network_type

        native_vlan = port.get('native_virtual_network', None)
        if native_vlan:
            actual_port['native_vlan'] = native_vlan.get('id', '')

        vlans = port.get('virtual_networks', [])
        if vlans:
            actual_port['vlans'] = []
            for vlan in vlans:
                actual_port['vlans'].append(vlan.get('id'))

        result.append(actual_port)

    return result


def extract_ids_from_projects_hrefs(resource: dict):
    return [href_to_id(p['href']) for p in resource.get('projects', [])]


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
    'network_ports': network_ports_getter,
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
    'payment_method_id': optional_str('payment_method.id'),
}

METAL_ORGANIZATION_RESPONSE_ATTRIBUTE_MAP = {
    'id': 'id',
    'name': 'name',
    'description': optional_str('description'),
    'website': optional_str('website'),
    'projects': extract_ids_from_projects_hrefs,
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
    'gateway': 'gateway',
    'project_id': 'project.id',
    'public': 'public',
    'quantity': cidr_to_quantity('cidr'),
    'tags': 'tags',
    'type': 'type',
}

METAL_HARDWARE_RESERVATION_RESPONSE_ATTRIBUTE_MAP = {
    'id': 'id',
    'project_id': 'project.id',
    'device_id': optional_str('device.id'),
    'provisionable': 'provisionable',
    'spare': 'spare',
    'switch_uuid': 'switch_uuid',
    'plan': 'plan.slug',
}

METAL_VRF_RESPONSE_ATTRIBUTE_MAP = {
    'id': 'id',
    'name': 'name',
    'metro': 'metro',
    'project_id': 'project.id',
    'description': optional_str('description'),
    'local_asn': 'local_asn',
    'ip_ranges': 'ip_ranges',
}

METAL_USER_RESPONSE_ATTRIBUTE_MAP = {
    'avatar_thumb_url': 'avatar_thumb_url',
    'avatar_url': 'avatar_url',
    'created_at': 'created_at',
    'customdata': 'customdata',
    'default_organization_id': 'default_organization_id',
    'email': 'email',
    'emails': 'emails',
    'first_name': 'first_name',
    'full_name': 'full_name',
    'href': 'href',
    'id': 'id',
    'last_login_at': 'last_login_at',
    'last_name': 'last_name',
    'max_projects': 'max_projects',
    'short_id': 'short_id',
    'timezone': 'timezone',
    'two_factor_auth': 'two_factor_auth',
    'updated_at': 'updated_at'
}

LIST_KEYS = [
    'projects',
    'devices',
    'ip_addresses',
    'ssh_keys',
    'metros',
    'operating_systems',
    'hardware_reservations',
    'organizations',
    'virtual_networks',
    'interconnections',
    'vrfs',
    'metal_gateways',
    'bgp_sessions',     # metal_bgp_session
    'sessions',         # metal_bgp_session_info
    'plans',
    'virtual_circuits',
    'users',
]


def get_assignment_address(resource: dict):
    addr = resource.get('address')
    cidr = resource.get('cidr')
    return "{0}/{1}".format(addr, cidr)


METAL_IP_ASSIGNMENT_RESPONSE_ATTRIBUTE_MAP = {
    'id': 'id',
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


METAL_SSH_KEY_RESPONSE_ATTRIBUTE_MAP = {
    'id': 'id',
    'label': 'label',
    'key': 'key',
    'fingerprint': 'fingerprint',
}


METAL_OPERATING_SYSTEM_RESPONSE_ATTRIBUTE_MAP = {
    'id': 'id',
    'distro': 'distro',
    'distro_label': 'distro_label',
    'licensed': 'licensed',
    'name': 'name',
    'preinstallable': 'preinstallable',
    'pricing': 'pricing',
    'provisionable_on': 'provisionable_on',
    'slug': 'slug',
    'version': 'version',
}


METAL_METRO_RESPONSE_ATTRIBUTE_MAP = {
    'id': 'id',
    'code': 'code',
    'name': 'name',
    'country': 'country',
}


VLAN_RESPONSE_ATTRIBUTE_MAP = {
    "id": "id",
    "description": optional_str('description'),
    "metro": optional("metro"),
    "facility": optional("facility"),
    "vxlan": "vxlan",
    "tags": "tags",
    "metal_gateways": "metal_gateways",
}

METAL_CONNECTION_RESPONSE_ATTRIBUTE_MAP = {
    'id': 'id',
    'name': 'name',
    'metro': 'metro',
    'contact_email': 'contact_email',
    'description': optional_str('description'),
    'mode': optional_str('mode'),
    'redundancy': 'redundancy',
    'tags': 'tags',
    'type': 'type',
    'ports': 'ports',
    'requested_by': 'requested_by',
    'status': 'status',
}

def private_ipv4_subnet_size(resource: dict):
    """
    Computes the private_ipv4_subnet_size from the ip_reservation.cidr field in the API response.
    Returns None if the ip_reservation is public.
    """
    ip_reservation = resource.get('ip_reservation')
    if ip_reservation is None:
        raise Exception("ip_reservation is not present in API response")
    is_public = ip_reservation.get('public')
    if is_public is None:
        raise Exception("'public' is not present in ip_reservation field in API response (maybe we need to explicitly include ip_reservation in request kwargs?)")
    if is_public:
        return None
    cidr = ip_reservation.get('cidr')
    if cidr is None:
        raise Exception("'cidr' is not present in ip_reservation field in API response (maybe we need to explicitly include ip_reservation through request kwargs?)")
    return ip_count_from_mask(cidr)


METAL_GATEWAY_RESPONSE_ATTRIBUTE_MAP = {
    'id': 'id',
    'ip_reservation_id': 'ip_reservation.id',
    'private_ipv4_subnet_size': private_ipv4_subnet_size,
    'virtual_network_id': 'virtual_network.id',
    'project_id': 'project.id',
    'metal_state': optional_str('state'),
}

METAL_BGP_SESSION_RESPONSE_ATTRIBUTE_MAP = {
    'id': 'id',
    'address_family': 'address_family',
    'device_id': 'device.id',
    'default_route': 'default_route',
}

METAL_PROJECT_BGP_CONFIG_RESPONSE_ATTRIBUTE_MAP = {
    'project_id': optional('project.id'),
    'asn': optional('asn'),
    'deployment_type': optional('deployment_type'),
    'md5': 'md5',
    'max_prefix': 'max_prefix',
    'id': optional('id'),
    'status': optional('status'),

}

METAL_PLAN_RESPONSE_ATTRIBUTE_MAP = {
    'id': 'id',
    'categories': 'categories',
    'name': 'name',
    'slug': 'slug',
    'description': 'description',
    'line': 'line',
    'legacy': 'legacy',
    'class': 'class',
    'pricing_hour': 'pricing.hour',
    'pricing_month': optional_float('pricing.month', None),
    'deployment_types': 'deployment_types',
    'available_in': 'available_in',
    'available_in_metros': 'available_in_metros',
}

METAL_VIRTUAL_CIRCUIT_RESPONSE_ATTRIBUTE_MAP = {
    'id': 'id',
    'name': 'name',
    'customer_ip': optional('customer_ip'),
    'metal_ip': optional('metal_ip'),
    'nni_vlan': 'nni_vlan',
    'peer_asn': optional('peer_asn'),
    'port': 'port',
    'project': 'project',
    'status': 'status',
    'subnet': optional('subnet'),
    'tags': 'tags',
    'type': 'type',
    'vrf': 'vrf',
    'project_id': 'project.id',
}


def get_attribute_mapper(resource_type):
    """
    Returns attribute mapper for the given resource type.
    """
    device_resources = set(['metal_device', 'metal_project_device'])
    project_resources = set(['metal_project', 'metal_organization_project'])
    ip_reservation_resources = set(['metal_ip_reservation', 'metal_available_ip'])
    ip_assignment_resources = set(['metal_ip_assignment'])
    ssh_key_resources = set(['metal_ssh_key', 'metal_project_ssh_key'])
    hardware_reservation_resources = set(['metal_project_hardware_reservation', 'metal_hardware_reservation'])
    vlan_resources = set(["metal_vlan"])
    connection_resources = set(['metal_connection', 'metal_connection_project', 'metal_connection_organization',
                                'metal_connection_project_dedicated', 'metal_connection_organization_dedicated',
                                'metal_connection_project_vlanfabric', 'metal_connection_project_vrf'])
    vrf_resources = set(['metal_vrf'])
    gateway_resources = set(["metal_gateway", "metal_gateway_vrf"])
    bgp_resources = {'metal_bgp_session', 'metal_bgp_session_by_project'}
    project_bgp_config_resources = {'metal_project_bgp_config'}
    plan_resources = set(["metal_plan"])
    virtual_circuit_resources = set(["metal_virtual_circuit", "metal_virtual_circuit_vrf"])
    if resource_type in device_resources:
        return METAL_DEVICE_RESPONSE_ATTRIBUTE_MAP
    elif resource_type in project_resources:
        return METAL_PROJECT_RESPONSE_ATTRIBUTE_MAP
    elif resource_type in ip_reservation_resources:
        return METAL_IP_RESERVATION_RESPONSE_ATTRIBUTE_MAP
    elif resource_type in ip_assignment_resources:
        return METAL_IP_ASSIGNMENT_RESPONSE_ATTRIBUTE_MAP
    elif resource_type in ssh_key_resources:
        return METAL_SSH_KEY_RESPONSE_ATTRIBUTE_MAP
    elif resource_type == 'metal_operating_system':
        return METAL_OPERATING_SYSTEM_RESPONSE_ATTRIBUTE_MAP
    elif resource_type == 'metal_metro':
        return METAL_METRO_RESPONSE_ATTRIBUTE_MAP
    elif resource_type in hardware_reservation_resources:
        return METAL_HARDWARE_RESERVATION_RESPONSE_ATTRIBUTE_MAP
    elif resource_type in connection_resources:
        return METAL_CONNECTION_RESPONSE_ATTRIBUTE_MAP
    elif resource_type == 'metal_organization':
        return METAL_ORGANIZATION_RESPONSE_ATTRIBUTE_MAP
    elif resource_type in vlan_resources:
        return VLAN_RESPONSE_ATTRIBUTE_MAP
    elif resource_type in vrf_resources:
        return METAL_VRF_RESPONSE_ATTRIBUTE_MAP
    elif resource_type in gateway_resources:
        return METAL_GATEWAY_RESPONSE_ATTRIBUTE_MAP
    elif resource_type in bgp_resources:
        return METAL_BGP_SESSION_RESPONSE_ATTRIBUTE_MAP
    elif resource_type in project_bgp_config_resources:
        return METAL_PROJECT_BGP_CONFIG_RESPONSE_ATTRIBUTE_MAP
    elif resource_type in plan_resources:
        return METAL_PLAN_RESPONSE_ATTRIBUTE_MAP
    elif resource_type in virtual_circuit_resources:
        return METAL_VIRTUAL_CIRCUIT_RESPONSE_ATTRIBUTE_MAP
    elif resource_type == 'metal_user':
        return METAL_USER_RESPONSE_ATTRIBUTE_MAP
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

    call = api_routes.build_api_call(conf, params)
    response = call.do()
    # uncomment to check response in /tmp/q
    # import q; q(response)
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
        elif v in response_dict:
            return_dict[k] = response_dict[v]
        else:
            raise Exception("attribute '{0}' (to map to '{1}') not found in response_dict: {2}".format(k, v, response_dict))
    return return_dict
