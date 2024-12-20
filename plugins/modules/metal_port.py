#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# DOCUMENTATION, EXAMPLES, and RETURN are generated by
# ansible_specdoc. Do not edit them directly.

DOCUMENTATION = r"""
author: Equinix DevRel Team (@equinix) <support@equinix.com>
description: This module doesn't create a resource in Equinix Metal, but rather provides
  finer control for [Layer 2 networking](https://deploy.equinix.com/developers/docs/metal/layer2-networking/overview/).
module: metal_port
notes: []
options:
  bonded:
    description:
    - Whether the port should be bonded.
    required: true
    type: bool
  id:
    description:
    - UUID of the port.
    required: true
    type: str
  layer2:
    description:
    - Whether the port should be in Layer 2 mode.
    required: false
    type: bool
  native_vlan_id:
    description:
    - UUID of native VLAN of the port
    required: false
    type: str
  vlan_ids:
    description:
    - UUIDs of VLANs that should be assigned to the port
    required: false
    type: list
requirements: null
short_description: Manage a device port in Equinix Metal
"""
EXAMPLES = r"""
- name: Convert port to layer 2
  hosts: localhost
  tasks:
  - equinix.cloud.metal_port:
      id: device port ID
      bonded: true
      layer2: true
'''
RETURN = '''
metal_port:
  description: The Metal device port
  returned: always
  sample:
    bonded: true
    id: 7624f0f7-75b6-4271-bc64-632b80f87de2
    layer2: true
  type: dict
"""

from ansible.module_utils._text import to_native
from ansible_specdoc.objects import (
    SpecField,
    FieldType,
    SpecReturnValue,
)
import time
import traceback

from ansible_collections.equinix.cloud.plugins.module_utils.equinix import (
    EquinixModule,
    get_diff,
    getSpecDocMeta,
)

import equinix.services.metalv1 as equinix_metal

module_spec = dict(
    id=SpecField(
        type=FieldType.string,
        description=['UUID of the port.'],
        required=True,
    ),
    bonded=SpecField(
        type=FieldType.bool,
        description=['Whether the port should be bonded.'],
        editable=True,
    ),
    layer2=SpecField(
        type=FieldType.bool,
        description=['Whether the port should be in Layer 2 mode.'],
        editable=True,
    ),
    vlan_ids=SpecField(
        type=FieldType.list,
        description=["UUIDs of VLANs that should be assigned to the port"],
        editable=True,
    ),
    native_vlan_id=SpecField(
        type=FieldType.string,
        description=["UUID of native VLAN of the port"],
        editable=True,
    ),
)


specdoc_examples = [
    '''
- name: capture port ids for my_device
  set_fact:
    bond_port_id: "{{ my_device.network_ports | selectattr('name', 'match', 'bond0') | map(attribute='id') | first }}"
    eth1_port_id: "{{ my_device.network_ports | selectattr('name', 'match', 'eth1') | map(attribute='id') | first }}"

- name: convert to layer2 bonded mode
  equinix.cloud.metal_port:
    id: "{{ bond_port_id }}"
    bonded: true
    layer2: true
    vlan_ids:
      - "<some_vlan_id>"
      - "<another_vlan_id>"

- name: assign native VLAN by UUID
  equinix.cloud.metal_port:
    id: "{{ bond_port_id }}"
    bonded: true
    layer2: true
    native_vlan_id: "{{ test_vlan1.id }}"

- name: convert to hybrid bonded mode
  equinix.cloud.metal_port:
    id: "{{ bond_port_id }}"
    bonded: true
    layer2: false

- name: convert to layer2 unbonded mode
  equinix.cloud.metal_port:
    id: "{{ bond_port_id }}"
    bonded: false
    layer2: true

- name: convert to hybrid unbonded mode
  equinix.cloud.metal_port:
    id: "{{ eth1_port_id }}"
    bonded: true
    layer2: false
''',
]

return_values = [
{
  "id": "7624f0f7-75b6-4271-bc64-632b80f87de2",
  "bonded": True,
  "layer2": True,
}
]

MUTABLE_ATTRIBUTES = [
    k for k, v in module_spec.items() if v.editable
]

SPECDOC_META = getSpecDocMeta(
    short_description='Manage a device port in Equinix Metal',
    description=(
        'This module doesn\'t create a resource in Equinix Metal, '
        'but rather provides finer control for '
        '[Layer 2 networking](https://deploy.equinix.com/developers/docs/metal/layer2-networking/overview/).'
    ),
    examples=specdoc_examples,
    options=module_spec,
    return_values={
        "metal_port": SpecReturnValue(
            description='The Metal device port',
            type=FieldType.dict,
            sample=return_values,
        ),
    },
)

l2_types = {"layer2-individual", "layer2-bonded"}
l3_types = {"layer3", "hybrid", "hybrid-bonded"}
port_includes = {"native_virtual_network", "virtual_networks"}

def _convert_layer3(module, port):
    port_convert_layer3_input = {
        "request_ips": [
            {"address_family": 4, "public": True},
            {"address_family": 4, "public": False},
            {"address_family": 6, "public": True},
        ]
    }

    return equinix_metal.PortsApi(module.equinix_metal_client).convert_layer3(port.id, port_includes, port_convert_layer3_input)

def _create_and_wait_for_batch(module, port, vlan_assignments, timeout: int):
    stop_time = time.perf_counter() + timeout
    ports_api = equinix_metal.PortsApi(module.equinix_metal_client)
    batch = ports_api.create_port_vlan_assignment_batch(port.id, { "vlan_assignments": vlan_assignments })

    while time.perf_counter() < stop_time:
        batch = ports_api.find_port_vlan_assignment_batch_by_port_id_and_batch_id(port.id, batch.id)

        if batch.state == "failed":
            module.fail_json("vlan assignment batch {0} provisioning failed: {1}".format(batch.id, batch.error_messages))
        if batch.state == "completed":
            return ports_api.find_port_by_id(port.id, port_includes)
        time.sleep(5)

    module.fail_json("vlan assignment batch {0} status is '{1}' after timeout".format(batch.id, batch.state))

def main():
    module = EquinixModule(
        argument_spec=SPECDOC_META.ansible_spec,
    )

    state = module.params.get("state")

    if state != "present":
        module.fail_json(msg="Metal ports cannot be deleted")

    changed = False

    try:
        module.params_syntax_check()
        ports_api = equinix_metal.PortsApi(module.equinix_metal_client)
        port = ports_api.find_port_by_id(module.params.get('id'), port_includes)

        wants_layer2 = module.params.get('layer2')
        specified_layer2 = wants_layer2 is not None
        wants_bonded = module.params.get('bonded')
        wants_vlan_ids = module.params.get('vlan_ids')
        wants_native_vlan_id = module.params.get('native_vlan_id')

        if port:
            # confirm that parameters are consistent
            is_bond_port = (port.type == "NetworkBondPort")
            if specified_layer2 and not is_bond_port:
                module.fail_json(msg="layer2 flag can be set only for bond ports")

            # disbond if needed
            if port.data.bonded and not wants_bonded:
                if is_bond_port and port.network_type in l3_types:
                    module.fail_json(msg="layer 3 bond ports cannot be unbonded")
                port = ports_api.disbond_port(port.id, None, port_includes)
                changed = True

            # convert to L2 if needed
            if wants_layer2:
                if port.network_type not in l2_types:
                    port = ports_api.convert_layer2(port.id, {}, port_includes)
                    changed = True

            # bond if needed
            if wants_bonded and not port.data.bonded:
                port = ports_api.bond_port(port.id, None, port_includes)
                changed = True

            # convert to L3 if needed
            if not wants_layer2 and port.network_type in l2_types:
                port = _convert_layer3(module, port)
                changed = True

            # batch VLAN assignment changes, add and remove
            if wants_vlan_ids is not None:
                current_vlan_ids = [vlan.id for vlan in port.virtual_networks]
                vlans_to_remove = [{ "vlan": id, "state": "unassigned" } for id in current_vlan_ids if not id in wants_vlan_ids]
                vlans_to_add = [{ "vlan": id, "state": "assigned" } for id in wants_vlan_ids if not id in current_vlan_ids]
                vlan_assignments = vlans_to_remove + vlans_to_add

                if len(vlan_assignments) > 0:
                    port = _create_and_wait_for_batch(module, port, vlan_assignments, 1800)
                    changed = True

            # update native VLAN ID
            current_native_vlan_id = port.native_virtual_network.id if port.native_virtual_network is not None else None
            if wants_native_vlan_id != current_native_vlan_id:
                if wants_native_vlan_id is None:
                    port = ports_api.delete_native_vlan(port.id, port_includes)
                    changed = True
                else:
                    port = ports_api.assign_native_vlan(port.id, wants_native_vlan_id, port_includes)
                    changed = True
        else:
            module.fail_json(msg="Could not find metal_port with ID {0}".format(module.params['id']))
    except Exception as e:
        tb = traceback.format_exc()
        module.fail_json(msg="Error in metal_port: {0}".format(to_native(e)),
                         exception=tb)
    
    result = port.to_dict()
    result.update({'changed': changed})
    module.exit_json(**result)

if __name__ == '__main__':
    main()