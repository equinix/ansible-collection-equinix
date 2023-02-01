# Copyright: (c) 2019, Nurfet Becirevic <nurfet.becirevic@gmail.com>
# Copyright: (c) 2021, Jason DeTiberus (@detiber) <jdetiberus@equinix.com>
# Copyright: (c) 2023, Tomas Karasek <tom.to.the.k@gmail.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
module: metal_project_info
extends_documentation_fragment:
    - equinix.cloud.metal_common
    - equinix.cloud.filters
short_description: Gather information about Equinix Metal projects
description:
    - Gather information about Equinix Metal projects.
options:
    organization_id:
        description:
            - UUID of the organization to list projects for.
        type: str
'''

EXAMPLES = r'''
- name: Gather information about all projects
  hosts: localhost
  tasks:
      - equinix.cloud.metal_project_info

- name: Gather information about all projects in organization
  hosts: localhost
  tasks:
      - equinix.cloud.metal_project_info:
            organization_id: 2a5122b9-c323-4d5c-b53c-9ad3f54273e7
'''

RETURN = r'''
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
        filters=dict(type='dict'),
        organization_id=dict(type='str'),
    )
    module = EquinixModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )
    try:
        filters = module.params.get('filters')
        if module.params.get('organization_id'):
            return_value = {'resources': module.get_list("metal_organization_project", filters)}
        else:
            return_value = {'resources': module.get_list("metal_project", filters)}
    except Exception as e:
        tr = traceback.format_exc()
        module.fail_json(msg=to_native(e), exception=tr)
    module.exit_json(**return_value)


if __name__ == '__main__':
    main()
