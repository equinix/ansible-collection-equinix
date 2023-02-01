# Copyright: (c) 2019, Nurfet Becirevic <nurfet.becirevic@gmail.com>
# Copyright: (c) 2021, Jason DeTiberus (@detiber) <jdetiberus@equinix.com>
# Copyright: (c) 2023, Tomas Karasek <tom.to.the.k@gmail.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: metal_device
extends_documentation_fragment:
    - equinix.cloud.metal_common
    - equinix.cloud.state
short_description: Create/delete a device in Equinix Metal
description:
    - Create/delete a device in Equinix Metal.
options:
    id:
        description:
            - UUID of the device.
        type: str

    project_id:
        description:
            - UUID of the project to create the device in.
        type: str

    facility:
        description:
            - The slug of the facility to use.
        type: str

    metro:
        description:
            - The slug of the metro to use.
        type: str

    always_pxe:
        type: bool
        description:
            - When true, devices with a `custom_ipxe` OS will always boot
              to iPXE. The default setting of false ensures that iPXE will
              be used on only the first boot.

    billing_cycle:
        type: string
        description:
            - The billing cycle of the device.
        choices:
        - hourly
        - daily
        - monthly
        - yearly

    customdata:
        type: dict
        description:
            - Customdata is an arbitrary JSON value that can be accessed via the metadata service.

    features:
        type: list
        description:
            - The features attribute allows you to optionally specify what features your server should have.
            - In the API shorthand syntax, all features listed are `required`:
            - '` { "features": ["tpm"] } `'
            - Alternatively, if you do not require a certain feature, but would prefer to be assigned a server with that feature if there are any available, you may specify that feature with a `preferred` value. The request will not fail if we have no servers with that feature in our inventory. The API offers an alternative syntax for mixing preferred and required features:
            - '` { "features": { "tpm": "required", "raid": "preferred" } } `'
            - The request will only fail if there are no available servers matching the required `tpm` criteria.

    hardware_reservation_id:
        type: string
        description:
            - The Hardware Reservation UUID to provision. Alternatively, `next-available` can be specified to select from any of the available hardware reservations. An error will be returned if the requested reservation option is not available.
            - See [Reserved Hardware](https://metal.equinix.com/developers/docs/deploy/reserved/) for more details.

    hostname:
        type: string
        description:
            - The hostname to use within the operating system. The same hostname may be used on multiple devices within a project.

    ip_addresses:
        type: list
        description:
            - 'The `ip_addresses` attribute will allow you to specify the addresses you want created with your device.'
            - The default value configures public IPv4, public IPv6, and private IPv4.
            - 'Private IPv4 address is required. When specifying `ip_addresses`, one of the array items must enable private IPv4.'
            - Some operating systems require public IPv4 address. In those cases you will receive an error message if public IPv4 is not enabled.
            - 'For example, to only configure your server with a private IPv4 address, you can send `{ "ip_addresses": [{ "address_family": 4, "public": false }] }`.'
            - 'It is possible to request a subnet size larger than a `/30` by assigning addresses using the UUID(s) of ip_reservations in your project.'
            - 'For example, `{ "ip_addresses": [..., {"address_family": 4, "public": true, "ip_reservations": ["uuid1", "uuid2"]}] }`'
            - To access a server without public IPs, you can use our Out-of-Band console access (SOS) or proxy through another server in the project with public IPs enabled.
        default: [{'address_family': 4, 'public': True}, {'address_family': 4, 'public': False}, {'address_family': 6, 'public': True}]

    ipxe_script_url:
        type: string
        description:
            - When set, the device will chainload an iPXE Script at boot fetched from the supplied URL.
            - See [Custom iPXE](https://metal.equinix.com/developers/docs/operating-systems/custom-ipxe/) for more details.

    locked:
        type: bool
        description:
            - Whether the device should be locked, preventing accidental deletion.

    metal_state:
        type: string
        description:
            - The state of the device from the perspective of the Equinix Metal API.

    no_ssh_keys:
        type: bool
        description:
            - Overrides default behaviour of attaching all of the organization members ssh keys and project ssh keys to device if no specific keys specified

    operating_system:
        type: string
        description:
            - The slug of the operating system to provision. Check the Equinix Metal operating system documentation for rules that may be imposed per operating system, including restrictions on IP address options and device plans.

    plan:
        type: string
        description:
            - The slug of the device plan to provision.

    private_ipv4_subnet_size:
        type: integer
        description:
            - Deprecated. Use ip_addresses. Subnet range for addresses allocated to this device.
        default: 28

    project_ssh_keys:
        type: list
        description:
            - A list of UUIDs identifying the device parent project that should be authorized to access this device (typically via /root/.ssh/authorized_keys). These keys will also appear in the device metadata.
            - If no SSH keys are specified (`user_ssh_keys`, `project_ssh_keys`, and `ssh_keys` are all empty lists or omitted), all parent project keys, parent project members keys and organization members keys will be included. This behaviour can be changed with 'no_ssh_keys' option to omit any SSH key being added.

    provisioning_wait_seconds:
        type: integer
        description:
            - The number of seconds to wait for the device to be provisioned. If the device is not provisioned within this time, the module will fail.
        default: 300

    public_ipv4_subnet_size:
        type: integer
        description:
            - Deprecated. Use ip_addresses. Subnet range for addresses allocated to this device. Your project must have addresses available for a non-default request.
        default: 31

    spot_instance:
        type: bool
        description:
            - Create a spot instance. Spot instances are created with a maximum bid price. If the bid price is not met, the spot instance will be terminated as indicated by the `termination_time` field.

    spot_price_max:
        type: number
        description:
            - The maximum amount to bid for a spot instance.

    ssh_keys:
        type: list
        description:
            - A list of new or existing project ssh_keys that should be authorized to access this device (typically via /root/.ssh/authorized_keys).
              These keys will also appear in the device metadata.
            - These keys are added in addition to any keys defined by `project_ssh_keys` and `user_ssh_keys`.

    termination_time:
        type: string
        description:
            - The time at which the device will be terminated.

    user_ssh_keys:
        type: list
        description:
            - A list of UUIDs identifying the users that should be authorized to access this device (typically via /root/.ssh/authorized_keys).  These keys will also appear in the device metadata.
            - The users must be members of the project or organization.
            - If no SSH keys are specified (`user_ssh_keys`, `project_ssh_keys`, and `ssh_keys` are all empty lists or omitted), all parent project keys,
              parent project members keys and organization members keys will be included. This behaviour can be changed with 'no_ssh_keys' option to omit
              any SSH key being added.

    userdata:
        type: string
        description:
            - The userdata presented in the metadata service for this device.  Userdata is fetched and interpreted by the operating system installed on
              the device. Acceptable formats are determined by the operating system, with the exception of a special iPXE enabling
              syntax which is handled before the operating system starts.
            - See [Server User Data](https://metal.equinix.com/developers/docs/servers/user-data/) and [Provisioning with Custom iPXE]
              (https://metal.equinix.com/developers/docs/operating-systems/custom-ipxe/#provisioning-with-custom-ipxe) for more details.

"""

EXAMPLES = r"""
- name: Create new device in a project
  hosts: localhost
  tasks:
    equinix.cloud.metal_device:
      name: "new device"
      project_id: 8e4b0b2a-4a6f-4d3b-9c6c-7a0b3c4d5e6f

- name: Remove device by id
  hosts: localhost
  tasks:
    equinix.cloud.metal_device:
      id: eef49903-7a09-4ca1-af67-4087c29ab5b6
      state: absent
"""

RETURN = r"""
id:
    description: UUID of the device.
    returned: success
    type: str
    sample: "eef49903-7a09-4ca1-af67-4087c29ab5b6"
href:
    description: URL of the device.
    returned: success
    type: str
    sample: "https://api.equinix.com/metal/v1/devices/eef49903-7a09-4ca1-af67-4087c29ab5b6"
"""

from ansible.module_utils._text import to_native
import traceback

from ansible_collections.equinix.cloud.plugins.module_utils.equinix import (
    EquinixModule,
    get_diff,
)

MUTABLE_ATTRIBUTES = [
    "always_pxe",
    "billing_cycle",
    "customdata",
    "hostname",
    "ipxe_script_url",
    "locked",
    "network_frozen",
    "spot_instance",
    "userdata",
]


def main():
    argument_spec = dict(
        state=dict(type="str", default="present", choices=["present", "absent"]),
        id=dict(type="str"),
        project_id=dict(type="str"),
        metro=dict(type="str"),
        facility=dict(type="str"),
        always_pxe=dict(type="bool"),
        billing_cycle=dict(type="str"),
        customdata=dict(type="str"),
        hostname=dict(type="str"),
        ip_addresses=dict(type="list", elements="dict"),
        ipxe_script_url=dict(type="str"),
        locked=dict(type="bool"),
        network_frozen=dict(type="bool"),
        operating_system=dict(type="str"),
        plan=dict(type="str"),
        project_ssh_keys=dict(type="list", elements="str"),
        provisioning_wait_seconds=dict(type="int", default=300),
        public_ipv4_subnet_size=dict(type="int"),
        spot_instance=dict(type="bool"),
        spot_price_max=dict(type="float"),
        ssh_keys=dict(type="list", elements="str"),
        termination_time=dict(type="str"),
        user_ssh_keys=dict(type="list", elements="str"),
        userdata=dict(type="str"),
    )
    module = EquinixModule(
        argument_spec=argument_spec,
        required_one_of=[("hostname", "id")],
        required_by=dict(hostname=("project_id", "operating_system", "plan")),
    )

    state = module.params.get("state")
    changed = False

    try:
        if module.params.get("id"):
            tolerate_not_found = state == "absent"
            fetched = module.get_by_id("metal_device", tolerate_not_found)
        else:
            hostname = module.params.get("hostname")
            fetched = module.get_one_from_list("metal_project_device", "hostname", {"hostname": hostname})
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
                # device doesn't exist, create it
                metro = module.params.get("metro")
                facility = module.params.get("facility")
                if metro and facility:
                    raise Exception("metro and facility are mutually exclusive when creating a device")
                if (metro is None) and (facility is None):
                    raise Exception("one of metro or facility is required when creating a device")
                if metro:
                    fetched = module.create("metal_device_metro")
                elif facility:
                    fetched = module.create("metal_device_facility")
                else:
                    raise Exception("metro or facility required when creating a device, this is a module bug")
                if "id" not in fetched:
                    raise Exception("UUID not found in device creation response")
                changed = True
                module.params["id"] = fetched["id"]
                fetched = module.wait_for_resource_condition("metal_device", "metal_state", "active", timeout=60)

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
