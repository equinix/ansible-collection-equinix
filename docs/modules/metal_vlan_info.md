# metal_vlan_info

Gather information about Equinix Metal VLAN resources


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: list vlans
  equinix.cloud.metal_vlan_info:
  register: listed_vlan

```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `project_id` | <center>`str`</center> | <center>Optional</center> | Filter vlans by Project UUID.   |






## Return Values



### Sample Response for resources
```json
{
  "description": "My VLAN",
  "id": "845b45a3-c565-47e5-b9b6-a86204a73d29",
  "metro": "se",
  "vxlan": 1234
}
```


