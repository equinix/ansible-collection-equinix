# (c) 2023, Tomas Karasek (@t0mk) <tom.to.the.k@gmail.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from typing import List, Union, Optional, Callable
import enum
import inspect

SKIPPED_MODULE_PARAMS = [
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


class Action(enum.Enum):
    CREATE = 'create'
    UPDATE = 'update'
    DELETE = 'delete'
    GET = 'get'
    LIST = 'list'


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


class ApiCallConfig(object):
    """
    A class to hold the combination of (function, parameter parser and 
    request model class of an API call.
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
                 conf: ApiCallConfig,
                 client,
                 params: Optional[dict] = {},
                 ):
        self.conf = conf
        self.client = client
        self.request_model_instance = None
        self.path_vars = []
        body_parameters = params
        if self.conf.params_parser:
            self.path_vars, body_parameters = self.conf.params_parser.parse(params)
        relevant_body_parameters = {k: v for k, v in body_parameters.items() if k not in SKIPPED_MODULE_PARAMS}
        if self.conf.request_model_class is not None:
            self.request_model_instance = self.conf.request_model_class.from_dict(
                relevant_body_parameters)

    def do(self, query_params: Optional[dict] = None):
        arg_list = [self.client] + self.path_vars
        if self.request_model_instance is not None:
            arg_list.append(self.request_model_instance)
        #_D('arg_list: {0}'.format(arg_list))
        result = self.conf.func(*arg_list, params=query_params)
        return result


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


# items in the ApiCall constructor are:
# - the function to call
# - params parser to use to parse path and body params, in other words, it returns
#   a tuple of [id params], [body params]
# - class for request body (defined for create and update)
# - a mapper to use to map the API response to the Ansible output. It ch

id_getter = ParamsParser("id")


def get_api_call_configs(equinixmetalpy_module):
    """
    This function returns a dictionary of API call configurations.
    The module parameter is here so that Python never crashes when
    equinixmetalpy is not installed. It's like this to satisfy the
    Ansible sanity checks.
    """
    return {
        ('metal_device', Action.GET): ApiCallConfig(
            equinixmetalpy_module.Client.find_device_by_id,
            id_getter,
            ),
        ('metal_project', Action.GET): ApiCallConfig(
            equinixmetalpy_module.Client.find_project_by_id,
            id_getter,
            ),

        ('metal_project_device', Action.LIST): ApiCallConfig(
            equinixmetalpy_module.Client.find_project_devices,
            ParamsParser("project_id"),
            ),
        ('metal_organization_device', Action.LIST): ApiCallConfig(
            equinixmetalpy_module.Client.find_organization_devices,
            ParamsParser("organization_id"),
            ),
        ('metal_project', Action.LIST): ApiCallConfig(equinixmetalpy_module.Client.find_projects),
        ('metal_organization_project', Action.LIST): ApiCallConfig(
            equinixmetalpy_module.Client.find_organization_projects,
            ParamsParser("organization_id"),
            ),

        ('metal_device', Action.DELETE): ApiCallConfig(
            equinixmetalpy_module.Client.delete_device,
            id_getter,
            ),
        ('metal_project', Action.DELETE): ApiCallConfig(
            equinixmetalpy_module.Client.delete_project,
            id_getter,
            ),

        ('metal_device_metro', Action.CREATE): ApiCallConfig(
            equinixmetalpy_module.Client.create_device,
            ParamsParser("project_id"),
            equinixmetalpy_module.models.DeviceCreateInMetroInput,
            ),
        ('metal_device_facility', Action.CREATE): ApiCallConfig(
            equinixmetalpy_module.Client.create_device,
            ParamsParser("project_id"),
            equinixmetalpy_module.models.DeviceCreateInFacilityInput,
        ),
        ('metal_project', Action.CREATE): ApiCallConfig(
            equinixmetalpy_module.Client.create_project,
            None,
            equinixmetalpy_module.models.ProjectCreateFromRootInput,
        ),
        ('metal_organization_project', Action.CREATE): ApiCallConfig(
            equinixmetalpy_module.Client.create_organization_project,
            ParamsParser("organization_id"),
            equinixmetalpy_module.models.ProjectCreateInput,
            ),

        ('metal_device', Action.UPDATE): ApiCallConfig(
            equinixmetalpy_module.Client.update_device,
            id_getter,
            equinixmetalpy_module.models.DeviceUpdateInput,
        ),
        ('metal_project', Action.UPDATE): ApiCallConfig(
            equinixmetalpy_module.Client.update_project,
            id_getter,
            equinixmetalpy_module.models.ProjectUpdateInput,
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
