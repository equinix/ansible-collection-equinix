#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
    name: device
    plugin_type: inventory
    short_description: Equinix Metal Device inventory source
    extends_documentation_fragment:
        - equinix.cloud.metal_common
        - constructed
    description:
        - Reads device inventories from Equinix Metal
        - Uses YAML configuration file that ends with equinix_metal.(yml|yaml).
        - ansible_host is set to first public IP address of the device.
    options:
        plugin:
            description: Token that ensures this is a source file for the plugin.
            required: True
            choices: ['equinix_metal', 'equinix.cloud.metal_device']
        project_ids:
            description: List of Equinix Metal project IDs to query for devices.
            type: list
            elements: str
        metal_api_token:
            description: Equinix Metal API token. Can also be specified via METAL_AUTH_TOKEN environment variable.
            required: True
            env:
                - name: METAL_AUTH_TOKEN
        keyed_groups:
            description: List of groups to create based on the values of a variable.
            type: list
            elements: dict
            suboptions:
                key:
                    description: The key to group by.
                    type: str
                prefix:
                    description: Prefix to prepend to the group name.
                    type: str
                separator:
                    description: Separator to use when joining the key and value.
                    type: str
                    default: ''
      
    version_added: 0.0.1
'''

EXAMPLES = '''
# Minimal example using environment var credentials
plugin: equinix.cloud.metal_device

# Example using constructed features to create groups and set ansible_host
plugin: equinix.cloud.metal_device
# keyed_groups may be used to create custom groups
strict: False
keyed_groups:
  # Add devices to tag_Name groups for each tag
  - prefix: tag
    key: tags
  # Add devices to e.g. equinix_metal_plan_c3_small_x86
  - prefix: equinix_metal_plan
    key: plan
  # Create a group per region e.g. equinix_metal_metro_sv
  - key: metro
    prefix: equinix_metal_metro
  # Create a group per device state e.g. equinix_metal_state_active
  - key: state
    prefix: equinix_metal_state
'''

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.inventory import BaseInventoryPlugin, Constructable, to_safe_group_name

from ansible.module_utils.six import string_types
from ansible_collections.equinix.cloud.plugins.module_utils import (
    action,
)
from ansible_collections.equinix.cloud.plugins.module_utils.metal import (
    metal_client,
    metal_api,
)

EXCLUDE_ATTRIBUTES = [
    "ssh_keys",
]

import os
from typing import List, Dict, Set, Tuple, Any


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
        if super(InventoryModule, self).verify_file(path):
            if path.endswith(('equinix.yml', 'equinix.yaml', 'device.yml', 'device.yaml')):
                return True
        self.display.debug("equinix.cloud inventory filename must end with 'equinix.yml' or 'equinix.yaml'")
        return False

    def parse(self, inventory, loader, path, cache):
        super().parse(inventory, loader, path)

        self._read_config_data(path)

        configured_project_ids = self._get_project_ids()
        devices = self._get_devices_from_project_ids(configured_project_ids)
        projects = set([device['project_id'] for device in devices])
        for project in projects:
            self.inventory.add_group(project)

        for device in devices:
            self.inventory.add_host(label(device), group=device['project_id'])
            first_public_ip = next((ip['address'] for ip in device['ip_addresses'] if ip['public']), None)
            self.inventory.set_variable(label(device), 'ansible_host', first_public_ip)
            self.inventory.add_host(label(device), group='all')
            for k, v in device.items():
                if k not in EXCLUDE_ATTRIBUTES:
                    self.inventory.set_variable(label(device), k, v)

        strict = self.get_option('strict')

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
        self._build_client()
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
