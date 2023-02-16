#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: metal_device_info
extends_documentation_fragment:
    - equinix.cloud.metal_common
    - equinix.cloud.filters
short_description: Gather information about Equinix Metal devices
description:
    - Gather information about Equinix Metal devices.
options:
    project_id:
        description:
            - UUID of the project to list devices in.
        type: str
    organization_id:
        description:
            - UUID of the organization to list devices in.
        type: str
'''

EXAMPLES = r'''
- name: Gather information about all devices
  hosts: localhost
  tasks:
      - equinix.metal.device_info:

- name: Gather information about devices in a particular project using ID
  hosts: localhost
  tasks:
      - equinix.metal.device_info:
            project_id: 173d7f11-f7b9-433e-ac40-f1571a38037a

- name: Gather information about devices in a particular organization using ID
  hosts: localhost
  tasks:
      - equinix.metal.device_info:
            organization_id: 173d7f11-f7b9-433e-ac40-f1571a38037a

- name: Gather information about devices with "webserver" in hostname in a project
  hosts: localhost
  tasks:
      - equinix.metal.device_info:
            project_id: 173d7f11-f7b9-433e-ac40-f1571a38037a
            filters:
                hostname: webserver
'''


RETURN = '''
resources:
    description: Information about each device that was found. See docs of equinix.cloud.metal_device for description of each item.
    type: list
    returned: always
'''

import traceback
from ansible.module_utils._text import to_native

from ansible_collections.equinix.cloud.plugins.module_utils.equinix import (
    EquinixModule,
)


def main():
    argument_spec = dict(
        filters=dict(type='dict'),
        project_id=dict(type='str'),
        organization_id=dict(type='str'),
    )
    module = EquinixModule(
        argument_spec=argument_spec,
        required_one_of=[('project_id', 'organization_id')],
        mutually_exclusive=[('project_id', 'organization_id')],
        supports_check_mode=True,
    )
    try:
        module.params_syntax_check()
        filters = module.params.get('filters')
        resource_type = "metal_project_device"
        if module.params.get('organization_id'):
            resource_type = "metal_organization_device"
        return_value = {'resources': module.get_list(resource_type, filters)}

    except Exception as e:
        tr = traceback.format_exc()
        module.fail_json(msg=to_native(e), exception=tr)
    module.exit_json(**return_value)


if __name__ == '__main__':
    main()
