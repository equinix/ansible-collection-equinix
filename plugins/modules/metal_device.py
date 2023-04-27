#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

DOCUMENTATION = '''
author: Equinix DevRel Team (@equinix) <support@equinix.com>
description: Create, update, or delete Equinix Metal devices
module: metal_device
notes: []
options:
  always_pxe:
    description: !!python/tuple
    - When true, devices with a `custom_ipxe` OS will always boot into iPXE. The default
      setting of false will ensure that iPXE is only used on first boot.
    required: false
    type: bool
  billing_cycle:
    choices:
    - hourly
    - daily
    - monthly
    - yearly
    description:
    - Billing cycle of the device.
    required: false
    type: str
  customdata:
    description:
    - Customdata is an arbitrary JSON value that can be accessed via the metadata
      service.
    required: false
    type: dict
  facility:
    description:
    - Facility of the device.
    required: false
    type: str
  features:
    description:
    - 'The features attribute allows you to optionally specify what features your
      server should have. In the API shorthand syntax, all features listed are `required`
      ` { "features": ["tpm"] } ` Alternatively, if you do not require a certain feature,
      but would prefer to be assigned a server with that feature if there are any
      available, you may specify that feature with a `preferred` value. The request
      will not fail if we have no servers with that feature in our inventory. The
      API offers an alternative syntax for mixing preferred and required features
      ` { "features": { "tpm": "required", "raid": "preferred" } } ` The request will
      only fail if there are no available servers matching the required `tpm` criteria. '
    elements: str
    required: false
    type: list
  hardware_reservation_id:
    description:
    - The Hardware Reservation UUID to provision. Alternatively, `next-available`
      can be specified to select from any of the available hardware reservations.
      An error will be returned if the requested reservation option is not available.
      See [Reserved Hardware](https://metal.equinix.com/developers/docs/deploy/reserved/)
      for more details.
    required: false
    type: str
  hostname:
    description:
    - Hostname to use within the operating system. The same hostname may be used on
      multiple devices within a project.
    required: false
    type: str
  id:
    description:
    - UUID of the device.
    required: false
    type: str
  ip_addresses:
    description:
    - 'The `ip_addresses` attribute will allow you to specify the addresses you want
      created with your device.The default value configures public IPv4, public IPv6,
      and private IPv4. Private IPv4 address is required. When specifying `ip_addresses`,
      one of the array items must enable private IPv4. Some operating systems require
      public IPv4 address. In those cases you will receive an error message if public
      IPv4 is not enabled. For example, to only configure your server with a private
      IPv4 address, you can send `{ "ip_addresses": [{ "address_family": 4, "public":
      false }] }`. It is possible to request a subnet size larger than a `/30` by
      assigning addresses using the UUID(s) of ip_reservations in your project. For
      example, `{ "ip_addresses": [..., {"address_family": 4, "public": true, "ip_reservations":
      ["uuid1", "uuid2"]}] }` To access a server without public IPs, you can use our
      Out-of-Band console access (SOS) or proxy through another server in the project
      with public IPs enabled. default is `[{''address_family'': 4, ''public'': True},
      {''address_family'': 4, ''public'': False}, {''address_family'': 6, ''public'':
      True}]`'
    elements: dict
    required: false
    suboptions:
      address:
        description:
        - IP address.
        required: false
        type: str
      address_family:
        description:
        - IP address family.
        required: false
        type: int
      public:
        description:
        - Whether the IP address is public.
        required: false
        type: bool
    type: list
  ipxe_script_url:
    description:
    - When set, the device will chainload an iPXE Script at boot fetched from the
      supplied URL. See [Custom iPXE](https://metal.equinix.com/developers/docs/operating-systems/custom-ipxe/)
      for more details.
    required: false
    type: str
  locked:
    description:
    - Whether the device is locked, preventing accidental deletion.
    required: false
    type: bool
  metro:
    description:
    - Metro of the device.
    required: false
    type: str
  network_frozen:
    description:
    - Whether the device network should be frozen, preventing any changes to the network
      configuration.
    required: false
    type: bool
  no_ssh_keys:
    description:
    - Overrides default behaviour of attaching all of the organization members ssh
      keys and project ssh keys to device if no specific keys specified.
    required: false
    type: bool
  operating_system:
    description:
    - Operating system of the device.
    required: false
    type: str
  plan:
    description:
    - Plan of the device.
    required: false
    type: str
  project_id:
    description:
    - Project id of the device.
    required: false
    type: str
  project_ssh_keys:
    description:
    - A list of UUIDs identifying the device parent project that should be authorized
      to access this device (typically via /root/.ssh/authorized_keys). These keys
      will also appear in the device metadata. If no SSH keys are specified (`user_ssh_keys`,
      `project_ssh_keys`, and `ssh_keys` are all empty lists or omitted), all parent
      project keys, parent project members keys and organization members keys will
      be included. This behaviour can be changed with 'no_ssh_keys' option to omit
      any SSH key being added.
    elements: str
    required: false
    type: list
  provisioning_wait_seconds:
    default: 300
    description:
    - How long should the module wait for the device to be provisionedi, in seconds.
    required: false
    type: int
  public_ipv4_subnet_size:
    description:
    - 'Deprecated. Use ip_addresses. Subnet range for addresses allocated to this
      device. Your project must have addresses available for a non-default request.
      If not specified, the default is a /31 for IPv4 and a /127 for IPv6. '
    required: false
    type: int
  spot_instance:
    description:
    - 'Create a spot instance. Spot instances are created with a maximum bid price.
      If the bid price is not met, the spot instance will be terminated as indicated
      by the `termination_time` field. '
    required: false
    type: bool
  spot_price_max:
    description:
    - 'Maximum bid price for a spot instance. If the bid price is not met, the spot
      instance will be terminated as indicated by the `termination_time` field. '
    required: false
    type: float
  ssh_keys:
    description:
    - A list of UUIDs identifying SSH keys that should be authorized to access this
      device (typically via /root/.ssh/authorized_keys). These keys will also appear
      in the device metadata. If no SSH keys are specified (`user_ssh_keys`, `project_ssh_keys`,
      and `ssh_keys` are all empty lists or omitted), all parent project keys, parent
      project members keys and organization members keys will be included. This behaviour
      can be changed with 'no_ssh_keys' option to omit any SSH key being added.
    elements: str
    required: false
    type: list
  tags:
    description:
    - A list of tags to assign to the device.
    elements: str
    required: false
    type: list
  termination_time:
    description:
    - Time at which the spot instance will be terminated.
    required: false
    type: str
  user_ssh_keys:
    description:
    - A list of UUIDs identifying the device parent user that should be authorized
      to access this device (typically via /root/.ssh/authorized_keys). These keys
      will also appear in the device metadata. If no SSH keys are specified (`user_ssh_keys`,
      `project_ssh_keys`, and `ssh_keys` are all empty lists or omitted), all parent
      project keys, parent project members keys and organization members keys will
      be included. This behaviour can be changed with 'no_ssh_keys' option to omit
      any SSH key being added.
    required: false
    type: list
  userdata:
    description:
    - The userdata presented in the metadata service for this device.  Userdata is
      fetched and interpreted by the operating system installed on the device. Acceptable
      formats are determined by the operating system, with the exception of a special
      iPXE enabling syntax which is handled before the operating system starts. See
      [Server User Data](https://metal.equinix.com/developers/docs/servers/user-data/)
      and [Provisioning with Custom iPXE] (https://metal.equinix.com/developers/docs/operating-systems/custom-ipxe/#provisioning-with-custom-ipxe)
      for more details.
    required: false
    type: str
requirements:
- python >= 3
- equinix_metal >= 0.0.1
short_description: Create, update, or delete Equinix Metal devices
'''
EXAMPLES = '''
- name: Create new device in a project
  hosts: localhost
  tasks:
    equinix.cloud.metal_device:
      name: new device
      project_id: 8e4b0b2a-4a6f-4d3b-9c6c-7a0b3c4d5e6f
- name: Remove device by id
  hosts: localhost
  tasks:
    equinix.cloud.metal_device:
      id: eef49903-7a09-4ca1-af67-4087c29ab5b6
      state: absent
'''
RETURN = '''
metal_device:
  description: The module object
  returned: always
  sample:
  - "\n{\n    \"always_pxe\": false,\n    \"billing_cycle\": \"hourly\",\n    \"changed\"\
    : true,\n    \"customdata\": {},\n    \"facility\": \"sv15\",\n    \"hardware_reservation_id\"\
    : \"\",\n    \"hostname\": \"ansible-integration-test-device-yi4fbuo4-dev1\",\n\
    \    \"id\": \"71a90c54-e0eb-414f-9ea2-9c39ecb32319\",\n    \"ip_addresses\":\
    \ [\n        {\n            \"address\": \"139.178.94.207\",\n            \"address_family\"\
    : 4,\n            \"public\": true\n        },\n        {\n            \"address\"\
    : \"2604:1380:45e3:2c00::1\",\n            \"address_family\": 6,\n          \
    \  \"public\": true\n        },\n        {\n            \"address\": \"10.67.168.2\"\
    ,\n            \"address_family\": 4,\n            \"public\": false\n       \
    \ }\n    ],\n    \"ipxe_script_url\": \"\",\n    \"locked\": false,\n    \"metal_state\"\
    : \"active\",\n    \"metro\": \"sv\",\n    \"operating_system\": \"ubuntu_20_04\"\
    ,\n    \"plan\": \"c3.small.x86\",\n    \"project_id\": \"6ac17ea6-a304-4b01-a1f3-f13a7371cfab\"\
    ,\n    \"spot_instance\": false,\n    \"spot_price_max\": 0.0,\n    \"ssh_keys\"\
    : [\n        {\n            \"href\": \"/metal/v1/ssh-keys/1ffe4e4b-eaf9-45d9-a268-0d81af71ae55\"\
    ,\n            \"id\": \"1ffe4e4b-eaf9-45d9-a268-0d81af71ae55\"\n        },\n\
    \        {\n            \"href\": \"/metal/v1/ssh-keys/d122d4e4-4832-41c8-abbb-40182930becf\"\
    ,\n            \"id\": \"d122d4e4-4832-41c8-abbb-40182930becf\"\n        },\n\
    \        {\n            \"href\": \"/metal/v1/ssh-keys/b0f196c0-9cf2-4cb7-96c5-403b81ff6813\"\
    ,\n            \"id\": \"b0f196c0-9cf2-4cb7-96c5-403b81ff6813\"\n        },\n\
    \        {\n            \"href\": \"/metal/v1/ssh-keys/4b011c75-e642-4f6d-85f4-590a5956ad28\"\
    ,\n            \"id\": \"4b011c75-e642-4f6d-85f4-590a5956ad28\"\n        },\n\
    \        {\n            \"href\": \"/metal/v1/ssh-keys/217ff08c-057a-4933-8efe-2e9f723fbb5f\"\
    ,\n            \"id\": \"217ff08c-057a-4933-8efe-2e9f723fbb5f\"\n        },\n\
    \        {\n            \"href\": \"/metal/v1/ssh-keys/10968e80-b234-469b-acb8-c5002b4111a4\"\
    ,\n            \"id\": \"10968e80-b234-469b-acb8-c5002b4111a4\"\n        },\n\
    \        {\n            \"href\": \"/metal/v1/ssh-keys/6ff0810b-135c-48cf-ac68-b365bdfd338c\"\
    ,\n            \"id\": \"6ff0810b-135c-48cf-ac68-b365bdfd338c\"\n        },\n\
    \        {\n            \"href\": \"/metal/v1/ssh-keys/6a71d7e1-db14-4dfd-9014-46032b507538\"\
    ,\n            \"id\": \"6a71d7e1-db14-4dfd-9014-46032b507538\"\n        },\n\
    \        {\n            \"href\": \"/metal/v1/ssh-keys/413e2347-f89c-40af-ba9e-0864f2fde990\"\
    ,\n            \"id\": \"413e2347-f89c-40af-ba9e-0864f2fde990\"\n        },\n\
    \        {\n            \"href\": \"/metal/v1/ssh-keys/9308b337-702a-4774-8351-37dfb8c90a57\"\
    ,\n            \"id\": \"9308b337-702a-4774-8351-37dfb8c90a57\"\n        }\n \
    \   ],\n    \"tags\": [],\n    \"userdata\": \"\"\n}\n"
  type: dict
'''


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
        description="UUID of the device.",
    ),
    always_pxe=SpecField(
        type=FieldType.bool,
        description=("When true, devices with a `custom_ipxe` OS will always "
                     "boot into iPXE. The default setting of false will "
                     "ensure that iPXE is only used on first boot.",),
        editable=True,
    ),
    billing_cycle=SpecField(
        type=FieldType.string,
        description="Billing cycle of the device.",
        choices=["hourly", "daily", "monthly", "yearly"],
        editable=True,
    ),
    customdata=SpecField(
        type=FieldType.dict,
        description=("Customdata is an arbitrary JSON value that can be accessed "
                     "via the metadata service."),
        editable=True,
    ),
    facility=SpecField(
        type=FieldType.string,
        description="Facility of the device.",
    ),
    features=SpecField(
        type=FieldType.list,
        description=(
            'The features attribute allows you to optionally specify what features your server should have. '
            'In the API shorthand syntax, all features listed are `required` '
            '` { "features": ["tpm"] } ` '
            'Alternatively, if you do not require a certain feature, but would prefer to be assigned a server '
            'with that feature if there are any available, you may specify that feature with a `preferred` value. '
            'The request will not fail if we have no servers with that feature in our inventory. '
            'The API offers an alternative syntax for mixing preferred and required features '
            '` { "features": { "tpm": "required", "raid": "preferred" } } ` '
            'The request will only fail if there are no available servers matching the required `tpm` criteria. '
        ),
        element_type=FieldType.string,
    ),
    hardware_reservation_id=SpecField(
        type=FieldType.string,
        description=(
            'The Hardware Reservation UUID to provision. Alternatively, `next-available` can be specified to select from any of the available hardware '
            'reservations. An error will be returned if the requested reservation option is not available. '
            'See [Reserved Hardware](https://metal.equinix.com/developers/docs/deploy/reserved/) for more details.'
        )
    ),
    hostname=SpecField(
        type=FieldType.string,
        description=(
            'Hostname to use within the operating system. The same hostname may '
            'be used on multiple devices within a project.'
        ),
        editable=True,
    ),
    ip_addresses=SpecField(
        type=FieldType.list,
        description=(
            'The `ip_addresses` attribute will allow you to specify the addresses you want created with your device.'
            'The default value configures public IPv4, public IPv6, and private IPv4. '
            'Private IPv4 address is required. When specifying `ip_addresses`, one of the array items must enable private IPv4. '
            'Some operating systems require public IPv4 address. In those cases you will receive an error message if public IPv4 is not enabled. '
            'For example, to only configure your server with a private IPv4 address, you can send '
            '`{ "ip_addresses": [{ "address_family": 4, "public": false }] }`. '
            'It is possible to request a subnet size larger than a `/30` by assigning addresses using the UUID(s) of ip_reservations in your project. '
            'For example, `{ "ip_addresses": [..., {"address_family": 4, "public": true, "ip_reservations": ["uuid1", "uuid2"]}] }` '
            'To access a server without public IPs, you can use our Out-of-Band console access (SOS) or proxy through another server '
            'in the project with public IPs enabled. '
            "default is `[{'address_family': 4, 'public': True}, {'address_family': 4, 'public': False}, {'address_family': 6, 'public': True}]`"
        ),
        element_type=FieldType.dict,
        suboptions=dict(
            address=SpecField(
                type=FieldType.string,
                description="IP address.",
            ),
            address_family=SpecField(
                type=FieldType.integer,
                description="IP address family.",
            ),
            public=SpecField(
                type=FieldType.bool,
                description="Whether the IP address is public.",
            ),
        ),
    ),
    ipxe_script_url=SpecField(
        type=FieldType.string,
        description=(
            'When set, the device will chainload an iPXE Script at boot fetched from the supplied URL. '
            'See [Custom iPXE](https://metal.equinix.com/developers/docs/operating-systems/custom-ipxe/) for more details.'
        ),
        editable=True,
    ),
    locked=SpecField(
        type=FieldType.bool,
        description="Whether the device is locked, preventing accidental deletion.",
        editable=True,
    ),
    metro=SpecField(
        type=FieldType.string,
        description="Metro of the device.",
    ),
    network_frozen=SpecField(
        type=FieldType.bool,
        description="Whether the device network should be frozen, preventing any changes to the network configuration.",
        editable=True,
    ),
    no_ssh_keys=SpecField(
        type=FieldType.bool,
        description="Overrides default behaviour of attaching all of the organization members ssh keys and project ssh keys to device if no specific keys specified.",
    ),
    operating_system=SpecField(
        type=FieldType.string,
        description="Operating system of the device.",
    ),
    plan=SpecField(
        type=FieldType.string,
        description="Plan of the device.",
    ),
    public_ipv4_subnet_size=SpecField(
        type=FieldType.integer,
        description=(
            'Deprecated. Use ip_addresses. Subnet range for addresses allocated to this device. Your project must have addresses '            'available for a non-default request. '
            'If not specified, the default is a /31 for IPv4 and a /127 for IPv6. '
        ),
    ),
    project_id=SpecField(
        type=FieldType.string,
        description="Project id of the device.",
    ),
    project_ssh_keys=SpecField(
        type=FieldType.list,
        description=(
            'A list of UUIDs identifying the device parent project that should be authorized to access this device '
            '(typically via /root/.ssh/authorized_keys). These keys will also appear in the device metadata. '
            'If no SSH keys are specified (`user_ssh_keys`, `project_ssh_keys`, and `ssh_keys` are all empty '
            'lists or omitted), all parent project keys, parent project members keys and organization members keys '
            "will be included. This behaviour can be changed with 'no_ssh_keys' option to omit any SSH key being added."
        ),
        element_type=FieldType.string,
    ),
    provisioning_wait_seconds=SpecField(
        type=FieldType.integer,
        description="How long should the module wait for the device to be provisionedi, in seconds.",
        default=300,
    ),
    spot_instance=SpecField(
        type=FieldType.bool,
        description=(
            'Create a spot instance. Spot instances are created with a maximum bid price. If the bid price is not met, the spot instance '
            'will be terminated as indicated by the `termination_time` field. '
        ),
        editable=True,
    ),
    spot_price_max=SpecField(
        type=FieldType.float,
        description=(
            'Maximum bid price for a spot instance. If the bid price is not met, the spot instance '
            'will be terminated as indicated by the `termination_time` field. '
        ),
    ),
    ssh_keys=SpecField(
        type=FieldType.list,
        description=(
            'A list of UUIDs identifying SSH keys that should be authorized to access this device '
            '(typically via /root/.ssh/authorized_keys). These keys will also appear in the device metadata. '
            'If no SSH keys are specified (`user_ssh_keys`, `project_ssh_keys`, and `ssh_keys` are all empty '
            'lists or omitted), all parent project keys, parent project members keys and organization members keys '
            "will be included. This behaviour can be changed with 'no_ssh_keys' option to omit any SSH key being added."
        ),
        element_type=FieldType.string,
    ),
    tags=SpecField(
        type=FieldType.list,
        description="A list of tags to assign to the device.",
        element_type=FieldType.string,
        editable=True,
    ),
    termination_time=SpecField(
        type=FieldType.string,
        description="Time at which the spot instance will be terminated.",
    ),
    userdata=SpecField(
        type=FieldType.string,
        description=(
            'The userdata presented in the metadata service for this device.  Userdata is fetched and interpreted by the operating system installed on '
            'the device. Acceptable formats are determined by the operating system, with the exception of a special iPXE enabling '
            'syntax which is handled before the operating system starts. '
            'See [Server User Data](https://metal.equinix.com/developers/docs/servers/user-data/) and [Provisioning with Custom iPXE] '
            '(https://metal.equinix.com/developers/docs/operating-systems/custom-ipxe/#provisioning-with-custom-ipxe) for more details.'
        ),
        editable=True,
    ),
    user_ssh_keys=SpecField(
        type=FieldType.list,
        description=(
            'A list of UUIDs identifying the device parent user that should be authorized to access this device '
            '(typically via /root/.ssh/authorized_keys). These keys will also appear in the device metadata. '
            'If no SSH keys are specified (`user_ssh_keys`, `project_ssh_keys`, and `ssh_keys` are all empty '
            'lists or omitted), all parent project keys, parent project members keys and organization members keys '
            "will be included. This behaviour can be changed with 'no_ssh_keys' option to omit any SSH key being added."
        ),
    ),
)

specdoc_examples = [
    '''
- name: Create new device in a project
  hosts: localhost
  tasks:
    equinix.cloud.metal_device:
      name: "new device"
      project_id: 8e4b0b2a-4a6f-4d3b-9c6c-7a0b3c4d5e6f
''', '''
- name: Remove device by id
  hosts: localhost
  tasks:
    equinix.cloud.metal_device:
      id: eef49903-7a09-4ca1-af67-4087c29ab5b6
      state: absent
''',
]

result_sample = ['''
{
    "always_pxe": false,
    "billing_cycle": "hourly",
    "changed": true,
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
''']

SPECDOC_META = getSpecDocMeta(
    short_description='Create, update, or delete Equinix Metal devices',
    description='Create, update, or delete Equinix Metal devices',
    examples=specdoc_examples,
    options=module_spec,
    return_values={
        "metal_device": SpecReturnValue(
            description='The module object',
            type=FieldType.dict,
            sample=result_sample,
        ),
    },
)

from ansible.module_utils._text import to_native
import traceback

from ansible_collections.equinix.cloud.plugins.module_utils.equinix import (
    EquinixModule,
    get_diff,
)

MUTABLE_ATTRIBUTES = [a for a, v in module_spec.items() if v.editable]


def main():
    module = EquinixModule(
        argument_spec=SPECDOC_META.ansible_spec,
        required_one_of=[("hostname", "id")],
        required_by=dict(hostname=("project_id")),
    )

    try:
        module.params_syntax_check()

        state = module.params.get("state")
        changed = False

        if module.params.get("id"):
            tolerate_not_found = state == "absent"
            fetched = module.get_by_id("metal_device", tolerate_not_found)
        else:
            fetched = module.get_one_from_list("metal_project_device", ["hostname"])
        if fetched:
            module.params["id"] = fetched["id"]
            if state == "present":
                diff = get_diff(module.params, fetched, MUTABLE_ATTRIBUTES)
                if diff:
                    fetched = module.update_by_id(diff, "metal_device")
                    changed = True

            else:
                module.delete_by_id("metal_device")
                changed = True
        else:
            if state == "present":
                plan = module.params.get("plan")
                operating_system = module.params.get("operating_system")
                if (plan is None) or (operating_system is None):
                    raise Exception("plan and operating_system are required when creating a device")
                fetched = module.create("metal_device")
                if "id" not in fetched:
                    raise Exception("UUID not found in device creation response")
                changed = True
                module.params["id"] = fetched["id"]
                seconds = module.params.get("provisioning_wait_seconds")
                fetched = module.wait_for_resource_condition(
                    "metal_device",
                    "metal_state",
                    "active",
                    timeout=seconds)

                # network_frozen is not a create attribute, so we need to update explicitly
                if module.params.get("network_frozen"):
                    fetched = module.update_by_id({"network_frozen": True}, "metal_device")
            else:
                fetched = {}
    except Exception as e:
        tb = traceback.format_exc()
        module.fail_json(msg="Error in metal_device: {0}".format(to_native(e)), exception=tb)

    fetched.update({"changed": changed})
    module.exit_json(**fetched)


if __name__ == "__main__":
    main()
