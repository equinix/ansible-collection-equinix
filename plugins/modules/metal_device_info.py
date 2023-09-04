#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
author: Equinix DevRel Team (@equinix) <support@equinix.com>
description: Select list of Equinix Metal devices
module: metal_device_info
notes: []
options:
  hostname:
    description:
    - Hostname to look up a device.
    required: false
    type: str
  organization_id:
    description:
    - UUID of the organization containing devices.
    required: false
    type: str
  project_id:
    description:
    - UUID of the project containing devices.
    required: false
    type: str
requirements: null
short_description: Select list of Equinix Metal devices
''' 
EXAMPLES = '''
- name: Gather information about all devices
  hosts: localhost
  tasks:
  - equinix.metal.device_info: null
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
      hostname: webserver
'''
RETURN = '''
resources:
  description: List of devices
  returned: always
  sample:
  - "\n[\n    {\n        \"always_pxe\": false,\n        \"billing_cycle\": \"hourly\"\
    ,\n        \"customdata\": {},\n        \"facility\": \"sv15\",\n        \"hardware_reservation_id\"\
    : \"\",\n        \"hostname\": \"ansible-integration-test-device-yi4fbuo4-dev2\"\
    ,\n        \"id\": \"6dee3ce4-72f4-4d92-a035-dff5237b2841\",\n        \"ip_addresses\"\
    : [\n            {\n                \"address\": \"147.75.71.193\",\n        \
    \        \"address_family\": 4,\n                \"public\": true\n          \
    \  },\n            {\n                \"address\": \"2604:1380:45e3:2c00::3\"\
    ,\n                \"address_family\": 6,\n                \"public\": true\n\
    \            },\n            {\n                \"address\": \"10.67.168.18\"\
    ,\n                \"address_family\": 4,\n                \"public\": false\n\
    \            }\n        ],\n        \"ipxe_script_url\": \"\",\n        \"locked\"\
    : false,\n        \"metal_state\": \"active\",\n        \"metro\": \"sv\",\n \
    \       \"operating_system\": \"ubuntu_20_04\",\n        \"plan\": \"c3.small.x86\"\
    ,\n        \"project_id\": \"6ac17ea6-a304-4b01-a1f3-f13a7371cfab\",\n       \
    \ \"spot_instance\": false,\n        \"spot_price_max\": 0.0,\n        \"ssh_keys\"\
    : [\n            {\n                \"href\": \"/metal/v1/ssh-keys/1ffe4e4b-eaf9-45d9-a268-0d81af71ae55\"\
    ,\n                \"id\": \"1ffe4e4b-eaf9-45d9-a268-0d81af71ae55\"\n        \
    \    },\n            {\n                \"href\": \"/metal/v1/ssh-keys/d122d4e4-4832-41c8-abbb-40182930becf\"\
    ,\n                \"id\": \"d122d4e4-4832-41c8-abbb-40182930becf\"\n        \
    \    },\n            {\n                \"href\": \"/metal/v1/ssh-keys/b0f196c0-9cf2-4cb7-96c5-403b81ff6813\"\
    ,\n                \"id\": \"b0f196c0-9cf2-4cb7-96c5-403b81ff6813\"\n        \
    \    },\n            {\n                \"href\": \"/metal/v1/ssh-keys/4b011c75-e642-4f6d-85f4-590a5956ad28\"\
    ,\n                \"id\": \"4b011c75-e642-4f6d-85f4-590a5956ad28\"\n        \
    \    },\n            {\n                \"href\": \"/metal/v1/ssh-keys/217ff08c-057a-4933-8efe-2e9f723fbb5f\"\
    ,\n                \"id\": \"217ff08c-057a-4933-8efe-2e9f723fbb5f\"\n        \
    \    },\n            {\n                \"href\": \"/metal/v1/ssh-keys/10968e80-b234-469b-acb8-c5002b4111a4\"\
    ,\n                \"id\": \"10968e80-b234-469b-acb8-c5002b4111a4\"\n        \
    \    },\n            {\n                \"href\": \"/metal/v1/ssh-keys/6ff0810b-135c-48cf-ac68-b365bdfd338c\"\
    ,\n                \"id\": \"6ff0810b-135c-48cf-ac68-b365bdfd338c\"\n        \
    \    },\n            {\n                \"href\": \"/metal/v1/ssh-keys/6a71d7e1-db14-4dfd-9014-46032b507538\"\
    ,\n                \"id\": \"6a71d7e1-db14-4dfd-9014-46032b507538\"\n        \
    \    },\n            {\n                \"href\": \"/metal/v1/ssh-keys/413e2347-f89c-40af-ba9e-0864f2fde990\"\
    ,\n                \"id\": \"413e2347-f89c-40af-ba9e-0864f2fde990\"\n        \
    \    },\n            {\n                \"href\": \"/metal/v1/ssh-keys/9308b337-702a-4774-8351-37dfb8c90a57\"\
    ,\n                \"id\": \"9308b337-702a-4774-8351-37dfb8c90a57\"\n        \
    \    }\n        ],\n        \"tags\": [],\n        \"userdata\": \"\"\n    },\n\
    \    {\n        \"always_pxe\": false,\n        \"billing_cycle\": \"hourly\"\
    ,\n        \"customdata\": {},\n        \"facility\": \"sv15\",\n        \"hardware_reservation_id\"\
    : \"\",\n        \"hostname\": \"ansible-integration-test-device-yi4fbuo4-dev1\"\
    ,\n        \"id\": \"71a90c54-e0eb-414f-9ea2-9c39ecb32319\",\n        \"ip_addresses\"\
    : [\n            {\n                \"address\": \"139.178.94.207\",\n       \
    \         \"address_family\": 4,\n                \"public\": true\n         \
    \   },\n            {\n                \"address\": \"2604:1380:45e3:2c00::1\"\
    ,\n                \"address_family\": 6,\n                \"public\": true\n\
    \            },\n            {\n                \"address\": \"10.67.168.2\",\n\
    \                \"address_family\": 4,\n                \"public\": false\n \
    \           }\n        ],\n        \"ipxe_script_url\": \"\",\n        \"locked\"\
    : false,\n        \"metal_state\": \"active\",\n        \"metro\": \"sv\",\n \
    \       \"operating_system\": \"ubuntu_20_04\",\n        \"plan\": \"c3.small.x86\"\
    ,\n        \"project_id\": \"6ac17ea6-a304-4b01-a1f3-f13a7371cfab\",\n       \
    \ \"spot_instance\": false,\n        \"spot_price_max\": 0.0,\n        \"ssh_keys\"\
    : [\n            {\n                \"href\": \"/metal/v1/ssh-keys/1ffe4e4b-eaf9-45d9-a268-0d81af71ae55\"\
    ,\n                \"id\": \"1ffe4e4b-eaf9-45d9-a268-0d81af71ae55\"\n        \
    \    },\n            {\n                \"href\": \"/metal/v1/ssh-keys/d122d4e4-4832-41c8-abbb-40182930becf\"\
    ,\n                \"id\": \"d122d4e4-4832-41c8-abbb-40182930becf\"\n        \
    \    },\n            {\n                \"href\": \"/metal/v1/ssh-keys/b0f196c0-9cf2-4cb7-96c5-403b81ff6813\"\
    ,\n                \"id\": \"b0f196c0-9cf2-4cb7-96c5-403b81ff6813\"\n        \
    \    },\n            {\n                \"href\": \"/metal/v1/ssh-keys/4b011c75-e642-4f6d-85f4-590a5956ad28\"\
    ,\n                \"id\": \"4b011c75-e642-4f6d-85f4-590a5956ad28\"\n        \
    \    },\n            {\n                \"href\": \"/metal/v1/ssh-keys/217ff08c-057a-4933-8efe-2e9f723fbb5f\"\
    ,\n                \"id\": \"217ff08c-057a-4933-8efe-2e9f723fbb5f\"\n        \
    \    },\n            {\n                \"href\": \"/metal/v1/ssh-keys/10968e80-b234-469b-acb8-c5002b4111a4\"\
    ,\n                \"id\": \"10968e80-b234-469b-acb8-c5002b4111a4\"\n        \
    \    },\n            {\n                \"href\": \"/metal/v1/ssh-keys/6ff0810b-135c-48cf-ac68-b365bdfd338c\"\
    ,\n                \"id\": \"6ff0810b-135c-48cf-ac68-b365bdfd338c\"\n        \
    \    },\n            {\n                \"href\": \"/metal/v1/ssh-keys/6a71d7e1-db14-4dfd-9014-46032b507538\"\
    ,\n                \"id\": \"6a71d7e1-db14-4dfd-9014-46032b507538\"\n        \
    \    },\n            {\n                \"href\": \"/metal/v1/ssh-keys/413e2347-f89c-40af-ba9e-0864f2fde990\"\
    ,\n                \"id\": \"413e2347-f89c-40af-ba9e-0864f2fde990\"\n        \
    \    },\n            {\n                \"href\": \"/metal/v1/ssh-keys/9308b337-702a-4774-8351-37dfb8c90a57\"\
    ,\n                \"id\": \"9308b337-702a-4774-8351-37dfb8c90a57\"\n        \
    \    }\n        ],\n        \"tags\": [],\n        \"userdata\": \"\"\n    }\n\
    ]\n"
  type: list
'''

from ansible.module_utils._text import to_native
from ansible_specdoc.objects import SpecField, FieldType, SpecDocMeta, SpecReturnValue
import traceback

from ansible_collections.equinix.cloud.plugins.module_utils.equinix import (
    EquinixModule,
    getSpecDocMeta,
)

module_spec = dict(
    hostname=SpecField(
        type=FieldType.string,
        description=['Hostname to look up a device.'],
    ),
    project_id=SpecField(
        type=FieldType.string,
        description=['UUID of the project containing devices.'],
    ),
    organization_id=SpecField(
        type=FieldType.string,
        description=['UUID of the organization containing devices.'],
    ),
)

specdoc_examples = [
    '''
- name: Gather information about all devices
  hosts: localhost
  tasks:
      - equinix.metal.device_info:
''', '''
- name: Gather information about devices in a particular project using ID
  hosts: localhost
  tasks:
      - equinix.metal.device_info:
            project_id: 173d7f11-f7b9-433e-ac40-f1571a38037a
''', '''
- name: Gather information about devices in a particular organization using ID
  hosts: localhost
  tasks:
      - equinix.metal.device_info:
            organization_id: 173d7f11-f7b9-433e-ac40-f1571a38037a
''', '''
- name: Gather information about devices with "webserver" in hostname in a project
  hosts: localhost
  tasks:
      - equinix.metal.device_info:
            project_id: 173d7f11-f7b9-433e-ac40-f1571a38037a
            hostname: webserver
''',
]

result_sample = [
'''
[
    {
        "always_pxe": false,
        "billing_cycle": "hourly",
        "customdata": {},
        "facility": "sv15",
        "hardware_reservation_id": "",
        "hostname": "ansible-integration-test-device-yi4fbuo4-dev2",
        "id": "6dee3ce4-72f4-4d92-a035-dff5237b2841",
        "ip_addresses": [
            {
                "address": "147.75.71.193",
                "address_family": 4,
                "public": true
            },
            {
                "address": "2604:1380:45e3:2c00::3",
                "address_family": 6,
                "public": true
            },
            {
                "address": "10.67.168.18",
                "address_family": 4,
                "public": false
            }
        ],
        "ipxe_script_url": "",
        "locked": false,
        "metal_state": "active",
        "metro": "sv",
        "operating_system": "ubuntu_20_04",
        "plan": "c3.small.x86",
        "project_id": "6ac17ea6-a304-4b01-a1f3-f13a7371cfab",
        "spot_instance": false,
        "spot_price_max": 0.0,
        "ssh_keys": [
            {
                "href": "/metal/v1/ssh-keys/1ffe4e4b-eaf9-45d9-a268-0d81af71ae55",
                "id": "1ffe4e4b-eaf9-45d9-a268-0d81af71ae55"
            },
            {
                "href": "/metal/v1/ssh-keys/d122d4e4-4832-41c8-abbb-40182930becf",
                "id": "d122d4e4-4832-41c8-abbb-40182930becf"
            },
            {
                "href": "/metal/v1/ssh-keys/b0f196c0-9cf2-4cb7-96c5-403b81ff6813",
                "id": "b0f196c0-9cf2-4cb7-96c5-403b81ff6813"
            },
            {
                "href": "/metal/v1/ssh-keys/4b011c75-e642-4f6d-85f4-590a5956ad28",
                "id": "4b011c75-e642-4f6d-85f4-590a5956ad28"
            },
            {
                "href": "/metal/v1/ssh-keys/217ff08c-057a-4933-8efe-2e9f723fbb5f",
                "id": "217ff08c-057a-4933-8efe-2e9f723fbb5f"
            },
            {
                "href": "/metal/v1/ssh-keys/10968e80-b234-469b-acb8-c5002b4111a4",
                "id": "10968e80-b234-469b-acb8-c5002b4111a4"
            },
            {
                "href": "/metal/v1/ssh-keys/6ff0810b-135c-48cf-ac68-b365bdfd338c",
                "id": "6ff0810b-135c-48cf-ac68-b365bdfd338c"
            },
            {
                "href": "/metal/v1/ssh-keys/6a71d7e1-db14-4dfd-9014-46032b507538",
                "id": "6a71d7e1-db14-4dfd-9014-46032b507538"
            },
            {
                "href": "/metal/v1/ssh-keys/413e2347-f89c-40af-ba9e-0864f2fde990",
                "id": "413e2347-f89c-40af-ba9e-0864f2fde990"
            },
            {
                "href": "/metal/v1/ssh-keys/9308b337-702a-4774-8351-37dfb8c90a57",
                "id": "9308b337-702a-4774-8351-37dfb8c90a57"
            }
        ],
        "tags": [],
        "userdata": ""
    },
    {
        "always_pxe": false,
        "billing_cycle": "hourly",
        "customdata": {},
        "facility": "sv15",
        "hardware_reservation_id": "",
        "hostname": "ansible-integration-test-device-yi4fbuo4-dev1",
        "id": "71a90c54-e0eb-414f-9ea2-9c39ecb32319",
        "ip_addresses": [
            {
                "address": "139.178.94.207",
                "address_family": 4,
                "public": true
            },
            {
                "address": "2604:1380:45e3:2c00::1",
                "address_family": 6,
                "public": true
            },
            {
                "address": "10.67.168.2",
                "address_family": 4,
                "public": false
            }
        ],
        "ipxe_script_url": "",
        "locked": false,
        "metal_state": "active",
        "metro": "sv",
        "operating_system": "ubuntu_20_04",
        "plan": "c3.small.x86",
        "project_id": "6ac17ea6-a304-4b01-a1f3-f13a7371cfab",
        "spot_instance": false,
        "spot_price_max": 0.0,
        "ssh_keys": [
            {
                "href": "/metal/v1/ssh-keys/1ffe4e4b-eaf9-45d9-a268-0d81af71ae55",
                "id": "1ffe4e4b-eaf9-45d9-a268-0d81af71ae55"
            },
            {
                "href": "/metal/v1/ssh-keys/d122d4e4-4832-41c8-abbb-40182930becf",
                "id": "d122d4e4-4832-41c8-abbb-40182930becf"
            },
            {
                "href": "/metal/v1/ssh-keys/b0f196c0-9cf2-4cb7-96c5-403b81ff6813",
                "id": "b0f196c0-9cf2-4cb7-96c5-403b81ff6813"
            },
            {
                "href": "/metal/v1/ssh-keys/4b011c75-e642-4f6d-85f4-590a5956ad28",
                "id": "4b011c75-e642-4f6d-85f4-590a5956ad28"
            },
            {
                "href": "/metal/v1/ssh-keys/217ff08c-057a-4933-8efe-2e9f723fbb5f",
                "id": "217ff08c-057a-4933-8efe-2e9f723fbb5f"
            },
            {
                "href": "/metal/v1/ssh-keys/10968e80-b234-469b-acb8-c5002b4111a4",
                "id": "10968e80-b234-469b-acb8-c5002b4111a4"
            },
            {
                "href": "/metal/v1/ssh-keys/6ff0810b-135c-48cf-ac68-b365bdfd338c",
                "id": "6ff0810b-135c-48cf-ac68-b365bdfd338c"
            },
            {
                "href": "/metal/v1/ssh-keys/6a71d7e1-db14-4dfd-9014-46032b507538",
                "id": "6a71d7e1-db14-4dfd-9014-46032b507538"
            },
            {
                "href": "/metal/v1/ssh-keys/413e2347-f89c-40af-ba9e-0864f2fde990",
                "id": "413e2347-f89c-40af-ba9e-0864f2fde990"
            },
            {
                "href": "/metal/v1/ssh-keys/9308b337-702a-4774-8351-37dfb8c90a57",
                "id": "9308b337-702a-4774-8351-37dfb8c90a57"
            }
        ],
        "tags": [],
        "userdata": ""
    }
]
'''
]

SPECDOC_META = getSpecDocMeta(
    short_description="Select list of Equinix Metal devices",
    description="Select list of Equinix Metal devices",
    examples=specdoc_examples,
    options=module_spec,
    return_values={
        "resources": SpecReturnValue(
            description="List of devices",
            type=FieldType.list,
            sample=result_sample,
        ),
    },
)


def main():
    module = EquinixModule(
        argument_spec=SPECDOC_META.ansible_spec,
        required_one_of=[('project_id', 'organization_id')],
        mutually_exclusive=[('project_id', 'organization_id')],
        supports_check_mode=True,
    )
    try:
        module.params_syntax_check()
        resource_type = "metal_project_device"
        if module.params.get('organization_id'):
            resource_type = "metal_organization_device"
        return_value = {'resources': module.get_list(resource_type)}

    except Exception as e:
        tr = traceback.format_exc()
        module.fail_json(msg=to_native(e), exception=tr)
    module.exit_json(**return_value)


if __name__ == '__main__':
    main()
