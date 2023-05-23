#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# DOCUMENTATION, EXAMPLES, and METAL_ssh_key_ARGS are generated by
# ansible_specdoc. Do not edit them directly.

DOCUMENTATION = '''
author: Equinix DevRel Team (@equinix) <support@equinix.com>
description: Manage personal SSH keys in Equinix Metal. Read more about personal and
  project SSH keys in [Equinix Metal documentation](https://deploy.equinix.com/developers/docs/metal/accounts/ssh-keys/#personal-keys-vs-project-keys).
  You can use *id* or *label* to lookup a SSH key. If you want to create new personal
  SSH key, you must provide a *label* and a public key in the *key* field.
module: metal_ssh_key
notes: []
options:
  id:
    description:
    - UUID of the ssh_key.
    required: false
    type: str
  key:
    description:
    - The public key of the ssh_key.
    required: false
    type: str
  label:
    description:
    - The name of the ssh_key.
    required: false
    type: str
requirements: null
short_description: Manage personal SSH keys in Equinix Metal
'''
EXAMPLES = '''
- name: Create new ssh_key
  hosts: localhost
  tasks:
  - equinix.cloud.metal_ssh_key:
      label: new ssh_key
      key: ssh-dss AAAAB3NzaC1kc3MAAACBAPLEVntPO3L7VUbEwWZ2ErkQJ3KJ8o9kFXJrPcpvVfdNag4jIhQDqbtAUgUy6BclhhbfH9l5nlGTprrpEFkxm/GL91qJUX6xrPkDMjMqx2wSKa4YraReOrCOfkqqEkC3o3G/gYSuvTzLgp2rmPiflypftZyzNM4JZT8jDwFGotJhAAAAFQDPk43bayONtUxjkAcOf+6zP1qb6QAAAIBZHHH0tIlth5ot+Xa/EYuB/M4qh77EkrWUbER0Kki7suskw/ffdKQ0y/v+ZhoAHtBU7BeE3HmP98Vrha1i4cOU+A7DCqV+lK/a+5LoEpua0M2M+VzNSGluYuV4qGpAOxNh3mxUi2R7yXxheN1oks1ROJ/bqkF4BJQXU9Nv49GkZgAAAIByWcsFeOitvzyDaNJOZzEHv9fqGuj0L3maRVWb6O47HGzlMzniIy8WjL2dfgm2/ek+NxVR/yFnYTKDPr6+0uqSD/cb4eHaFbIj7v+k7H8hA1Ioz+duJ1ONAjn6KwneXxOXu15bYIR49P7Go0s9jCdSAP/r9NE5TnE3yiRiQzgEzw==
        tomk@node
- name: Remove ssh_key by id
  hosts: localhost
  tasks:
  - equinix.cloud.metal_ssh_key:
      id: eef49903-7a09-4ca1-af67-4087c29ab5b6
      state: absent
'''
RETURN = '''
metal_ssh_key:
  description: The module object
  returned: always
  sample:
  - "\n{\n  \"fingerprint\": \"98:9c:35:ed:f9:75:5b:52:e2:70:50:22:ea:77:5b:b6\",\n\
    \  \"id\": \"260c8ef0-2667-4446-9c9d-a156f7234da6\",\n  \"key\": \"ssh-dss AAAAB3NzaC1kc3MAAACBAPLEVntPO3L7VUbEwWZ2ErkQJ3KJ8o9kFXJrPcpvVfdNag4jIhQDqbtAUgUy6BclhhbfH9l5nlGTprrpEFkxm/GL91qJUX6xrPkDMjMqx2wSKa4YraReOrCOfkqqEkC3o3G/gYSuvTzLgp2rmPiflypftZyzNM4JZT8jDwFGotJhAAAAFQDPk43bayONtUxjkAcOf+6zP1qb6QAAAIBZHHH0tIlth5ot+Xa/EYuB/M4qh77EkrWUbER0Kki7suskw/ffdKQ0y/v+ZhoAHtBU7BeE3HmP98Vrha1i4cOU+A7DCqV+lK/a+5LoEpua0M2M+VzNSGluYuV4qGpAOxNh3mxUi2R7yXxheN1oks1ROJ/bqkF4BJQXU9Nv49GkZgAAAIByWcsFeOitvzyDaNJOZzEHv9fqGuj0L3maRVWb6O47HGzlMzniIy8WjL2dfgm2/ek+NxVR/yFnYTKDPr6+0uqSD/cb4eHaFbIj7v+k7H8hA1Ioz+duJ1ONAjn6KwneXxOXu15bYIR49P7Go0s9jCdSAP/r9NE5TnE3yiRiQzgEzw==\
    \ tomk@xps\",\n  \"label\": \"fsdfsdf\"\n}\n"
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
        description=['UUID of the ssh_key.'],
    ),
    label=SpecField(
        type=FieldType.string,
        description=['The name of the ssh_key.'],
        editable=True,
    ),
    key=SpecField(
        type=FieldType.string,
        description=['The public key of the ssh_key.'],
        editable=True,
    ),
)


specdoc_examples = [
    '''
- name: Create new ssh_key
  hosts: localhost
  tasks:
  - equinix.cloud.metal_ssh_key:
      label: "new ssh_key"
      key: "ssh-dss AAAAB3NzaC1kc3MAAACBAPLEVntPO3L7VUbEwWZ2ErkQJ3KJ8o9kFXJrPcpvVfdNag4jIhQDqbtAUgUy6BclhhbfH9l5nlGTprrpEFkxm/GL91qJUX6xrPkDMjMqx2wSKa4YraReOrCOfkqqEkC3o3G/gYSuvTzLgp2rmPiflypftZyzNM4JZT8jDwFGotJhAAAAFQDPk43bayONtUxjkAcOf+6zP1qb6QAAAIBZHHH0tIlth5ot+Xa/EYuB/M4qh77EkrWUbER0Kki7suskw/ffdKQ0y/v+ZhoAHtBU7BeE3HmP98Vrha1i4cOU+A7DCqV+lK/a+5LoEpua0M2M+VzNSGluYuV4qGpAOxNh3mxUi2R7yXxheN1oks1ROJ/bqkF4BJQXU9Nv49GkZgAAAIByWcsFeOitvzyDaNJOZzEHv9fqGuj0L3maRVWb6O47HGzlMzniIy8WjL2dfgm2/ek+NxVR/yFnYTKDPr6+0uqSD/cb4eHaFbIj7v+k7H8hA1Ioz+duJ1ONAjn6KwneXxOXu15bYIR49P7Go0s9jCdSAP/r9NE5TnE3yiRiQzgEzw== tomk@node"  
''', '''
- name: Remove ssh_key by id
  hosts: localhost
  tasks:
  - equinix.cloud.metal_ssh_key:
      id: "eef49903-7a09-4ca1-af67-4087c29ab5b6"
      state: absent
''',
]

result_sample = ['''
{
  "fingerprint": "98:9c:35:ed:f9:75:5b:52:e2:70:50:22:ea:77:5b:b6",
  "id": "260c8ef0-2667-4446-9c9d-a156f7234da6",
  "key": "ssh-dss AAAAB3NzaC1kc3MAAACBAPLEVntPO3L7VUbEwWZ2ErkQJ3KJ8o9kFXJrPcpvVfdNag4jIhQDqbtAUgUy6BclhhbfH9l5nlGTprrpEFkxm/GL91qJUX6xrPkDMjMqx2wSKa4YraReOrCOfkqqEkC3o3G/gYSuvTzLgp2rmPiflypftZyzNM4JZT8jDwFGotJhAAAAFQDPk43bayONtUxjkAcOf+6zP1qb6QAAAIBZHHH0tIlth5ot+Xa/EYuB/M4qh77EkrWUbER0Kki7suskw/ffdKQ0y/v+ZhoAHtBU7BeE3HmP98Vrha1i4cOU+A7DCqV+lK/a+5LoEpua0M2M+VzNSGluYuV4qGpAOxNh3mxUi2R7yXxheN1oks1ROJ/bqkF4BJQXU9Nv49GkZgAAAIByWcsFeOitvzyDaNJOZzEHv9fqGuj0L3maRVWb6O47HGzlMzniIy8WjL2dfgm2/ek+NxVR/yFnYTKDPr6+0uqSD/cb4eHaFbIj7v+k7H8hA1Ioz+duJ1ONAjn6KwneXxOXu15bYIR49P7Go0s9jCdSAP/r9NE5TnE3yiRiQzgEzw== tomk@xps",
  "label": "fsdfsdf"
}
''']

MUTABLE_ATTRIBUTES = [
    k for k, v in module_spec.items() if v.editable
]

SPECDOC_META = getSpecDocMeta(
    short_description='Manage personal SSH keys in Equinix Metal',
    description=(
        'Manage personal SSH keys in Equinix Metal. '
        'Read more about personal and project SSH keys in [Equinix Metal documentation](https://deploy.equinix.com/developers/docs/metal/accounts/ssh-keys/#personal-keys-vs-project-keys). '
        'You can use *id* or *label* to lookup a SSH key. '
        'If you want to create new personal SSH key, you must provide a *label* and a public key in the *key* field.'
    ),
    examples=specdoc_examples,
    options=module_spec,
    return_values={
        "metal_ssh_key": SpecReturnValue(
            description='The module object',
            type=FieldType.dict,
            sample=result_sample,
        ),
    },
)


def main():
    module = EquinixModule(
        argument_spec=SPECDOC_META.ansible_spec,
        required_one_of=[("label", "id")],
        required_together=[("label", "key")],
    )

    state = module.params.get("state")
    changed = False

    try:
        module.params_syntax_check()
        if module.params.get("id"):
            tolerate_not_found = state == "absent"
            fetched = module.get_by_id("metal_ssh_key", tolerate_not_found)
        else:
            fetched = module.get_one_from_list(
                "metal_ssh_key",
                ["key"],
            )

        if fetched:
            module.params['id'] = fetched['id']
            if state == "present":
                diff = get_diff(module.params, fetched, MUTABLE_ATTRIBUTES)
                if diff:
                    fetched = module.update_by_id(diff, "metal_ssh_key")
                    changed = True

            else:
                module.delete_by_id("metal_ssh_key")
                changed = True
        else:
            if state == "present":
                fetched = module.create("metal_ssh_key")
                changed = True
            else:
                fetched = {}
    except Exception as e:
        tb = traceback.format_exc()
        module.fail_json(msg="Error in metal_ssh_key: {0}".format(to_native(e)),
                         exception=tb)

    fetched.update({'changed': changed})
    module.exit_json(**fetched)


if __name__ == '__main__':
    main()
