#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function
__metaclass__ = type

from typing import Any, Dict, List, Optional, Tuple, Union
import time
import yaml

from ansible.module_utils.basic import AnsibleModule, env_fallback, missing_required_lib

from ansible_specdoc.objects import SpecField, FieldType

from ansible_collections.equinix.cloud.plugins.module_utils import (
    action,
)
from ansible_collections.equinix.cloud.plugins.module_utils.metal import (
    metal_client,
    metal_api,
)

from ansible_specdoc.objects import SpecDocMeta

METAL_COMMON_ARGS = dict(
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


METAL_API_TOKEN_ARG=dict(
    type='str',
    fallback=(env_fallback, metal_client.TOKEN_ENVVARS),
    required=True,
    no_log=True,
)


EQUINIX_STATE_ARG = dict(
    type='str',
    default='present',
    choices=['present', 'absent'],
)


class EquinixModule(AnsibleModule):
    def __init__(self,
                 argument_spec,
                 required_one_of=None,
                 required_by=None,
                 required_if=None,
                 supports_check_mode=False,
                 is_info=False,
                 mutually_exclusive=None,
                 required_together=None,
                 needs_auth=True,
                 ):
        metal_client.raise_if_missing_equinix_metal()
        argument_spec.update(METAL_COMMON_ARGS)
        if needs_auth:
            argument_spec['metal_api_token'] = METAL_API_TOKEN_ARG
        if not is_info:
            argument_spec['state'] = EQUINIX_STATE_ARG
        AnsibleModule.__init__(
            self,
            argument_spec=argument_spec,
            required_one_of=required_one_of,
            required_by=required_by,
            required_if=required_if,
            supports_check_mode=supports_check_mode,
            mutually_exclusive=mutually_exclusive,
            required_together=required_together,
        )

        # not sure if calling code after super-constructor is fine, but it's the only
        # way to get configure the client in this class' constructor
        try:
            self.equinix_metal_client = metal_client.get_equinix_metal_client(
                self.params.get("metal_api_token"),
                self.params.get("metal_api_url"),
                self.params.get("metal_ua_prefix"),
            )
        except metal_client.MissingMetalPythonError as e:
            self.fail_json(msg=missing_required_lib("equinix_metal"), exception=e.exception_traceback)

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
                    # Skip uuid check for next-available when using reserved hardware
                    if k == "hardware_reservation_id" and v == "next-available":
                        continue
                    if not metal_client.is_valid_uuid(v):
                        raise Exception("Invalid UUID for {0}: {1}".format(k, v))
        except Exception as e:
            self.fail_json(msg=str(e))

    def _metal_api_call(self, resource_type, action, call_params={}):
        result = metal_api.call(
            resource_type,
            action,
            self.equinix_metal_client,
            call_params,
        )
        return result

    def create(self, resource_type):
        return self._metal_api_call(resource_type, action.CREATE, self.params.copy())

    def get_by_id(self, resource_type, tolerate_not_found=False):
        if self.params.get('id') is None:
            raise Exception("get_by_id called without id, this is a module bug.")
        try:
            result = self._metal_api_call(resource_type, action.GET, self.params.copy())
        except metal_client.NotFoundException as e:
            if tolerate_not_found:
                return None
            raise e
        return result

    def get_one_with_tags(self, resource_type: str, tags: List[str]):
        '''
        Gets exactly one resource matching a list of tags.

        This function runs a list call for the resource_type specified, and
        returns zero or one elements matching a set of tags. Raises an exception
        if more than one resource matches.
        '''
        if self.params.get('tags') is None:
            raise Exception("get_with_tags called without tags, this is a module bug.")   

        result = self._metal_api_call(resource_type, action.LIST, self.params.copy())
        matches = []
        for i in result:
            resource_tags = i.get("tags")
            # if break statement isn't hit, `else` block runs.
            for t in tags:
                if t not in resource_tags:
                    break
            else:
                matches.append(i)

        if len(matches) == 0:
            return None
        if len(matches) > 1:
            raise Exception(f'found more than one {resource_type} with tags {tags}: {matches}')
        return matches[0]

    def get_one_from_list(self, resource_type: str, match_attrs: List[str]):
        match_values = []
        for attr in match_attrs:
            if self.params.get(attr) is not None:
                match_values.append(self.params.get(attr))
            else:
                raise Exception(f'get_one_from_list called without {attr}, this is a module bug.')
        result = self._metal_api_call(resource_type, action.LIST, self.params.copy())
        matches = []
        for i in result:
            if all(i.get(attr) == value for attr, value in zip(match_attrs, match_values)):
                matches.append(i)
        if len(matches) == 0:
            return None
        if len(matches) > 1:
            raise Exception(f'found more than one {resource_type} with name {match_values}')
        return matches[0]

    def get_list(self, resource_type: str):
        return self._metal_api_call(resource_type, action.LIST, self.params.copy())

    def delete_by_id(self, resource_type: str):
        if self.params.get('id') is None:
            raise Exception('no id in module when deleting, this is a module bug')
        try:
            self._metal_api_call(resource_type, action.DELETE, self.params.copy())
        except metal_client.NotFoundException as e:
            return None
        return None

    def update_by_id(self, update_dict: dict, resource_type: str):
        specified_id = self.params.get('id')
        if specified_id is None:
            raise Exception('no id in module when updating, this is a module bug')
        update_dict['id'] = specified_id
        return self._metal_api_call(resource_type, action.UPDATE, update_dict)

    def _get_id_safe(self):
        specified_id = self.params.get('id')
        if specified_id is None:
            raise Exception('no id in module when about to poll for a condition, this is a module bug')
        return specified_id


    def wait_for_resource_condition(self, resource_type: str,
                                    attribute: str, target_value: str, timeout: int):
        specified_id = self._get_id_safe()
        stop_time = time.time() + timeout
        while time.time() < stop_time:
            result = self._metal_api_call(resource_type, action.GET, self.params.copy())
            if result[attribute] == target_value:
                return result
            time.sleep(5)
        raise Exception(f'wait for {resource_type} {specified_id} {attribute} {target_value} timed out')
    
    def wait_for_resource_removal(self, resource_type: str, timeout: int):
        specified_id = self._get_id_safe()
        stop_time = time.time() + timeout
        while time.time() < stop_time:
            try:
                self._metal_api_call(resource_type, action.GET, self.params.copy())
            except metal_client.NotFoundException:
                return
            time.sleep(5)
        raise Exception(f'wait for {resource_type} {specified_id} removal timed out')

    def get_hardware_reservation(self):
        params = {'id': self.params['hardware_reservation_id']}
        return self._metal_api_call('metal_hardware_reservation', action.GET, params)

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


def get_diff(params: dict, fetched: dict, mutables: list, overwrite_undefined_from_api=False):
    current_mutable = only_defined_mutable(params, mutables)

    # The shared get_diff function will not report a diff if an attribute
    # has a None value in either the config or the API response.  Setting
    # overwrite_undefined_from_api to True tells get_diff to report a diff
    # if an attribute is defined in the config but not the API response.
    # TODO: Long-term we should probably move away from this centralized
    # logic so that each module has to make its own decisions about when
    # and how to update attributes
    if overwrite_undefined_from_api:
        fetched_mutable = fetched
    else:
        fetched_mutable = only_defined_mutable(fetched, mutables)

    defined_mutable_keys = current_mutable.keys() & fetched_mutable.keys()
    if defined_mutable_keys == set():
        return {}
    return update_dict(
        {k: current_mutable[k] for k in defined_mutable_keys},
        {k: fetched_mutable[k] for k in defined_mutable_keys},
        mutables,
    )


def getSpecDocMeta(short_description, description, options, examples, return_values):
    # validate_yaml(examples)
    return SpecDocMeta(
        short_description=short_description,
        description=description,
        options=options,
        examples=examples,
        return_values=return_values,
        author='Equinix DevRel Team (@equinix) <support@equinix.com>',
    )


def validate_yaml(s):
    try:
        [yaml.safe_load(e) for e in s]
    except yaml.YAMLError as e:
        raise Exception(e)
