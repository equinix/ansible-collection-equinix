#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt) 



from __future__ import absolute_import, division, print_function
__metaclass__ = type

import time

from ansible.module_utils.basic import AnsibleModule, env_fallback, missing_required_lib

from ansible_collections.equinix.cloud.plugins.module_utils import (
    metal_client,
    metal_api,
    action,
)


METAL_COMMON_ARGS = dict(
    metal_api_token=dict(
        type='str',
        fallback=(env_fallback, metal_client.TOKEN_ENVVARS),
        required=True,
        no_log=True,
    ),
    metal_api_url=dict(
        type='str',
        default=metal_client.API_URL,
        fallback=(env_fallback, metal_client.URL_ENVVARS),
        no_log=True,
    ),
    metal_ua_prefix=dict(
        type='str',
        default="",
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


class EquinixModule(AnsibleModule):
    def __init__(self, *args, **kwargs):
        metal_client.raise_if_missing_equinixmetalpy()
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
        try:
            self.client = metal_client.get_metal_client(
                self.params.get("metal_api_token"),
                self.params.get("metal_api_url"),
                self.params.get("metal_ua_prefix"),
            )
        except metal_client.MissingEquinixmetalpyError as e:
            self.fail_json(msg=missing_required_lib("equinixmetalpy"), exception=e.exception_traceback)
        self.params_checked = False
        AnsibleModule.__init__(self, *args, **kwargs)

    def params_syntax_check(self):
        try:
            name = self.params.get("name")
            if name:
                metal_client.raise_if_invalid_resource_name(name)
            hostname = self.params.get("hostname")
            if hostname:
                metal_client.raise_if_invalid_hostname(hostname)
            uuid_args = {k: v for k, v in self.params.items() if (k == "id") | (k.endswith("_id"))}
            for k, v in uuid_args.items():
                if v is not None:
                    if not metal_client.is_valid_uuid(v):
                        raise Exception("Invalid UUID for {0}: {1}".format(k, v))
        except Exception as e:
            self.fail_json(msg=str(e))

    def _metal_api_call(self, resource_type, action, body_params={}, url_params={}):
        return metal_api.call(resource_type, action, self.client, body_params, url_params)

    def create(self, resource_type):
        return self._metal_api_call(resource_type, action.CREATE, self.params.copy())

    def get_by_id(self, resource_type, tolerate_not_found=False):
        if self.params.get('id') is None:
            raise Exception("get_by_id called without id, this is a module bug.")
        try:
            result = self._metal_api_call(resource_type, action.GET, self.params.copy())
        except metal_client.MetalApiError as e:
            if (e.isNotFoundError) & tolerate_not_found:
                return None
            raise e
        return result

    def get_one_from_list(self, resource_type: str, name_attr: str, filters: dict = None):
        name_value = self.params.get(name_attr)
        if name_value is None:
            raise Exception(f'get_one_from_list called without {name_attr}, this is a module bug.')
        result = self._metal_api_call(resource_type, action.LIST, self.params.copy(), url_params=filters)
        dict_list = result
        matches = [i for i in dict_list if i[name_attr] == name_value]
        if len(matches) == 0:
            return None
        if len(matches) > 1:
            raise Exception(f'found more than one {resource_type} with name {name_value}')
        return matches[0]

    def get_list(self, resource_type: str, filters: dict = None):
        return self._metal_api_call(resource_type, action.LIST, self.params.copy(), url_params=filters)

    def delete_by_id(self, resource_type: str):
        if self.params.get('id') is None:
            raise Exception('no id in module when deleting, this is a module bug')
        try:
            self._metal_api_call(resource_type, action.DELETE, self.params.copy())
        except metal_client.MetalApiError as e:
            if e.isNotFoundError:
                return None
            raise e
        return None

    def update_by_id(self, update_dict: dict, resource_type: str):
        specified_id = self.params.get('id')
        if specified_id is None:
            raise Exception('no id in module when updating, this is a module bug')
        update_dict['id'] = specified_id
        return self._metal_api_call(resource_type, action.UPDATE, update_dict)

    def wait_for_resource_condition(self, resource_type: str,
                                    attribute: str, target_value: str, timeout: int):
        specified_id = self.params.get('id')
        if specified_id is None:
            raise Exception('no id in module when waiting for condition, this is a module bug')
        stop_time = time.time() + timeout
        while time.time() < stop_time:
            result = self._metal_api_call(resource_type, action.GET, self.params.copy())
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
