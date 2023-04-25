#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# DOCUMENTATION, EXAMPLES, and METAL_PROJECT_ARGS are generated by
# ansible_specdoc. Do not edit them directly.

DOCUMENTATION = '''
author: Equinix DevRel Team (@equinix) <support@equinix.com>
description: Gather information about Equinix Metal projects
module: metal_project_info
notes: []
options:
  name:
    description:
    - The name of the project.
    required: false
    type: str
  organization_id:
    description:
    - UUID of the organization containing the project.
    required: false
    type: str
requirements:
- python >= 3
- equinix_metal >= 0.0.1
short_description: Gather information about Equinix Metal projects
'''
EXAMPLES = '''
- name: Gather information about all projects
  hosts: localhost
  tasks:
  - equinix.cloud.metal_project_info
- name: Gather information about all projects in an organization
  hosts: localhost
  tasks:
  - equinix.cloud.metal_project_info:
      organization_id: 2a5122b9-c323-4d5c-b53c-9ad3f54273e7
'''
RETURN = '''
resources:
  description: Found resources
  returned: always
  sample:
  - "\n\n[  \n  {\n    \"backend_transfer_enabled\": false,\n    \"customdata\": {},\n\
    \    \"description\": \"\",\n    \"id\": \"31d3ae8b-bd5a-41f3-a420-055211345cc7\"\
    ,\n    \"name\": \"ansible-integration-test-project-csle6t2y-project2\",\n   \
    \ \"organization_id\": \"70c2f878-9f32-452e-8c69-ab15480e1d99\",\n    \"payment_method_id\"\
    : \"845b45a3-c565-47e5-b9b6-a86204a73d29\"\n  }\n]"
  type: dict
'''

# End

from ansible.module_utils._text import to_native
from ansible_specdoc.objects import SpecField, FieldType, SpecReturnValue
import traceback

from ansible_collections.equinix.cloud.plugins.module_utils.equinix import (
    EquinixModule,
    getSpecDocMeta,
)

module_spec = dict(
    name=SpecField(
        type=FieldType.string,
        description=['The name of the project.'],
    ),
    organization_id=SpecField(
        type=FieldType.string,
        description=['UUID of the organization containing the project.'],
    ),
)

specdoc_examples = ['''
- name: Gather information about all projects
  hosts: localhost
  tasks:
      - equinix.cloud.metal_project_info
''', '''
- name: Gather information about all projects in an organization
  hosts: localhost
  tasks:
      - equinix.cloud.metal_project_info:
          organization_id: 2a5122b9-c323-4d5c-b53c-9ad3f54273e7
''',
                    ]

result_sample = ['''

[  
  {
    "backend_transfer_enabled": false,
    "customdata": {},
    "description": "",
    "id": "31d3ae8b-bd5a-41f3-a420-055211345cc7",
    "name": "ansible-integration-test-project-csle6t2y-project2",
    "organization_id": "70c2f878-9f32-452e-8c69-ab15480e1d99",
    "payment_method_id": "845b45a3-c565-47e5-b9b6-a86204a73d29"
  }
]''',
]

SPECDOC_META = getSpecDocMeta(
    short_description="Gather information about Equinix Metal projects",
    description=(
        'Gather information about Equinix Metal projects'
    ),
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
        if module.params.get('organization_id'):
            return_value = {'resources': module.get_list("metal_organization_project")}
        else:
            return_value = {'resources': module.get_list("metal_project")}
    except Exception as e:
        tr = traceback.format_exc()
        module.fail_json(msg=to_native(e), exception=tr)
    module.exit_json(**return_value)


if __name__ == '__main__':
    main()
