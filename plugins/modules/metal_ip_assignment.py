#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = '''
author: Equinix DevRel Team (@equinix) <support@equinix.com>
description: Asign reserved IPs to Equinix Metal devices.
module: metal_ip_assignment
notes: []
options:
  address:
    description:
    - IP address to assign to the device.
    required: false
    type: str
  customdata:
    description:
    - Custom data about the ip_assignment to create.
    required: false
    type: dict
  device_id:
    description:
    - UUID of the device to assign the IP to.
    required: false
    type: str
  id:
    description:
    - UUID of the ip_assignment.
    required: false
    type: str
  manageable:
    description:
    - Whether the IP address is manageable.
    required: false
    type: bool
requirements: null
short_description: Manage Equinix Metal IP assignments
'''
EXAMPLES = '''
- name: request ip reservation
  equinix.cloud.metal_reserved_ip_block:
    type: public_ipv4
    metro: sv
    quantity: 1
    project_id: '{{ project.id }}'
  register: ip_reservation
- name: available addresses from reservation
  equinix.cloud.metal_available_ips_info:
    reserved_ip_block_id: '{{ ip_reservation.id }}'
    cidr: 32
  register: available_ips
- assert:
    that:
    - available_ips.available | length == 1
- name: create device
  equinix.cloud.metal_device:
    project_id: '{{ project.id }}'
    hostname: device1
    operating_system: ubuntu_20_04
    plan: c3.small.x86
    metro: sv
    state: present
  register: device
- name: assign available IP
  equinix.cloud.metal_ip_assignment:
    device_id: '{{ device.id }}'
    address: '{{ available_ips.available[0] }}'
  register: assignment
'''   
RETURN = '''
metal_ip_assignment:
  description: The assignment object.
  returned: always
  sample:
  - "\n{\n    \"address\": \"147.75.71.192/32\",\n    \"address_family\": 4,\n   \
    \ \"changed\": true,\n    \"cidr\": 32,\n    \"device_id\": \"a8c5dd81-9f7a-4c70-81c6-a168782931ab\"\
    ,\n    \"id\": \"83b5503c-7b7f-4883-9509-b6b728b41491\",\n    \"management\":\
    \ false,\n    \"metro\": \"sv\",\n    \"netmask\": \"255.255.255.255\",\n    \"\
    network\": \"147.75.71.192\",\n    \"public\": true\n}\n"
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
    get_diff,
    getSpecDocMeta,
)

module_spec = dict(
    id=SpecField(
        type=FieldType.string,
        description="UUID of the ip_assignment.",
    ),
    device_id=SpecField(
        type=FieldType.string,
        description="UUID of the device to assign the IP to.",
    ),
    address=SpecField(
        type=FieldType.string,
        description="IP address to assign to the device.",
    ),
    customdata=SpecField(
        type=FieldType.dict,
        description="Custom data about the ip_assignment to create.",
    ),
    manageable=SpecField(
        type=FieldType.bool,
        description="Whether the IP address is manageable.",
    ),
)

specdoc_examples = [
    '''
    - name: request ip reservation
      equinix.cloud.metal_reserved_ip_block:
        type: "public_ipv4"
        metro: "sv"
        quantity: 1
        project_id: "{{ project.id }}"
      register: ip_reservation

    - name: available addresses from reservation
      equinix.cloud.metal_available_ips_info:
        reserved_ip_block_id: "{{ ip_reservation.id }}"
        cidr: 32
      register: available_ips
    
    - assert:
        that:
          - "available_ips.available | length == 1"  


    - name: create device
      equinix.cloud.metal_device:
        project_id: "{{ project.id }}"
        hostname: "device1"
        operating_system: ubuntu_20_04
        plan: c3.small.x86
        metro: sv
        state: present
      register: device

    - name: assign available IP
      equinix.cloud.metal_ip_assignment:
        device_id: "{{ device.id }}"
        address: "{{ available_ips.available[0] }}"
      register: assignment
''',
]

result_sample = [
    """
{
    "address": "147.75.71.192/32",
    "address_family": 4,
    "changed": true,
    "cidr": 32,
    "device_id": "a8c5dd81-9f7a-4c70-81c6-a168782931ab",
    "id": "83b5503c-7b7f-4883-9509-b6b728b41491",
    "management": false,
    "metro": "sv",
    "netmask": "255.255.255.255",
    "network": "147.75.71.192",
    "public": true
}
"""

]

MUTABLE_ATTRIBUTES = [
    k for k, v in module_spec.items() if v.editable
]

SPECDOC_META = getSpecDocMeta(
    short_description='Manage Equinix Metal IP assignments',
    description='Asign reserved IPs to Equinix Metal devices.',
    examples=specdoc_examples,
    options=module_spec,
    return_values={
        "metal_ip_assignment": SpecReturnValue(
            description='The assignment object.',
            type=FieldType.dict,
            sample=result_sample,
        ),
    },
)


def main():
    module = EquinixModule(
        argument_spec=SPECDOC_META.ansible_spec,
        required_one_of=[("device_id", "id")],
        required_by=dict(device_id=["address"]),
    )

    state = module.params.get("state")
    changed = False

    try:
        module.params_syntax_check()
        if module.params.get("id"):
            tolerate_not_found = state == "absent"
            fetched = module.get_by_id("metal_ip_assignment", tolerate_not_found)
        else:
            fetched = module.get_one_from_list(
                "metal_ip_assignment",
                ["device_id", "address"],
            )

        if fetched:
            module.params['id'] = fetched['id']
            if state == "present":
                diff = get_diff(module.params, fetched, MUTABLE_ATTRIBUTES)
                if diff:
                    module.fail_json(msg="Cannot update metal_ip_assignment: %s" % diff)
            else:
                module.delete_by_id("metal_ip_assignment")
                changed = True
        else:
            if state == "present":
                fetched = module.create("metal_ip_assignment")
                if 'id' not in fetched:
                    module.fail_json(msg="UUID not found in ip_assignment creation response")
                changed = True
            else:
                fetched = {}
    except Exception as e:
        tb = traceback.format_exc()
        module.fail_json(msg="Error in metal_ip_assignment: {0}".format(to_native(e)),
                         exception=tb)

    fetched.update({'changed': changed})
    module.exit_json(**fetched)


if __name__ == '__main__':
    main()
