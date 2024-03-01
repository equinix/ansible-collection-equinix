#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = '''
author: Equinix DevRel Team (@equinix) <support@equinix.com>
description: Gather IP address assignments for a device
module: metal_ip_assignment_info
notes: []
options:
  device_id:
    description:
    - UUID of the device to list ip_assignments for.
    required: true
    type: str
requirements: null
short_description: Gather IP address assignments for a device
'''
EXAMPLES = '''
- name: assignment info
  equinix.cloud.metal_ip_assignment_info:
    device_id: '{{ device.id }}'
  register: assignment_info
'''
RETURN = '''
resources:
  description: Found resources
  returned: always
  sample:
  - address: 147.75.55.115/31
    address_family: 4
    cidr: 31
    device_id: 8ea9837a-6d19-4607-b166-f7f7bb04b022
    id: 38deafaa-0a1d-4e32-b8cd-417e2ba958db
    management: true
    metro: da
    netmask: 255.255.255.254
    network: 147.75.55.114
    public: true
  - address: 145.40.102.107/32
    address_family: 4
    cidr: 32
    device_id: 8ea9837a-6d19-4607-b166-f7f7bb04b022
    id: c30b9d28-755c-4016-8480-b90497643c29
    management: false
    metro: da
    netmask: 255.255.255.255
    network: 145.40.102.107
    public: true
  - address: 2604:1380:4641:5b00::1/127
    address_family: 6
    cidr: 127
    device_id: 8ea9837a-6d19-4607-b166-f7f7bb04b022
    id: ad2f9b8c-f73f-4ae7-9016-f78b316f7ad6
    management: true
    netmask: ffff:ffff:ffff:ffff:ffff:ffff:ffff:fffe
    network: '2604:1380:4641:5b00::'
    public: true
  - address: 10.70.50.129/31
    address_family: 4
    cidr: 31
    device_id: 8ea9837a-6d19-4607-b166-f7f7bb04b022
    id: 4d81a406-3fb2-4ac4-9e03-2a498c5788e1
    management: true
    netmask: 255.255.255.254
    network: 10.70.50.128
    public: false
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
    device_id=SpecField(
        type=FieldType.string,
        description="UUID of the device to list ip_assignments for.",
        required=True,
    ),
)

specdoc_examples = [
    '''
- name: assignment info 
  equinix.cloud.metal_ip_assignment_info:
    device_id: "{{ device.id }}"
  register: assignment_info
''',
]

result_sample = [
    {
        "address": "147.75.55.115/31",
        "address_family": 4,
        "cidr": 31,
        "device_id": "8ea9837a-6d19-4607-b166-f7f7bb04b022",
        "id": "38deafaa-0a1d-4e32-b8cd-417e2ba958db",
        "management": True,
        "metro": "da",
        "netmask": "255.255.255.254",
        "network": "147.75.55.114",
        "public": True
    },
    {
        "address": "145.40.102.107/32",
        "address_family": 4,
        "cidr": 32,
        "device_id": "8ea9837a-6d19-4607-b166-f7f7bb04b022",
        "id": "c30b9d28-755c-4016-8480-b90497643c29",
        "management": False,
        "metro": "da",
        "netmask": "255.255.255.255",
        "network": "145.40.102.107",
        "public": True
    },
    {
        "address": "2604:1380:4641:5b00::1/127",
        "address_family": 6,
        "cidr": 127,
        "device_id": "8ea9837a-6d19-4607-b166-f7f7bb04b022",
        "id": "ad2f9b8c-f73f-4ae7-9016-f78b316f7ad6",
        "management": True,
        "netmask": "ffff:ffff:ffff:ffff:ffff:ffff:ffff:fffe",
        "network": "2604:1380:4641:5b00::",
        "public": True
    },
    {
        "address": "10.70.50.129/31",
        "address_family": 4,
        "cidr": 31,
        "device_id": "8ea9837a-6d19-4607-b166-f7f7bb04b022",
        "id": "4d81a406-3fb2-4ac4-9e03-2a498c5788e1",
        "management": True,
        "netmask": "255.255.255.254",
        "network": "10.70.50.128",
        "public": False
    }
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
        argument_spec=SPECDOC_META.ansible_spec,
        is_info=True,
    )
    try:
        module.params_syntax_check()
        return_value = {'resources': module.get_list("metal_ip_assignment")}
    except Exception as e:
        tr = traceback.format_exc()
        module.fail_json(msg=to_native(e), exception=tr)
    module.exit_json(**return_value)


if __name__ == '__main__':
    main()
