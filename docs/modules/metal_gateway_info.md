# metal_gateway_info

Gather information about Metal Gateways


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Gather information about all gateways in a project
  hosts: localhost
  tasks:
      - equinix.cloud.metal_gateway_info:
          project_id: 2a5122b9-c323-4d5c-b53c-9ad3f54273e7

```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `project_id` | <center>`str`</center> | <center>Optional</center> | UUID of parent project the gateway is scoped to.   |






## Return Values



### Sample Responses for resources
```json
{
  "id": "771c9418-7c60-4a45-8fa6-3a002132331d",
  "ip_reservation_id": "d45c9629-3aab-4a7b-af5d-4ca50041e311",
  "metal_state": "ready",
  "private_ipv4_subnet_size": 8,
  "project_id": "f7a35065-2e41-4747-b3d1-400af0a3e0e8",
  "virtual_network_id": "898972b3-7eb9-4ca2-b803-7b5d339bbea7"
}
```
```json
{
  "id": "b66eb02d-c4bb-4ae8-a22e-0f7934da971e",
  "ip_reservation_id": "6282982a-e6de-4f4d-b230-2ae27e90778c",
  "metal_state": "ready",
  "private_ipv4_subnet_size": 8,
  "project_id": "f7a35065-2e41-4747-b3d1-400af0a3e0e8",
  "virtual_network_id": "898972b3-7eb9-4ca2-b803-7b5d339bbea7"
}
```


