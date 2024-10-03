# metal_reserved_ip_block

When a user provisions first device in a facility, Equinix Metal API automatically allocates IPv6/56 and private IPv4/25 blocks. The new device then gets IPv6 and private IPv4 addresses from those block. It also gets a public IPv4/31 address. Every new device in the project and facility will automatically get IPv6 and private IPv4 addresses from these pre-allocated blocks. The IPv6 and private IPv4 blocks can't be created, only imported. With this resource, it's possible to create either public IPv4 blocks or global IPv4 blocks.


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Create a new reserved IP block in metro "sv"
  hosts: localhost
  tasks:
  - equinix.cloud.metal_reserved_ip_block:
      project_id: 2a5122b9-c323-4d5c-b53c-9ad3f54273e7
      type: public_ipv4
      quantity: 1
      metro: "sv"

```

```yaml
- name: Create a new global reserved IP block (no metro)
  hosts: localhost
  tasks:
  - equinix.cloud.metal_reserved_ip_block:
      project_id: 2a5122b9-c323-4d5c-b53c-9ad3f54273e7
      type: global_ipv4
      quantity: 1

```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`str`</center> | <center>Optional</center> | UUID of the reserved IP block   |
| `type` | <center>`str`</center> | <center>Optional</center> | The type of IP address to list  **(Choices: `public_ipv4`, `public_ipv6`, `private_ipv4`, `global_ipv4`, `vrf`)** |
| `quantity` | <center>`int`</center> | <center>Optional</center> | The number of IP addresses to reserve   |
| `details` | <center>`str`</center> | <center>Optional</center> | Details about the reserved IP block   |
| `metro` | <center>`str`</center> | <center>Optional</center> | The metro where the reserved IP block will be created   |
| `customdata` | <center>`str`</center> | <center>Optional</center> | Custom data to associate with the reserved IP block   |
| `comments` | <center>`str`</center> | <center>Optional</center> | Comments to associate with the reserved IP block   |
| `vrf_id` | <center>`str`</center> | <center>Optional</center> | The ID of the VRF in which this VRF IP Reservation is created. The VRF must have an existing IP Range that contains the requested subnet.   |
| `network` | <center>`str`</center> | <center>Optional</center> | The starting address for this VRF IP Reservation's subnet. Both IPv4 and IPv6 are supported.   |
| `cidr` | <center>`int`</center> | <center>Optional</center> | The size of the VRF IP Reservation's subnet. The following subnet sizes are supported:<br>- IPv4: between 22 - 29 inclusive<br>- IPv6: exactly 64   |
| `project_id` | <center>`str`</center> | <center>Optional</center> | The ID of the project to which the reserved IP block will be assigned   |
| `tags` | <center>`list`</center> | <center>Optional</center> | Tags to associate with the reserved IP block   |






## Return Values



### Sample Response for metal_reserved_ip_block
```json
{
  "address_family": 4,
  "changed": true,
  "customdata": {},
  "details": "",
  "id": "6d94f567-6cf5-4536-8216-7dc96e1585dd",
  "management": false,
  "metro": "sv",
  "netmask": "255.255.255.255",
  "network": "145.40.67.3",
  "project_id": "fd554070-70b6-420d-b3f8-7ed8438862d5",
  "public": true,
  "quantity": 1,
  "tags": [
    "t1",
    "t2"
  ],
  "type": "public_ipv4"
}
```


