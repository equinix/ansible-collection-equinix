# (c) 2016, Tomas Karasek <tom.to.the.k@gmail.com>
# (c) 2016, Matt Baldwin <baldwin@stackpointmetal.com>
# (c) 2016, Thibaud Morel l'Horset <teebes@gmail.com>
# (c) 2021, Jason DeTiberus (@detiber) <jdetiberus@equinix.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: metal_device_info
extends_documentation_fragment:
    - equinix.cloud.metal_common
    - equinix.cloud.filters
short_description: Gather information about Equinix Metal devices
description:
    - Gather information about Equinix Metal devices.
options:
    project_id:
        description:
            - UUID of the project to list devices in.
        type: str
    organization_id:
        description:
            - UUID of the organization to list devices in.
        type: str
'''

EXAMPLES = r'''
- name: Gather information about all devices
  hosts: localhost
  tasks:
      - equinix.metal.device_info:

- name: Gather information about devices in a particular project using ID
  hosts: localhost
  tasks:
      - equinix.metal.device_info:
            project_id: 173d7f11-f7b9-433e-ac40-f1571a38037a

- name: Gather information about devices in a particular organization using ID
  hosts: localhost
  tasks:
      - equinix.metal.device_info:
            organization_id: 173d7f11-f7b9-433e-ac40-f1571a38037a

- name: Gather information about devices with "webserver" in hostname in a project
  hosts: localhost
  tasks:
      - equinix.metal.device_info:
            project_id: 173d7f11-f7b9-433e-ac40-f1571a38037a
            filters:
                hostname: webserver
'''


RETURN = '''
resources:
    description: Information about each device that was found
    type: list
    sample: '[{"hostname": "my-server.com", "id": "2a5122b9-c323-4d5c-b53c-9ad3f54273e7",
            "public_ipv4": "147.229.15.12", "private-ipv4": "10.0.15.12",
            "tags": [], "locked": false, "state": "provisioning",
            "public_ipv6": ""2604:1380:2:5200::3"}]'
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
        project_id=dict(type='str'),
        organization_id=dict(type='str'),
    )
    module = EquinixModule(
        argument_spec=argument_spec,
        required_one_of=[('project_id', 'organization_id')],
        mutually_exclusive=[('project_id', 'organization_id')],
        supports_check_mode=True,
    )
    try:
        filters = module.params.get('filters')
        resource_type = "metal_project_device"
        if module.params.get('organization_id'):
            resource_type = "metal_organization_device"
        return_value = {'resources': module.get_list(resource_type, filters)}

    except Exception as e:
        tr = traceback.format_exc()
        module.fail_json(msg=to_native(e), exception=tr)
    module.exit_json(**return_value)


if __name__ == '__main__':
    main()
