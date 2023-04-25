#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


import os
from typing import List, Dict, Any

from ansible.errors import AnsibleError
from ansible.plugins.inventory import BaseInventoryPlugin, Constructable, to_safe_group_name

from ansible_collections.equinix.cloud.plugins.module_utils import (
    action,
)
from ansible_collections.equinix.cloud.plugins.module_utils.metal import (
    metal_client,
    metal_api,
)

DOCUMENTATION = '''
author: Equinix DevRel Team (@equinix) <support@equinix.com>
description: Reads device inventories from Equinix Metal. Uses YAML configuration
  file that ends with equinix_metal.(yml|yaml). ansible_host is set to first public
  IP address of the device.
module: metal_device
extends_documentation_fragment: [constructed]
notes: []
options:
  plugin:
    choices: ['equinix_metal', 'equinix.cloud.metal_device']
    description:
    - Token that ensures this is a source file for the plugin.
    required: true
    type: str
  metal_api_token:
    description:
    - Equinix Metal API token. Can also be specified via METAL_AUTH_TOKEN environment
      variable.
    required: true
    env:
        - name: METAL_AUTH_TOKEN
    type: str
  project_ids:
    description:
    - List of Equinix Metal project IDs to query for devices.
    type: list
    elements: str
    required: false
requirements:
- python >= 3
- metal_python >= 0.0.1
short_description: Equinix Metal Device inventory source
'''

EXAMPLES = '''
plugin: equinix.cloud.metal_device
strict: false
keyed_groups:
  - prefix: tag
    key: tags
  - prefix: equinix_metal_plan
    key: plan
  - key: metro
    prefix: equinix_metal_metro
  - key: state
    prefix: equinix_metal_state
'''

RETURN = '''
'''

EXCLUDE_ATTRIBUTES = [
    "ssh_keys",
]


def label(device: Dict[str, Any]) -> str:
    """Return the label of a device."""
    return device['hostname']


class InventoryModule(BaseInventoryPlugin, Constructable):

    NAME = 'equinix.cloud.metal_device'

    def __init__(self) -> None:
        super().__init__()
        self.client = None
        self.api_call_configs = None

    def _build_client(self) -> None:
        metal_api_token = self.get_option('metal_api_token')
        if metal_api_token is None:
            for envvarname in metal_client.TOKEN_ENVVARS:
                metal_api_token = os.environ.get(envvarname)
                if metal_api_token is not None:
                    break
        if metal_api_token is None:
            raise AnsibleError(
                "The Equinix Metal dynamic inventory plugin requires a token. "
                "Please set the 'metal_api_token' option or set one of the "
                "following environment variables: %s"
                % ', '.join(metal_client.TOKEN_ENVVARS)
            )
        try:
            self.client = metal_client.get_equinix_metal_client(str(metal_api_token))
        except metal_client.MissingMetalPythonError as e:
            raise AnsibleError("The Equinix Metal dynamic inventory plugin equires the 'equinix_metal' package")

    def verify_file(self, path):
        '''
            :param path: the path to the inventory config file
            :return the contents of the config file
        '''
        if not super().verify_file(path):
            return False
        endings = ('equinix.yml', 'equinix.yaml', 'device.yml', 'device.yaml')
        if any((path.endswith(ending) for ending in endings)):
            return True
        self.display.debug("equinix.cloud inventory filename must end with 'equinix.yml' or 'equinix.yaml'")
        return False

    def parse(self, inventory, loader, path, cache=True):
        super().parse(inventory, loader, path)
        self._read_config_data(path)
        self._build_client()

        strict = self.get_option("strict")
        configured_project_ids = self._get_project_ids()
        devices = self._get_devices_from_project_ids(configured_project_ids)
        projects = set([device['project_id'] for device in devices])
        for project in projects:
            self.inventory.add_group(to_safe_group_name(project))

        for device in devices:
            group_name = to_safe_group_name(device['project_id'])
            self.inventory.add_host(label(device), group=group_name)
            first_public_ip = next((ip['address'] for ip in device['ip_addresses'] if ip['public']), None)
            self.inventory.set_variable(label(device), 'ansible_host', first_public_ip)
            self.inventory.add_host(label(device), group='all')
            for k, v in device.items():
                if k not in EXCLUDE_ATTRIBUTES:
                    self.inventory.set_variable(label(device), k, v)

        for device in devices:
            variables = self.inventory.get_host(label(device)).get_vars()
            self._add_host_to_composed_groups(
                self.get_option('groups'),
                variables,
                label(device),
                strict=strict)
            self._add_host_to_keyed_groups(
                self.get_option('keyed_groups'),
                variables,
                label(device),
                strict=strict)
            self._set_composite_vars(
                self.get_option('compose'),
                variables,
                label(device),
                strict=strict
            )

    def _get_project_ids(self):
        project_ids_arg_value = self.get_option('project_ids')
        project_ids: List[str] = []
        if project_ids_arg_value:
            project_ids = project_ids_arg_value
        for pid in project_ids:
            if not metal_client.is_valid_uuid(pid):
                raise AnsibleError("Invalid project id: %s" % pid)
        if len(project_ids) == 0:
            return [p["id"] for p in self._get_all_projects()]
        return project_ids

    def _get_all_projects(self):
        return metal_api.call("metal_project", action.LIST, self.client)

    def _get_project_devices(self, project_id):
        return metal_api.call("metal_project_device", action.LIST, self.client, {"project_id": project_id})

    def _get_devices_from_project_ids(self, project_ids):
        devices = []
        for p in project_ids:
            devices.extend(self._get_project_devices(p))
        return devices
