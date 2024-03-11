#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# DOCUMENTATION, EXAMPLES, and METAL_PROJECT_ARGS are generated by
# ansible_specdoc. Do not edit them directly.

DOCUMENTATION = '''
author: Equinix DevRel Team (@equinix) <support@equinix.com>
description: Manage Projects in Equinix Metal. You can use *id* or *name* to lookup
  a project. If you want to create new project, you must provide *name*.
module: metal_project
notes: []
options:
  backend_transfer_enabled:
    description:
    - Enable backend transfer for the project.
    required: false
    type: bool
  customdata:
    description:
    - Custom data about the project to create.
    required: false
    type: str
  id:
    description:
    - UUID of the project.
    required: false
    type: str
  name:
    description:
    - The name of the project.
    required: false
    type: str
  organization_id:
    description:
    - UUID of the organization containing the project.
    - When not specified, the default organization will be used.
    required: false
    type: str
  payment_method_id:
    description:
    - UUID of payment method to use for the project.
    - When blank, the API assumes default org payment method.
    required: false
    type: str
requirements: null
short_description: Manage Projects in Equinix Metal
'''

EXAMPLES = '''
- name: Create new project
  hosts: localhost
  tasks:
  - equinix.cloud.metal_project:
      name: new project
- name: Create new project within non - default organization
  hosts: localhost
  tasks:
  - equinix.cloud.metal_project:
      name: my org project
      organization_id: a4cc87f9-e00f-48c2-9460-74aa60beb6b0
- name: Remove project by id
  hosts: localhost
  tasks:
  - equinix.cloud.metal_project:
      id: eef49903-7a09-4ca1-af67-4087c29ab5b6
      state: absent
- name: Create new project with non - default billing method
  hosts: localhost
  tasks:
  - equinix.cloud.metal_project:
      name: newer project
      payment_method_id: abf49903-7a09-4ca1-af67-4087c29ab343
'''

RETURN = '''
metal_project:
  description: The module object
  returned: always
  sample:
  - backend_transfer_enabled: false
    changed: false
    customdata: {}
    description: ''
    id: 8624f0f7-75b6-4271-bc64-632b80f87de2
    name: ansible-integration-test-project-csle6t2y-project1_renamed
    organization_id: 70c2f878-9f32-452e-8c69-ab15480e1d99
    payment_method_id: 845b45a3-c565-47e5-b9b6-a86204a73d29
  type: dict
'''

# End of generated documentation

from ansible.module_utils._text import to_native
from ansible_specdoc.objects import (
    SpecField,
    FieldType,
    SpecReturnValue,
)
import traceback

from ansible_collections.equinix.cloud.plugins.module_utils.equinix import (
    EquinixModule,
    get_diff,
    getSpecDocMeta,
)


module_spec = dict(
    id=SpecField(
        type=FieldType.string,
        description=['UUID of the project.'],
    ),
    name=SpecField(
        type=FieldType.string,
        description=['The name of the project.'],
        editable=True,
    ),
    organization_id=SpecField(
        type=FieldType.string,
        description=[
            'UUID of the organization containing the project.',
            'When not specified, the default organization will be used.',
        ],
    ),
    payment_method_id=SpecField(
        type=FieldType.string,
        editable=True,
        description=[
            'UUID of payment method to use for the project.',
            'When blank, the API assumes default org payment method.',
        ],
    ),
    customdata=SpecField(
        type=FieldType.string,
        description=['Custom data about the project to create.'],
        editable=True,
    ),
    backend_transfer_enabled=SpecField(
        type=FieldType.bool,
        description=['Enable backend transfer for the project.'],
        editable=True,
    ),
)


specdoc_examples = [
    '''
- name: Create new project
  hosts: localhost
  tasks:
  - equinix.cloud.metal_project:
      name: "new project"
''', '''
- name: Create new project within non - default organization
  hosts: localhost
  tasks:
  - equinix.cloud.metal_project:
      name: "my org project"
      organization_id: "a4cc87f9-e00f-48c2-9460-74aa60beb6b0"
''', '''
- name: Remove project by id
  hosts: localhost
  tasks:
  - equinix.cloud.metal_project:
      id: "eef49903-7a09-4ca1-af67-4087c29ab5b6"
      state: absent
''', '''
- name: Create new project with non - default billing method
  hosts: localhost
  tasks:
  - equinix.cloud.metal_project:
      name: "newer project"
      payment_method_id: "abf49903-7a09-4ca1-af67-4087c29ab343"
''',
]

result_sample = [
{
  "backend_transfer_enabled": False,
  "changed": False,
  "customdata": {},
  "description": "",
  "id": "8624f0f7-75b6-4271-bc64-632b80f87de2",
  "name": "ansible-integration-test-project-csle6t2y-project1_renamed",
  "organization_id": "70c2f878-9f32-452e-8c69-ab15480e1d99",
  "payment_method_id": "845b45a3-c565-47e5-b9b6-a86204a73d29"
},
]

MUTABLE_ATTRIBUTES = [
    k for k, v in module_spec.items() if v.editable
]

SPECDOC_META = getSpecDocMeta(
    short_description='Manage Projects in Equinix Metal',
    description=(
        'Manage Projects in Equinix Metal. '
        'You can use *id* or *name* to lookup a project. '
        'If you want to create new project, you must provide *name*.'
    ),
    examples=specdoc_examples,
    options=module_spec,
    return_values={
        "metal_project": SpecReturnValue(
            description='The module object',
            type=FieldType.dict,
            sample=result_sample,
        ),
    },
)


def main():
    module = EquinixModule(
        argument_spec=SPECDOC_META.ansible_spec,
        required_one_of=[("name", "id")],
    )

    state = module.params.get("state")
    changed = False

    try:
        module.params_syntax_check()
        if module.params.get("id"):
            tolerate_not_found = state == "absent"
            fetched = module.get_by_id("metal_project", tolerate_not_found)
        else:
            fetched = module.get_one_from_list(
                "metal_project",
                ["name"],
            )

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
