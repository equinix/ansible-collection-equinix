#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r'''
module: metal_reserved_ip_block_info
extends_documentation_fragment:
    - equinix.cloud.metal_common
    - equinix.cloud.filters
short_description: Gather information about Equinix Metal reserved_ip_blocks
description:
    - Gather information about Equinix Metal reserved_ip_blocks.
options:
    organization_id:
        description:
            - UUID of the organization to list reserved_ip_blocks for.
        type: str
'''

EXAMPLES = r'''
- name: Gather information about all reserved_ip_blocks
  hosts: localhost
  tasks:
      - equinix.cloud.metal_reserved_ip_block_info

- name: Gather information about all reserved_ip_blocks in organization
  hosts: localhost
  tasks:
      - equinix.cloud.metal_reserved_ip_block_info:
            organization_id: 2a5122b9-c323-4d5c-b53c-9ad3f54273e7
'''

RETURN = r'''
resources:
    description: List of reserved_ip_block resources. See docs of equinix.cloud.metal_reserved_ip_block for description of each item.
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
        type=dict(type='str', required=True, choices=[
            'public_ipv4', 'public_ipv6', 'private_ipv4', 'global_ipv4', 'vrf',
        ]),
        project_id=dict(type='str', required=True),
        metro=dict(type='str'),
        filters=dict(type='dict'),
    )
    module = EquinixModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )
    try:
        module.params_syntax_check()
        filters = module.params.get('filters')
        typ = module.params.get('type')
        metro = module.params.get('metro')
        if (metro is not None) & (typ == 'global_ipv4'):
            module.fail_json(msg="metro is not valid parameter for global_ipv4")
        return_value = {'resources': module.get_list(
            "metal_ip_reservation", filters)
        }
    except Exception as e:
        tr = traceback.format_exc()
        module.fail_json(msg=to_native(e), exception=tr)
    module.exit_json(**return_value)


if __name__ == '__main__':
    main()
