#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# DOCUMENTATION, EXAMPLES, and RETURN are generated by
# ansible_specdoc. Do not edit them directly.

DOCUMENTATION = r"""
author: Equinix DevRel Team (@equinix) <support@equinix.com>
description: Gather project SSH keys. Read more about project vs project SSH keys
  in [Equinix Metal documentation](https://deploy.equinix.com/developers/docs/metal/identity-access-management/ssh-keys/).
module: metal_project_ssh_key_info
notes: []
options:
  label:
    description:
    - Name to search for in existing keys.
    required: false
    type: str
  project_id:
    description:
    - Name of the project for listing project keys.
    required: false
    type: str
requirements: null
short_description: Gather project SSH keys.
"""
EXAMPLES = r"""
- set_fact:
    desired_name_substring: tkarasek
- name: list project ssh keys
  equinix.cloud.metal_project_ssh_key_info: null
  register: ssh_keys_listed
- name: filter found ssh keys
  set_fact:
    both_ssh_keys_listed: '{{ ssh_keys_listed.resources | selectattr(''label'', ''match'',
      desired_name_substring) }}'
"""
RETURN = r"""
resources:
  description: Found resources
  returned: always
  sample:
  - fingerprint: 70:c1:73:8b:3f:2f:a4:18:ea:4d:79:13:52:7b:c4:3e
    id: 6edfcbc2-17e5-4221-9eac-2f40dbe60daf
    key: ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAt5gwVMhwcCrxyxpMEKwiS0xgit3PIIEgVXt6SQHc8eONq0mYJJ5TOBNTnySqXd9RtSv/Jbf5Aq9BzBGWeoZ6sZfKwh984Ip35StJtjXtyIOlY3skovndtupBIwlGXgX/WQzyLr+G/+Yu9/nhdxQi801PDZnDvKoeomM0rMD29nV+m0ud+GrtsAt6VFul2PxqpypZ1TYviyED6IKo7rgQsQDkE9QHcNdfT1FZWiJbfP7o8TIurQJcAXg+MtLoc8rKKcxFMeZ9FSydgtTC7nP1h558RtECGWiUgaBPI7TpBmcdMtbEfAiBoGT17GWnT8qmy2u5xnEKPD9Qft4w4fjfpw==
    label: tkarasek
    project_id: b8c6c653-3c96-446e-987e-9c4d12f25353
  - fingerprint: ba:70:af:b3:0f:0e:7f:e5:eb:97:e2:27:b1:f5:6f:94
    id: d00c596d-b42a-44a7-ac14-e299b85e73d3
    key: ssh-dss AAAAB3NzaC1kc3MAAACBAOpXVtmc0Bla98bt0o5/Zj7sb4mHIukgVFZu7F32R3VK1cEKB4rEE8uS0oLS/qMRLue45TWVJwRMYGlPjt3p/VyraelxoyJZLuITIsqa5hBc9w0oTlB5Bmbkn16umW96WCaWEoq/aitpocbRChTiP5biI6FyQTQlIHDaYzBDOi11AAAAFQDUXy7cmuzphDpJSYYTiudiUhVokwAAAIEAyUQ9m8qL/1HPkFe6jbXAvtSSmW27F4c+G2xR5HizaHQzXgBOxPcsOsY17KTU+Ddbg+OF9soWNwSpm9pyVjVmNGqH3S8R1pwvuJF/O2Asy1m6wpWhbPw8JdEBW7WHoptBpfuzJoS2LOzJUEmUu4Eb+xS237KG1d1BVny/49KAoH0AAACBAJKBSsm9Xey0fUN6vYtTQgoYeGxxj/LqAIAOs/TpCxZDntly860y/SzHYai8x48k4t7whENY1CJ41fpMcPlz8xIsrNP3326Wbr0ExwOIvJKAVN1YLYqF8NXWzaVrjo5WbSeI8PiWTYemvLAujVxZssIrApTZBhp55nnwge6K1zTG
      tomk@air
    label: ansible-integration-test-ssh_key-ztiapihf-ssh_key1_renamed
    project_id: b8c6c653-3c96-446e-987e-9c4d12f25353
  type: dict
"""

# End

from ansible.module_utils._text import to_native
from ansible_specdoc.objects import SpecField, FieldType, SpecReturnValue
import traceback

from ansible_collections.equinix.cloud.plugins.module_utils.equinix import (
    EquinixModule,
    getSpecDocMeta,
)

module_spec = dict(
    label=SpecField(
        type=FieldType.string,
        description=["Name to search for in existing keys."],
        required=False,
    ),
    project_id=SpecField(
        type=FieldType.string,
        description=["Name of the project for listing project keys."],
        required=False,
    ),
)

specdoc_examples = [
    """

- set_fact:
    desired_name_substring: "tkarasek"

- name: list project ssh keys
  equinix.cloud.metal_project_ssh_key_info:
  register: ssh_keys_listed

- name: filter found ssh keys
  set_fact:
    both_ssh_keys_listed: "{{ ssh_keys_listed.resources | selectattr('label', 'match', desired_name_substring) }}"
""",
]

return_values = [
    {
        "fingerprint": "70:c1:73:8b:3f:2f:a4:18:ea:4d:79:13:52:7b:c4:3e",
        "id": "6edfcbc2-17e5-4221-9eac-2f40dbe60daf",
        "key": "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAt5gwVMhwcCrxyxpMEKwiS0xgit3PIIEgVXt6SQHc8eONq0mYJJ5TOBNTnySqXd9RtSv/Jbf5Aq9BzBGWeoZ6sZfKwh984Ip35StJtjXtyIOlY3skovndtupBIwlGXgX/WQzyLr+G/+Yu9/nhdxQi801PDZnDvKoeomM0rMD29nV+m0ud+GrtsAt6VFul2PxqpypZ1TYviyED6IKo7rgQsQDkE9QHcNdfT1FZWiJbfP7o8TIurQJcAXg+MtLoc8rKKcxFMeZ9FSydgtTC7nP1h558RtECGWiUgaBPI7TpBmcdMtbEfAiBoGT17GWnT8qmy2u5xnEKPD9Qft4w4fjfpw==",
        "label": "tkarasek",
        "project_id": "b8c6c653-3c96-446e-987e-9c4d12f25353"
    },
    {
        "fingerprint": "ba:70:af:b3:0f:0e:7f:e5:eb:97:e2:27:b1:f5:6f:94",
        "id": "d00c596d-b42a-44a7-ac14-e299b85e73d3",
        "key": "ssh-dss AAAAB3NzaC1kc3MAAACBAOpXVtmc0Bla98bt0o5/Zj7sb4mHIukgVFZu7F32R3VK1cEKB4rEE8uS0oLS/qMRLue45TWVJwRMYGlPjt3p/VyraelxoyJZLuITIsqa5hBc9w0oTlB5Bmbkn16umW96WCaWEoq/aitpocbRChTiP5biI6FyQTQlIHDaYzBDOi11AAAAFQDUXy7cmuzphDpJSYYTiudiUhVokwAAAIEAyUQ9m8qL/1HPkFe6jbXAvtSSmW27F4c+G2xR5HizaHQzXgBOxPcsOsY17KTU+Ddbg+OF9soWNwSpm9pyVjVmNGqH3S8R1pwvuJF/O2Asy1m6wpWhbPw8JdEBW7WHoptBpfuzJoS2LOzJUEmUu4Eb+xS237KG1d1BVny/49KAoH0AAACBAJKBSsm9Xey0fUN6vYtTQgoYeGxxj/LqAIAOs/TpCxZDntly860y/SzHYai8x48k4t7whENY1CJ41fpMcPlz8xIsrNP3326Wbr0ExwOIvJKAVN1YLYqF8NXWzaVrjo5WbSeI8PiWTYemvLAujVxZssIrApTZBhp55nnwge6K1zTG tomk@air",
        "label": "ansible-integration-test-ssh_key-ztiapihf-ssh_key1_renamed",
        "project_id": "b8c6c653-3c96-446e-987e-9c4d12f25353"
    }
]

SPECDOC_META = getSpecDocMeta(
    short_description="Gather project SSH keys.",
    description=(
        "Gather project SSH keys. Read more about project vs project SSH keys in [Equinix Metal documentation](https://deploy.equinix.com/developers/docs/metal/identity-access-management/ssh-keys/)."
    ),
    examples=specdoc_examples,
    options=module_spec,
    return_values={
        "resources": SpecReturnValue(
            description="Found resources",
            type=FieldType.dict,
            sample=return_values,
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
        return_value = {"resources": module.get_list("metal_project_ssh_key")}
    except Exception as e:
        tr = traceback.format_exc()
        module.fail_json(msg=to_native(e), exception=tr)
    module.exit_json(**return_value)


if __name__ == "__main__":
    main()
