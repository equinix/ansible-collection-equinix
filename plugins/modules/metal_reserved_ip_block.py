#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
module: metal_reserved_ip_block
extends_documentation_fragment:
    - equinix.cloud.metal_common
    - equinix.cloud.state
short_description: Create/delete blocks of reserved IP addresses in a project.
description:
    - When a user provisions first device in a facility, Equinix Metal API automatically allocates IPv6/56 and private IPv4/25 blocks. The new device then gets IPv6 and private IPv4 addresses from those block. It also gets a public IPv4/31 address. Every new device in the project and facility will automatically get IPv6 and private IPv4 addresses from these pre-allocated blocks. The IPv6 and private IPv4 blocks can't be created, only imported. With this resource, it's possible to create either public IPv4 blocks or global IPv4 blocks.
options:
'''

EXAMPLES = r'''
- name: Create new reserved_ip_block
  hosts: localhost
  tasks:
      equinix.cloud.metal_reserved_ip_block:
          name: "new reserved_ip_block"
'''

RETURN = r'''
'''

from ansible.module_utils._text import to_native
import traceback

from ansible_collections.equinix.cloud.plugins.module_utils.equinix import (
    EquinixModule,
    get_diff,
)

MUTABLE_ATTRIBUTES = [
    'tags',
    'description',
]


def main():
    argument_spec = dict(
        state=dict(type='str', default='present', choices=['present', 'absent']),
        id=dict(type='str'),
        wait_for_state=dict(type='str', choices=['pending', 'created']),

        type=dict(type='str', choices=['global_ipv4', 'public_ipv4', 'vrf']),
        quantity=dict(type='int'),
        details=dict(type='str'),
        metro=dict(type='str'),
        customdata=dict(type='str'),
        comments=dict(type='str'),
        vrf_id=dict(type='str'),
        network=dict(type='str'),
        cidr=dict(type='int'),
    )
    module = EquinixModule(
        argument_spec=argument_spec,
        supports_project_id=True,
        supports_tags=True,
        required_one_of=[['id', 'project_id']],
        required_by=dict(project_id=['quantity', 'type']),
        required_if=[
            ['type', 'vrf', ['vrf_id', 'cidr', 'network']],
            ['type', 'public_ipv4', ['metro']]
        ],
    )

    state = module.params.get("state")
    changed = False

    try:
        module.params_syntax_check()
        if module.params.get("id"):
            tolerate_not_found = state == "absent"
            fetched = module.get_by_id("metal_ip_reservation", tolerate_not_found)
        else:
            fetched = module.get_one_from_list(
                "metal_ip_reservation",
                ["type", "metro"],
            )

        if fetched:
            module.params['id'] = fetched['id']
            if state == "present":
                diff = get_diff(module.params, fetched, MUTABLE_ATTRIBUTES)
                if diff:
                    fetched = module.update_by_id(diff, "metal_ip_reservation")
                    changed = True

            else:
                module.delete_by_id("metal_ip_reservation")
                changed = True
        else:
            if state == "present":
                fetched = module.create("metal_ip_reservation")
                if 'id' not in fetched:
                    module.fail_json(msg="UUID not found in metal_reserved_ip_block creation response")
                changed = True
            else:
                fetched = {}
    except Exception as e:
        tb = traceback.format_exc()
        module.fail_json(msg="Error in metal_reserved_ip_block: {0}".format(to_native(e)),
                         exception=tb)

    fetched.update({'changed': changed})
    module.exit_json(**fetched)


if __name__ == '__main__':
    main()
