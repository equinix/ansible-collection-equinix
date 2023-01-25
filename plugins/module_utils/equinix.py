# (c) 2021, Jason DeTiberus (@detiber) <jdetiberus@equinix.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import re
import uuid
import traceback
from typing import Any

from .mappers import *

try:
    from ansible.module_utils.ansible_release import __version__ as ANSIBLE_VERSION
except Exception:
    ANSIBLE_VERSION = 'unknown'

HAS_METAL_SDK = True
try:
    import equinixmetalpy
    from equinixmetalpy import ApiException
except ImportError:
    HAS_METAL_SDK = False
    HAS_METAL_SDK_EXC = traceback.format_exc()


from ansible.module_utils.basic import AnsibleModule, env_fallback, missing_required_lib

NAME_RE = r'({0}|{0}{1}*{0})'.format(r'[a-zA-Z0-9]', r'[a-zA-Z0-9\-]')
HOSTNAME_RE = r'({0}\.)*{0}$'.format(NAME_RE)

METAL_USER_AGENT = 'ansible_equinix Ansible/{0}'.format(ANSIBLE_VERSION)

METAL_COMMON_ARGS = dict(
    metal_api_token=dict(
        type='str',
        fallback=(env_fallback, ['METAL_API_TOKEN', 'METAL_AUTH_TOKEN']),
        required=True,
        no_log=True,
    ),
    metal_api_url=dict(
        type='str',
        description='The Equinix Metal API URL to use',
        default='https://api.equinix.com/metal/v1',
        fallback=(env_fallback, ['METAL_API_URL']),
        no_log=True,
    ),
    metal_ua_prefix=dict(
        type='str',
        description='The prefix to use for the User-Agent header',
        fallback=(env_fallback, ['METAL_UA_PREFIX']),
        no_log=True,
    ),
)

METAL_TAG_ARGS = dict(
    tags=dict(type='list',
              description='The tags to assign to this resource.'),
)


def href_to_id(href):
    return href.split('/')[-1]


def get_resource_arg(module_arg, resource):
    if module_arg in resource:
        return resource[module_arg]
    if module_arg.endswith('_id'):
        subres = module_arg[:-3]
        return href_to_id(resource[subres]['href'])


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

class EquinixModule(AnsibleModule):
    def __init__(self, *args, **kwargs):
        argument_spec = {}
        if "argument_spec" in kwargs:
            argument_spec = kwargs["argument_spec"]
        argument_spec.update(METAL_COMMON_ARGS)

        if kwargs.get("supports_tags", False):
            argument_spec.update(METAL_TAG_ARGS)
            kwargs.pop("supports_tags")

        kwargs["argument_spec"] = argument_spec
        AnsibleModule.__init__(self, *args, **kwargs)

    def get_metal_client(self):
        if not HAS_METAL_SDK:
            self.fail_json(msg=missing_required_lib('equinixmetalpy'), exception=HAS_METAL_SDK_EXC)
        ua = METAL_USER_AGENT
        if self.params.get('metal_ua_prefix'):
            ua = '{0} {1}'.format(self.params.get('metal_ua_prefix'), ua)
        return equinixmetalpy.Client(
            credential=self.params.get('metal_api_token'),
            base_url=self.params.get('metal_api_url'),
            base_user_agent=ua,
            user_agent_overwrite=True,
        )

    def create(self, resource_type):
        client = self.get_metal_client()
        creator = pick_creator(client, self.params, resource_type)
        request_model = CREATOR_REQUEST_MODEL_MAP.get(resource_type)
        if request_model is None:
            raise NotImplementedError(f'Model for creating {resource_type} not implemented')
        request = request_model.from_dict(self.params)
        result = creator(request)
        equinixmetalpy.raise_if_error(result)
        return self.map_to_module_params(resource_type, result)

    def map_to_module_params(self, resource_type, response):
        # resource_type will be necessary with non-straightforward attribute mappings
        return_dict = {}
        simple_types = ['str', 'bool', 'int', 'float']
        response_dict = populate_ids_from_hrefs(response)
        # The input params of a module
        for k, v in self.argument_spec.items():
            if k in SKIPPED_MODULE_PARAMS:
                continue
            if v['type'] in simple_types:
                if k in response_dict:
                    return_dict[k] = response_dict[k]
                elif k.endswith('_id'):
                    subres = k[:-3]
                    if subres in response_dict:
                        return_dict[k] = response_dict[subres]['id']
                else:
                    raise NotImplementedError(f'Not sure how to map "{k}" to "{v}" from {response}')
        for k, v in response_dict.items():
            if k not in return_dict:
                return_dict[k] = v
        return return_dict

    def get_one(self, resource_type: str):
        client = self.get_metal_client()
        id = self.params.get('id')
        if id:
            getter = pick_getter(client, self.params, resource_type)
            result = getter(id)
            equinixmetalpy.raise_if_error(result)
            return self.map_to_module_params(resource_type, result)
        name = self.params.get('name')
        if name:
            lister = pick_lister(client, self.params, resource_type)
            resource_list = lister().list
            matchings = [resource for resource in resource_list if resource.name == name]
            if len(matchings) > 1:
                raise Exception(f'found more than one {resource_type} with name {name}')
            if len(matchings) == 1:
                result = matchings[0]
                equinixmetalpy.raise_if_error(result)
                return self.map_to_module_params(resource_type, result)
            return None
        raise Exception('no id or name in module when fetching, this is a module bug')

    def get_list(self, resource_type: str):
        client = self.get_metal_client()
        lister = pick_lister(client, self.params, resource_type)
        listing_kwargs = {}

        search = self.params.get('name')
        if search:
            listing_kwargs['name'] = search
        result_list = lister(**listing_kwargs).list
        return [self.map_to_module_params(resource_type, result) for result in result_list]

    def delete(self, resource_type: str):
        client = self.get_metal_client()
        id = self.params.get('id')
        if id:
            deleter = pick_deleter(client, resource_type)
            result = deleter(id)
            equinixmetalpy.raise_if_error(result)
            return None
        raise Exception('no id in module when deleting, this is a module bug')

    def update(self, params: dict, resource_type: str):
        id = self.params.get('id')
        return self.update_by_id(id, params, resource_type)

    def update_by_id(self, id, params: dict, resource_type: str):
        client = self.get_metal_client()
        if id:
            updater = pick_updater(client, params, resource_type)
            request_model = UPDATER_REQUEST_MODEL_MAP.get(resource_type)
            if request_model is None:
                raise NotImplementedError(f'Update of {resource_type} not implemented')
            request = request_model.from_dict(params)
            result = updater(id, request)
            equinixmetalpy.raise_if_error(result)
            return self.map_to_module_params(resource_type, result)
        raise Exception('no id in module when updating, this is a module bug')


def update_dict(current, fetched, mutables: list):
    d = {}
    for a in mutables:
        if current.get(a) != fetched.get(a):
            d[a] = current.get(a)
    return d


def only_defined_mutable(params: dict, mutables: list):
    return_dict = {}
    for a in mutables:
        v = params.get(a)
        if v is not None:
            return_dict[a] = v
    return return_dict


def get_diff(params: dict, fetched: dict, mutables: list):
    current_mutable = only_defined_mutable(params, mutables)
    fetched_mutable = only_defined_mutable(fetched, mutables)

    defined_mutable_keys = current_mutable.keys() & fetched_mutable.keys()
    if defined_mutable_keys == set():
        return {}
    return update_dict(
        {k: current_mutable[k] for k in defined_mutable_keys},
        {k: fetched_mutable[k] for k in defined_mutable_keys},
        mutables,
    )
