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

from ansible.module_utils._text import to_native
import traceback

from ansible_specdoc.objects import (
    SpecField,
    FieldType,
    SpecReturnValue,
)

from ansible_collections.equinix.cloud.plugins.module_utils.equinix import (
    EquinixModule,
    getSpecDocMeta,
)

module_spec = dict(
    device_id=SpecField(
        type=FieldType.string,
        description="UUID of the device to list ip_assignments for.",
        required=True,
    ),
)

specdoc_examples = [
    '''
    ''',
]

result_sample = [
    '''
    ''',
]

SPECDOC_META = getSpecDocMeta(
    short_description="Gather IP address assignments for a device",
    description="Gather IP address assignments for a device",
    examples=specdoc_examples,
    options=module_spec,
    return_values={
        "resources": SpecReturnValue(
            description='Found resources',
            type=FieldType.dict,
            sample=result_sample,
        ),
    },
)

def main():
    module = EquinixModule(
        argument_spec=SPECDOC_META.ansbile_spec,
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
