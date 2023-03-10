# metal_ip_assignment_info

Gather IP address assignments for a device


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: assignment info 
  equinix.cloud.metal_ip_assignment_info:
    device_id: "{{ device.id }}"
  register: assignment_info

```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `device_id` | <center>`str`</center> | <center>**Required**</center> | UUID of the device to list ip_assignments for.   |






## Return Values

- `resources` - Found resources

    - Sample Response:
        ```json
        
        [
            {
                "address": "147.75.55.115/31",
                "address_family": 4,
                "cidr": 31,
                "device_id": "8ea9837a-6d19-4607-b166-f7f7bb04b022",
                "id": "38deafaa-0a1d-4e32-b8cd-417e2ba958db",
                "management": true,
                "metro": "da",
                "netmask": "255.255.255.254",
                "network": "147.75.55.114",
                "public": true
            },
            {
                "address": "145.40.102.107/32",
                "address_family": 4,
                "cidr": 32,
                "device_id": "8ea9837a-6d19-4607-b166-f7f7bb04b022",
                "id": "c30b9d28-755c-4016-8480-b90497643c29",
                "management": false,
                "metro": "da",
                "netmask": "255.255.255.255",
                "network": "145.40.102.107",
                "public": true
            },
            {
                "address": "2604:1380:4641:5b00::1/127",
                "address_family": 6,
                "cidr": 127,
                "device_id": "8ea9837a-6d19-4607-b166-f7f7bb04b022",
                "id": "ad2f9b8c-f73f-4ae7-9016-f78b316f7ad6",
                "management": true,
                "metro": null,
                "netmask": "ffff:ffff:ffff:ffff:ffff:ffff:ffff:fffe",
                "network": "2604:1380:4641:5b00::",
                "public": true
            },
            {
                "address": "10.70.50.129/31",
                "address_family": 4,
                "cidr": 31,
                "device_id": "8ea9837a-6d19-4607-b166-f7f7bb04b022",
                "id": "4d81a406-3fb2-4ac4-9e03-2a498c5788e1",
                "management": true,
                "metro": null,
                "netmask": "255.255.255.254",
                "network": "10.70.50.128",
                "public": false
            }
        ]
        
        ```


