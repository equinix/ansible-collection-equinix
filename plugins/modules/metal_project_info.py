#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Nurfet Becirevic <nurfet.becirevic@gmail.com>
# Copyright: (c) 2021, Jason DeTiberus (@detiber) <jdetiberus@equinix.com>
# Copyright: (c) 2023, Tomas Karasek <tom.to.the.k@gmail.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: metal_project_info
extends_documentation_fragment:
    - equinix.cloud.metal_common
short_description: Gather information about Equinix Metal projects
description:
    - Gather information about Equinix Metal projects.
options:
    name:
        description:
            - Substring to match against project names.
        type: str   
    organization_id:
        description:
            - UUID of the organization to list projects for.
        type: str
'''

EXAMPLES = '''
# All the examples assume that you have your Equinix Metal API token in env var METAL_API_TOKEN.
# You can also pass it to the api_token parameter of the module instead.

- name: Gather information about all projects
  hosts: localhost
  tasks:
    - equinix.metal.project_info:


- name: Gather information about a particular project using ID
  hosts: localhost
  tasks:
    - equinix.metal.project_info:
        ids:
          - 173d7f11-f7b9-433e-ac40-f1571a38037a
'''

RETURN = '''
resources:
    description: Information about each project that was found
    type: list
    sample: '[{"name": "my-project", "id": "2a5122b9-c323-4d5c-b53c-9ad3f54273e7"}]'
    returned: always
'''

import traceback
from ansible.module_utils._text import to_native

from ansible_collections.equinix.cloud.plugins.module_utils.equinix import (
    EquinixModule,
)


def main():
    argument_spec = dict(
        name=dict(type='str'),
        organization_id=dict(type='str'),
    )
    module = EquinixModule(
        argument_spec=argument_spec,
    )
    try:
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
