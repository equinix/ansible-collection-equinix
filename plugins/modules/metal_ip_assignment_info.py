#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r'''
module: metal_ip_assignment_info
extends_documentation_fragment:
    - equinix.cloud.metal_common
    - equinix.cloud.filters
short_description: Gather information about Equinix Metal ip_assignments
description:
    - Gather information about Equinix Metal ip_assignments.
options:
    organization_id:
        description:
            - UUID of the organization to list ip_assignments for.
        type: str
'''

EXAMPLES = r'''
- name: Gather information about all ip_assignments
  hosts: localhost
  tasks:
      - equinix.cloud.metal_ip_assignment_info

- name: Gather information about all ip_assignments in organization
  hosts: localhost
  tasks:
      - equinix.cloud.metal_ip_assignment_info:
            organization_id: 2a5122b9-c323-4d5c-b53c-9ad3f54273e7
'''

RETURN = r'''
resources:
    description: List of ip_assignment resources. See docs of equinix.cloud.metal_reserved_ip_block for description of each item.
    returned: always
    type: list

'''

import traceback
from ansible.module_utils._text import to_native

from ansible_collections.equinix.cloud.plugins.module_utils.equinix import (
    EquinixModule,
)


def main():
    argument_spec = dict(
        device_id=dict(type='str', required=True),
    )
    module = EquinixModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )
    try:
        module.params_syntax_check()
        return_value = {'resources': module.get_list(
            "metal_ip_assignment")
        }
    except Exception as e:
        tr = traceback.format_exc()
        module.fail_json(msg=to_native(e), exception=tr)
    module.exit_json(**return_value)


if __name__ == '__main__':
    main()
