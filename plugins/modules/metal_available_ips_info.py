#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = '''
author: Equinix DevRel Team (@equinix) <support@equinix.com>
description: Get list of avialable IP addresses from a reserved IP block
module: metal_available_ips_info
notes: []
options:
  cidr:
    description:
    - CIDR of the reserved IP block to list available IPs for.
    required: false
    type: str
  reserved_ip_block_id:
    description:
    - UUID of the reserved IP block to list available IPs for.
    required: true
    type: str
requirements:
- python >= 3
- equinix_metal >= 0.0.1
short_description: Get list of avialable IP addresses from a reserved IP block
'''
EXAMPLES = '''
name: available addresses from reservation
equinix.cloud.metal_available_ips_info:
  reserved_ip_block_id: '{{ ip_reservation.id }}'
  cidr: 32
  register: available_ips
'''
RETURN = '''
available:
  description: Available IP addresses from the reservation.
  returned: always
  sample:
  - "\n{\n    \"available\": [\n        \"147.75.71.192/32\"\n    ],\n}\n"
  type: dict
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
    reserved_ip_block_id=SpecField(
        type=FieldType.string,
        description="UUID of the reserved IP block to list available IPs for.",
        required=True,
    ),
    cidr=SpecField(
        type=FieldType.string,
        description="CIDR of the reserved IP block to list available IPs for.",
    ),
)

specdoc_examples = [
    '''
name: available addresses from reservation
equinix.cloud.metal_available_ips_info:
  reserved_ip_block_id: "{{ ip_reservation.id }}"
  cidr: 32
  register: available_ips
''',
]

result_sample = [
    '''
{
    "available": [
        "147.75.71.192/32"
    ],
}
''',
]

SPECDOC_META = getSpecDocMeta(
    short_description="Get list of avialable IP addresses from a reserved IP block",
    description="Get list of avialable IP addresses from a reserved IP block",
    examples=specdoc_examples,
    options=module_spec,
    return_values={
        "available": SpecReturnValue(
            description='Available IP addresses from the reservation.',
            type=FieldType.dict,
            sample=result_sample,
        ),
    },
)


def main():
    module = EquinixModule(
        argument_spec=SPECDOC_META.ansible_spec,
        supports_check_mode=True,
    )
    try:
        module.params_syntax_check()
        return_value = {'available': module.get_list(
            "metal_available_ip")
        }
    except Exception as e:
        tr = traceback.format_exc()
        module.fail_json(msg=to_native(e), exception=tr)
    module.exit_json(**return_value)


if __name__ == '__main__':
    main()
