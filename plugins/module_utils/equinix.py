# (c) 2023, Tomas Karasek <tom.to.the.k@gmail.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import time
import traceback
import re

from .mappers import (
    get_api_call_configs,
    get_attribute_mapper,
    Action,
    ApiCall,
)

HAS_METAL_SDK = True
try:
    import equinixmetalpy
except ImportError:
    HAS_METAL_SDK = False
    HAS_METAL_SDK_EXC = traceback.format_exc()


from ansible.module_utils.basic import AnsibleModule, env_fallback, missing_required_lib

NAME_RE = r'^({0}|{0}{1}*{0})$'.format(r'[a-zA-Z0-9]', r'[a-zA-Z0-9\-_ ]')
HOSTNAME_RE = r'^({0}\.)*{0}$'.format(NAME_RE)
UUID_RE = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'

METAL_USER_AGENT = 'ansible-metal'

METAL_COMMON_ARGS = dict(
    metal_api_token=dict(
        type='str',
        fallback=(env_fallback, ['METAL_API_TOKEN', 'METAL_AUTH_TOKEN']),
        required=True,
        no_log=True,
    ),
    metal_api_url=dict(
        type='str',
        default='https://api.equinix.com/metal/v1',
        fallback=(env_fallback, ['METAL_API_URL']),
        no_log=True,
    ),
    metal_ua_prefix=dict(
        type='str',
        no_log=True,
    ),
)

METAL_PROJECT_ARG = dict(
    project_id=dict(
        type='str',
        fallback=(env_fallback, ['METAL_PROJECT_ID']),
    ),
)

METAL_TAGS_ARG = dict(
    tags=dict(type='list',
              elements='str',
              ),
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


class EquinixModule(AnsibleModule):
    def __init__(self, *args, **kwargs):
        argument_spec = {}
        if "argument_spec" in kwargs:
            argument_spec = kwargs["argument_spec"]
        argument_spec.update(METAL_COMMON_ARGS)

        if kwargs.get("supports_tags", False):
            argument_spec.update(METAL_TAGS_ARG)
            kwargs.pop("supports_tags")
        if kwargs.get("supports_project_id", False):
            argument_spec.update(METAL_PROJECT_ARG)
            kwargs.pop("supports_project_id")
        kwargs["argument_spec"] = argument_spec
        AnsibleModule.__init__(self, *args, **kwargs)
        self.client = self._get_metal_client()
        self.api_call_configs = get_api_call_configs(equinixmetalpy)
        self.params_checked = False
        AnsibleModule.__init__(self, *args, **kwargs)

    def params_syntax_check(self):
        name = self.params.get("name")
        if name:
            import q
            q(name)
            if not re.match(NAME_RE, name):
                raise Exception("name {0} is not a valid name. Regexp for name is {1}".format(name, NAME_RE))
        hostname = self.params.get("hostname")
        if hostname:
            if not re.match(HOSTNAME_RE, hostname):
                raise Exception("hostname {0} is not a valid hostname. regexp for hostname is {1}".format(hostname, HOSTNAME_RE))
        uuid_args = {k: v for k, v in self.params.items() if (k == "id") | (k.endswith("_id"))}
        for k, v in uuid_args.items():
            if v is not None:
                if not re.match(UUID_RE, v):
                    raise Exception("{0} {1} is not a valid UUID".format(k, v))

    def _get_metal_client(self):
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

    def _do_api_call(self, resource_type, action, params, additional_params: dict = None):
        conf = self.api_call_configs[(resource_type, action)]
        response = ApiCall(conf, self.client, params)
        return self._parse_api_response(resource_type, action, response.do(additional_params))

    def _parse_api_response(self, resource_type, action, response):
        equinixmetalpy.raise_if_error(response)
        if action == Action.DELETE:
            return None
        attribute_mapper = get_attribute_mapper(resource_type)
        if action == Action.LIST:
            return [response_to_ansible_dict(r, attribute_mapper)for r in response.list]
        return response_to_ansible_dict(response, attribute_mapper)

    def create(self, resource_type):
        return self._do_api_call(resource_type, Action.CREATE, self.params.copy())

    def get_by_id(self, resource_type, tolerate_not_found=False):
        if self.params.get('id') is None:
            raise Exception("get_by_id called without id, this is a module bug.")
        try:
            result = self._do_api_call(resource_type, Action.GET, self.params.copy())
        except equinixmetalpy.ApiError as e:
            if (e.error_list == ["Not found"]) & tolerate_not_found:
                return None
            raise e
        return result

    def get_one_from_list(self, resource_type: str, name_attr: str, filters: dict = None):
        name_value = self.params.get(name_attr)
        if name_value is None:
            raise Exception(f'get_one_from_list called without {name_attr}, this is a module bug.')
        result = self._do_api_call(resource_type, Action.LIST, self.params.copy(), filters)
        dict_list = result
        matches = [i for i in dict_list if i[name_attr] == name_value]
        if len(matches) == 0:
            return None
        if len(matches) > 1:
            raise Exception(f'found more than one {resource_type} with name {name_value}')
        return matches[0]

    def get_list(self, resource_type: str, filters: dict = None):
        return self._do_api_call(resource_type, Action.LIST, self.params.copy(), filters)

    def delete_by_id(self, resource_type: str):
        if self.params.get('id') is None:
            raise Exception('no id in module when deleting, this is a module bug')
        try:
            self._do_api_call(resource_type, Action.DELETE, self.params.copy())
        except equinixmetalpy.ApiError as e:
            if e.error_list == ["Not found"]:
                return None
            raise e
        return None

    def update_by_id(self, update_dict: dict, resource_type: str):
        specified_id = self.params.get('id')
        if specified_id is None:
            raise Exception('no id in module when updating, this is a module bug')
        update_dict['id'] = specified_id
        return self._do_api_call(resource_type, Action.UPDATE, update_dict)

    def wait_for_resource_condition(self, resource_type: str,
                                    attribute: str, target_value: str, timeout: int):
        specified_id = self.params.get('id')
        if specified_id is None:
            raise Exception('no id in module when waiting for condition, this is a module bug')
        stop_time = time.time() + timeout
        while time.time() < stop_time:
            result = self._do_api_call(resource_type, Action.GET, self.params.copy())
            if result[attribute] == target_value:
                return result
            time.sleep(5)
        raise Exception(f'wait for {resource_type} {specified_id} {attribute} {target_value} timed out')


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
