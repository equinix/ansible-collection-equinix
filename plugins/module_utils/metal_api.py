# (c) 2023, Tomas Karasek (@t0mk) <tom.to.the.k@gmail.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from typing import List, Union, Optional, Callable
import inspect

from ansible_collections.equinix.cloud.plugins.module_utils import (
    metal_client,
    action,
)

try:
    import equinixmetalpy
except ImportError:
    # This is handled in raise_if_missing_equinixmetalpy()
    pass

SKIPPED_PARAMS = [
    "state",
    "metal_api_token",
    "metal_api_url",
    "metal_ua_prefix",
]

SKIPPED_RESPONSE_PARAMS = [
    "actions", "created_by", "facility", "ip_addresses",
    "network_ports", "operating_system", "plan", "project",
    "ssh_keys"
]


class ParamsParser:
    """
    A class to parse the module parameters into a tuple:
    (id_params for URL path, params for request body)

    Right now it only pops ids from the module params, later it might also
    do some validation and/or transformation of the params for the request
    body.
    """

    def __init__(self, id_param_names: Union[str, List[str]] = []):
        self.id_param_names = id_param_names if isinstance(id_param_names, list) else [id_param_names]

    def parse(self, params):
        #_D("ParamsParser.parse() called with params: ", _PJ(params))
        id_params = []
        for name in self.id_param_names:
            if name not in params:
                raise ValueError('Missing required option: {0}'.format(name))
            id_params.append(params.pop(name))
        return id_params, params


class ApiCallSpecs(object):
    """
    Specification of API call for certain resource type, action and parameters parser.

    An instance might specify API calls for GETting metal_device and parsing 
    resource attributes to ansible dict.
    """

    def __init__(self,
                 func: Callable,
                 params_parser: Optional[ParamsParser] = None,
                 request_model_class: Optional[Callable] = None,
                 ):
        self.func = func
        self.params_parser = params_parser
        self.request_model_class = request_model_class
        if self.request_model_class is not None:
            if not inspect.isclass(request_model_class):
                raise ValueError('request_model_class must be a class, is {0}'.format(type(request_model_class)))


class ApiCall(object):
    """
    A class representing an API call. It holds the configuration of the
    API call (ApiCallConfig) and the module parameters which are parsed
    into URL params and body params.

    API call body (if necessary) is created from the module parameters.
    """

    def __init__(self,
                 conf: ApiCallSpecs,
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
        relevant_body_params = {k: v for k, v in body_params.items() if k not in SKIPPED_PARAMS}
        if self.conf.request_model_class is not None:
            self.request_model_instance = self.conf.request_model_class.from_dict(
                relevant_body_params)

    def do(self):
        arg_list = [self.client] + self.path_vars
        if self.request_model_instance is not None:
            arg_list.append(self.request_model_instance)
        #_D('arg_list: {0}'.format(arg_list))
        result = self.conf.func(*arg_list, params=self.url_params)
        return result

    def describe(self):
        return "{0} to {1}".format(self.conf.func.__name__, self.path_vars)


def optional_str(key: str):
    return lambda resource: resource.get(key, '')


def optional_bool(key: str):
    return lambda resource: resource.get(key, False)


def optional_float(key: str):
    return lambda resource: resource.get(key, 0.0)


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


id_getter = ParamsParser("id")


def get_api_call_configs():
    """
    This function returns a dictionary of API call configurations.
    """

    # we check for the presence of the equinixmetalpy module here, because
    # the ApiCallConfigs use classes straight from the equinixmetalpy module
    # and we prefer to fail early and hopefully into module.fail_json()
    metal_client.raise_if_missing_equinixmetalpy()

    return {
        ('metal_device', action.GET): ApiCallSpecs(
            equinixmetalpy.Client.find_device_by_id,
            id_getter,
            ),
        ('metal_project', action.GET): ApiCallSpecs(
            equinixmetalpy.Client.find_project_by_id,
            id_getter,
            ),

        ('metal_project_device', action.LIST): ApiCallSpecs(
            equinixmetalpy.Client.find_project_devices,
            ParamsParser("project_id"),
            ),
        ('metal_organization_device', action.LIST): ApiCallSpecs(
            equinixmetalpy.Client.find_organization_devices,
            ParamsParser("organization_id"),
            ),
        ('metal_project', action.LIST): ApiCallSpecs(equinixmetalpy.Client.find_projects),
        ('metal_organization_project', action.LIST): ApiCallSpecs(
            equinixmetalpy.Client.find_organization_projects,
            ParamsParser("organization_id"),
            ),

        ('metal_device', action.DELETE): ApiCallSpecs(
            equinixmetalpy.Client.delete_device,
            id_getter,
            ),
        ('metal_project', action.DELETE): ApiCallSpecs(
            equinixmetalpy.Client.delete_project,
            id_getter,
            ),

        ('metal_device_metro', action.CREATE): ApiCallSpecs(
            equinixmetalpy.Client.create_device,
            ParamsParser("project_id"),
            equinixmetalpy.models.DeviceCreateInMetroInput,
            ),
        ('metal_device_facility', action.CREATE): ApiCallSpecs(
            equinixmetalpy.Client.create_device,
            ParamsParser("project_id"),
            equinixmetalpy.models.DeviceCreateInFacilityInput,
        ),
        ('metal_project', action.CREATE): ApiCallSpecs(
            equinixmetalpy.Client.create_project,
            None,
            equinixmetalpy.models.ProjectCreateFromRootInput,
        ),
        ('metal_organization_project', action.CREATE): ApiCallSpecs(
            equinixmetalpy.Client.create_organization_project,
            ParamsParser("organization_id"),
            equinixmetalpy.models.ProjectCreateInput,
            ),

        ('metal_device', action.UPDATE): ApiCallSpecs(
            equinixmetalpy.Client.update_device,
            id_getter,
            equinixmetalpy.models.DeviceUpdateInput,
        ),
        ('metal_project', action.UPDATE): ApiCallSpecs(
            equinixmetalpy.Client.update_project,
            id_getter,
            equinixmetalpy.models.ProjectUpdateInput,
        ),
    }


def get_attribute_mapper(resource_type):
    """
    Returns attribute mapper for the given resource type.
    """
    device_resources = set(['metal_device', 'metal_device_metro',
                            'metal_project_device', 'metal_device_facility'])
    project_resources = set(['metal_project', 'metal_organization_project'])
    if resource_type in device_resources:
        return METAL_DEVICE_RESPONSE_ATTRIBUTE_MAP
    elif resource_type in project_resources:
        return METAL_PROJECT_RESPONSE_ATTRIBUTE_MAP
    else:
        raise NotImplementedError("No mapper for resource type %s" % resource_type)


def call(resource_type, action, client, body_params={}, url_params={}):
    """
    This function wraps the API call and returns the response.
    """
    metal_client.raise_if_missing_equinixmetalpy()
    conf = get_api_call_configs().get((resource_type, action))
    if conf is None:
        raise NotImplementedError("No API call for resource type %s and action %s" % (resource_type, action))
    call = ApiCall(conf, client, body_params, url_params)
    response = call.do()
    metal_client.raise_if_error(response, call.describe())
    if action == action.DELETE:
        return None
    attribute_mapper = get_attribute_mapper(resource_type)
    if action == action.LIST:
        return [response_to_ansible_dict(r, attribute_mapper)for r in response.list]
    return response_to_ansible_dict(response, attribute_mapper)


def href_to_id(href):
    return href.split('/')[-1]


def add_id_from_href(v):
    if ('href' in v) & ('id' not in v):
        v['id'] = href_to_id(v['href'])


def populate_ids_from_hrefs(resource):
    return_dict = resource.as_dict()
    for v in return_dict.values():
        if type(v) is dict:
            if ('href' in v) & ('id' not in v):
                add_id_from_href(v)
        if type(v) is list:
            for i in v:
                if type(i) is dict:
                    add_id_from_href(i)
    return return_dict


def response_to_ansible_dict(response, attribute_mapper):
    return_dict = {}
    if response is None:
        return {}
    response_dict = populate_ids_from_hrefs(response)
    if attribute_mapper is None:
        return response_dict()
    for k, v in attribute_mapper.items():
        if callable(v):
            return_dict[k] = v(response_dict)
        elif "." in v:
            vs = v.split(".")
            if vs[0] in response_dict:
                if vs[1] in response_dict[vs[0]]:
                    return_dict[k] = response_dict[vs[0]][vs[1]]
        elif k in response_dict:
            return_dict[k] = response_dict[v]
        else:
            raise Exception('key {0} (to map to {1}) not found in response_dict:\n {2}'.format(k, v))
    return return_dict
