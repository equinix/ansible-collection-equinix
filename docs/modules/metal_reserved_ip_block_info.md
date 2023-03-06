# metal_reserved_ip_block_info

Gather information about Equinix Metal projects


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Gather information about all reserved_ip_blocks
  hosts: localhost
  tasks:
      - equinix.cloud.metal_reserved_ip_block_info

```

```yaml
- name: Gather information about all reserved_ip_blocks in organization
  hosts: localhost
  tasks:
      - equinix.cloud.metal_reserved_ip_block_info:
            organization_id: 2a5122b9-c323-4d5c-b53c-9ad3f54273e7

```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `type` | <center>`str`</center> | <center>**Required**</center> | The type of IP address to list  **(Choices: `public_ipv4`, `public_ipv6`, `private_ipv4`, `global_ipv4`, `vrf`)** |
| `project_id` | <center>`str`</center> | <center>**Required**</center> | UUID of the project to list IP addresses for   |
| `metro` | <center>`str`</center> | <center>Optional</center> | The metro to list IP addresses for   |






## Return Values

- `resources` - Found resources


