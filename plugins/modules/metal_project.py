#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Nurfet Becirevic <nurfet.becirevic@gmail.com>
# Copyright: (c) 2021, Jason DeTiberus (@detiber) <jdetiberus@equinix.com>
# Copyright: (c) 2023, Tomas Karasek <tom.to.the.k@gmail.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
module: metal_project
extends_documentation_fragment:
    - equinix.cloud.metal_common
    - equinix.cloud.state
short_description: Create/delete a project in Equinix Metal
description:
    - Create/delete a project in Equinix Metal.
options:
    name:
        description:
            - The name of the project.
        type: str
    id:
        description:
            - UUID of the project.
        type: str
    organization_id:
        description:
            - UUID of the organization to create the project in.
        type: str
    payment_method_id:
        description:
            - UUID of payment method to use for the project. When blank, the API assumes default org payment method.
        type: str
    customdata:
        description:
            - Custom data about the project to create.
        type: str
    backend_transfer_enabled:
        description:
            - Enable backend transfer for the project.
        type: bool
'''

EXAMPLES = r'''
- name: Create new project
  hosts: localhost
  tasks:
      equinix.cloud.metal_project:
          name: "new project"

- name: Create new project within non-default organization
  hosts: localhost
  tasks:
      equinix.cloud.metal_project:
          name: "my org project"
          organization_id: a4cc87f9-e00f-48c2-9460-74aa60beb6b0

- name: Remove project by id
  hosts: localhost
  tasks:
      equinix.cloud.metal_project:
          state: absent
          id: eef49903-7a09-4ca1-af67-4087c29ab5b6

- name: Create new project with non-default billing method
  hosts: localhost
  tasks:
      equinix.cloud.metal_project:
          name: "newer project"
          payment_method_id: "abf49903-7a09-4ca1-af67-4087c29ab343"
'''

RETURN = r'''
id:
    description: UUID of the project.
    returned: I(state=present)
    type: str
    sample: "eef49903-7a09-4ca1-af67-4087c29ab5b6"
name:
    description: Name of the project.
    returned: I(state=present)
    type: str
    sample: "new project"
organization_id:
    description: UUID of the organization the project belongs to.
    returned: I(state=present)
    type: str
    sample: "a4cc87f9-e00f-48c2-9460-74aa60beb6b0"
payment_method_id:
    description: UUID of the payment method used for the project.
    returned: I(state=present)
    type: str
    sample: "abf49903-7a09-4ca1-af67-4087c29ab343"
customdata:
    description: Custom data about the project.
    returned: I(state=present)
    type: str
    sample: '{"setting": 12}'
backend_transfer_enabled:
    description: Whether backend transfer is enabled for the project.
    returned: I(state=present)
    type: bool
    sample: true
'''

from ansible.module_utils._text import to_native
import traceback

from ansible_collections.equinix.cloud.plugins.module_utils.equinix import (
    EquinixModule,
    get_diff,
)

MUTABLE_ATTRIBUTES = [
    'name',
    'payment_method_id',
    'customdata',
    'backend_transfer_enabled',
]


def main():
    argument_spec = dict(
        state=dict(type='str', default='present', choices=['present', 'absent']),
        name=dict(type='str'),
        id=dict(type='str'),
        organization_id=dict(type='str'),
        payment_method_id=dict(type='str'),
        customdata=dict(type='str'),
        backend_transfer_enabled=dict(type='bool'),
    )
    module = EquinixModule(
        argument_spec=argument_spec,
        required_one_of=[("name", "id")],
    )

    state = module.params.get("state")
    changed = False

    try:
        if module.params.get("id"):
            tolerate_not_found = state == "absent"
            fetched = module.get_by_id("metal_project", tolerate_not_found)
        else:
            name = module.params.get("name")
            fetched = module.get_one_from_list(
                "metal_project",
                "name",
                {"name": name})

        if fetched:
            module.params['id'] = fetched['id']
            if state == "present":
                diff = get_diff(module.params, fetched, MUTABLE_ATTRIBUTES)
                if diff:
                    fetched = module.update_by_id(diff, "metal_project")
                    changed = True

            else:
                module.delete_by_id("metal_project")
                changed = True
        else:
            if state == "present":
                organization_id = module.params.get("organization_id")
                if organization_id:
                    fetched = module.create("metal_organization_project")
                else:
                    fetched = module.create("metal_project")
                if 'id' not in fetched:
                    module.fail_json(msg="UUID not found in project creation response")
                changed = True

                # backend_transfer_enabled need to be explicitly set by update
                if module.params.get("backend_transfer_enabled"):
                    module.params['id'] = fetched['id']
                    fetched = module.update_by_id({"backend_transfer_enabled": True}, "metal_project")

                # TODO: add support for bgp_config once we have a module
            else:
                fetched = {}
    except Exception as e:
        tb = traceback.format_exc()
        module.fail_json(msg="Error in metal_project: {0}".format(to_native(e)),
                         exception=tb)

    fetched.update({'changed': changed})
    module.exit_json(**fetched)


if __name__ == '__main__':
    main()
