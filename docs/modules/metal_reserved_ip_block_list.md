# metal_reserved_ip_block_list

Gather list of reserved IP blocks matching the specified criteria


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Gather list of public_ipv4 reserved_ip_blocks in a project
  hosts: localhost
  tasks:
  - equinix.cloud.metal_reserved_ip_block_list:
      type: public_ipv4
      project_id: 2a5122b9-c323-4d5c-b53c-9ad3f54273e7

```

```yaml
- name: Gather list of public_ipv6 reserved_ip_blocks in a project in metro ams
  hosts: localhost
  tasks:
  - equinix.cloud.metal_reserved_ip_block_list:
      type: public_ipv6
      project_id: 2a5122b9-c323-4d5c-b53c-9ad3f54273e7
      metro: ams

```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `type` | <center>`str`</center> | <center>**Required**</center> | The type of IP address to list  **(Choices: `public_ipv4`, `public_ipv6`, `private_ipv4`, `global_ipv4`, `vrf`)** |
| `project_id` | <center>`str`</center> | <center>**Required**</center> | UUID of the project to list IP addresses for   |
| `metro` | <center>`str`</center> | <center>Optional</center> | The metro to list IP addresses for   |






## Return Values

- `resources` - Found resources

    - Sample Response:
        ```json
        
        [
            {
                "address_family": 4,
                "customdata": {},
                "details": "some desc fff",
                "id": "16148fad-7839-4c63-b33f-0ecfec4f9e29",
                "management": false,
                "metro": "da",
                "netmask": "255.255.255.255",
                "network": "145.40.102.107",
                "project_id": "52000fb2-ee46-4673-93a8-de2c2bdba33b",
                "public": true,
                "quantity": 1,
                "tags": [],
                "type": "public_ipv4"
            }
        ]
        
        ```


