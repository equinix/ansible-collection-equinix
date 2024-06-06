# metal_device

Create, update, or delete Equinix Metal devices


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Create new device in a project
  hosts: localhost
  tasks:
    equinix.cloud.metal_device:
      name: "new device"
      project_id: 8e4b0b2a-4a6f-4d3b-9c6c-7a0b3c4d5e6f

```

```yaml
- name: Remove device by id
  hosts: localhost
  tasks:
    equinix.cloud.metal_device:
      id: eef49903-7a09-4ca1-af67-4087c29ab5b6
      state: absent

```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`str`</center> | <center>Optional</center> | UUID of the device.   |
| `always_pxe` | <center>`bool`</center> | <center>Optional</center> | When true, devices with a `custom_ipxe` OS will always boot into iPXE. The default setting of false will ensure that iPXE is only used on first boot.  **(Updatable)** |
| `billing_cycle` | <center>`str`</center> | <center>Optional</center> | Billing cycle of the device.  **(Choices: `hourly`, `daily`, `monthly`, `yearly`; Updatable)** |
| `customdata` | <center>`dict`</center> | <center>Optional</center> | Customdata is an arbitrary JSON value that can be accessed via the metadata service.  **(Updatable)** |
| `facility` | <center>`str`</center> | <center>Optional</center> | Facility of the device.   |
| `features` | <center>`list`</center> | <center>Optional</center> | The features attribute allows you to optionally specify what features your server should have. In the API shorthand syntax, all features listed are `required` ` { "features": ["tpm"] } ` Alternatively, if you do not require a certain feature, but would prefer to be assigned a server with that feature if there are any available, you may specify that feature with a `preferred` value. The request will not fail if we have no servers with that feature in our inventory. The API offers an alternative syntax for mixing preferred and required features ` { "features": { "tpm": "required", "raid": "preferred" } } ` The request will only fail if there are no available servers matching the required `tpm` criteria.    |
| `hardware_reservation_id` | <center>`str`</center> | <center>Optional</center> | The Hardware Reservation UUID to provision. Alternatively, `next-available` can be specified to select from any of the available hardware reservations. An error will be returned if the requested reservation option is not available. See [Reserved Hardware](https://metal.equinix.com/developers/docs/deploy/reserved/) for more details.   |
| `hostname` | <center>`str`</center> | <center>Optional</center> | Hostname to use within the operating system. The same hostname may be used on multiple devices within a project.  **(Updatable)** |
| [`ip_addresses` (sub-options)](#ip_addresses) | <center>`list`</center> | <center>Optional</center> | The `ip_addresses` attribute will allow you to specify the addresses you want created with your device.The default value configures public IPv4, public IPv6, and private IPv4. Private IPv4 address is required. When specifying `ip_addresses`, one of the array items must enable private IPv4. Some operating systems require public IPv4 address. In those cases you will receive an error message if public IPv4 is not enabled. For example, to only configure your server with a private IPv4 address, you can send `{ "ip_addresses": [{ "address_family": 4, "public": false }] }`. It is possible to request a subnet size larger than a `/30` by assigning addresses using the UUID(s) of ip_reservations in your project. For example, `{ "ip_addresses": [..., {"address_family": 4, "public": true, "ip_reservations": ["uuid1", "uuid2"]}] }` To access a server without public IPs, you can use our Out-of-Band console access (SOS) or proxy through another server in the project with public IPs enabled. default is `[{'address_family': 4, 'public': True}, {'address_family': 4, 'public': False}, {'address_family': 6, 'public': True}]`   |
| `ipxe_script_url` | <center>`str`</center> | <center>Optional</center> | When set, the device will chainload an iPXE Script at boot fetched from the supplied URL. See [Custom iPXE](https://metal.equinix.com/developers/docs/operating-systems/custom-ipxe/) for more details.  **(Updatable)** |
| `locked` | <center>`bool`</center> | <center>Optional</center> | Whether the device is locked, preventing accidental deletion.  **(Updatable)** |
| `metro` | <center>`str`</center> | <center>Optional</center> | Metro of the device.   |
| `network_frozen` | <center>`bool`</center> | <center>Optional</center> | Whether the device network should be frozen, preventing any changes to the network configuration.  **(Updatable)** |
| `no_ssh_keys` | <center>`bool`</center> | <center>Optional</center> | Overrides default behaviour of attaching all of the organization members ssh keys and project ssh keys to device if no specific keys specified.   |
| `operating_system` | <center>`str`</center> | <center>Optional</center> | Operating system of the device.   |
| `plan` | <center>`str`</center> | <center>Optional</center> | Plan of the device.   |
| `public_ipv4_subnet_size` | <center>`int`</center> | <center>Optional</center> | Deprecated. Use ip_addresses. Subnet range for addresses allocated to this device. Your project must have addresses available for a non-default request. If not specified, the default is a /31 for IPv4 and a /127 for IPv6.    |
| `project_id` | <center>`str`</center> | <center>Optional</center> | Project id of the device.   |
| `project_ssh_keys` | <center>`list`</center> | <center>Optional</center> | A list of UUIDs identifying the device parent project that should be authorized to access this device (typically via /root/.ssh/authorized_keys). These keys will also appear in the device metadata. If no SSH keys are specified (`user_ssh_keys`, `project_ssh_keys`, and `ssh_keys` are all empty lists or omitted), all parent project keys, parent project members keys and organization members keys will be included. This behaviour can be changed with 'no_ssh_keys' option to omit any SSH key being added.   |
| `provisioning_wait_seconds` | <center>`int`</center> | <center>Optional</center> | How long should the module wait for the device to reach `active` status, in seconds.  **(Default: `1800`)** |
| `spot_instance` | <center>`bool`</center> | <center>Optional</center> | Create a spot instance. Spot instances are created with a maximum bid price. If the bid price is not met, the spot instance will be terminated as indicated by the `termination_time` field.   **(Updatable)** |
| `spot_price_max` | <center>`float`</center> | <center>Optional</center> | Maximum bid price for a spot instance. If the bid price is not met, the spot instance will be terminated as indicated by the `termination_time` field.    |
| `ssh_keys` | <center>`list`</center> | <center>Optional</center> | A list of UUIDs identifying SSH keys that should be authorized to access this device (typically via /root/.ssh/authorized_keys). These keys will also appear in the device metadata. If no SSH keys are specified (`user_ssh_keys`, `project_ssh_keys`, and `ssh_keys` are all empty lists or omitted), all parent project keys, parent project members keys and organization members keys will be included. This behaviour can be changed with 'no_ssh_keys' option to omit any SSH key being added.   |
| `tags` | <center>`list`</center> | <center>Optional</center> | A list of tags to assign to the device.  **(Updatable)** |
| `termination_time` | <center>`str`</center> | <center>Optional</center> | Time at which the spot instance will be terminated.   |
| `userdata` | <center>`str`</center> | <center>Optional</center> | The userdata presented in the metadata service for this device.  Userdata is fetched and interpreted by the operating system installed on the device. Acceptable formats are determined by the operating system, with the exception of a special iPXE enabling syntax which is handled before the operating system starts. See [Server User Data](https://metal.equinix.com/developers/docs/servers/user-data/) and [Provisioning with Custom iPXE] (https://metal.equinix.com/developers/docs/operating-systems/custom-ipxe/#provisioning-with-custom-ipxe) for more details.  **(Updatable)** |
| `user_ssh_keys` | <center>`list`</center> | <center>Optional</center> | A list of UUIDs identifying the device parent user that should be authorized to access this device (typically via /root/.ssh/authorized_keys). These keys will also appear in the device metadata. If no SSH keys are specified (`user_ssh_keys`, `project_ssh_keys`, and `ssh_keys` are all empty lists or omitted), all parent project keys, parent project members keys and organization members keys will be included. This behaviour can be changed with 'no_ssh_keys' option to omit any SSH key being added.   |





### ip_addresses

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `address` | <center>`str`</center> | <center>Optional</center> | IP address.   |
| `address_family` | <center>`int`</center> | <center>Optional</center> | IP address family.   |
| `public` | <center>`bool`</center> | <center>Optional</center> | Whether the IP address is public.   |






## Return Values



### Sample Response for metal_device
```json
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
```


