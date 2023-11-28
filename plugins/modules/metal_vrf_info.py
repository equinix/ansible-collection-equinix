#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# DOCUMENTATION, EXAMPLES, and RETURN are generated by
# ansible_specdoc. Do not edit them directly.

DOCUMENTATION = '''
author: Equinix DevRel Team (@equinix) <support@equinix.com>
description: Gather information about Equinix Metal resources
module: metal_vrf_info
notes: []
options:
  name:
    description:
    - Filter VRF on substring in name attribute.
    required: false
    type: str
  project_id:
    description:
    - Project ID where the VRF will be deployed.
    required: false
    type: str
requirements: null
short_description: Gather information about Equinix Metal resources
'''
EXAMPLES = '''
- name: Gather information about all resources in parent resource
  hosts: localhost
  tasks:
  - equinix.cloud.metal_vrf_info:
      project_id: 2a5122b9-c323-4d5c-b53c-9ad3f54273e7
'''
RETURN = '''
resources:
  description: Found resources
  returned: always
  sample:
  - "\n\n[  \n  {\n    \"id\": \"31d3ae8b-bd5a-41f3-a420-055211345cc7\",\n    \"name\"\
    : \"ansible-integration-test-resource-csle6t2y-resource2\",\n    \"parent_resource_id\"\
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
        description=['Filter VRF on substring in name attribute.'],
    ),
    project_id=SpecField(
        type=FieldType.string,
        description=['Project ID where the VRF will be deployed.'],
    ),
)

specdoc_examples = ['''
- name: Gather information about all resources in parent resource
  hosts: localhost
  tasks:
      - equinix.cloud.metal_vrf_info:
          project_id: 2a5122b9-c323-4d5c-b53c-9ad3f54273e7
''', '''
''',
                    ]

result_sample = ['''

[  
  {
    "id": "31d3ae8b-bd5a-41f3-a420-055211345cc7",
    "name": "ansible-integration-test-resource-csle6t2y-resource2",
    "parent_resource_id": "845b45a3-c565-47e5-b9b6-a86204a73d29"
  }
]''',
]

SPECDOC_META = getSpecDocMeta(
    short_description="Gather VRFs",
    description=(
        'Gather information about Equinix VRFs'
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
        return_value = {'resources': module.get_list("metal_vrf")}
    except Exception as e:
        tr = traceback.format_exc()
        module.fail_json(msg=to_native(e), exception=tr)
    module.exit_json(**return_value)


if __name__ == '__main__':
    main()
