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
| `metro` | <center>`str`</center> | <center>Optional</center> |  (Optional) Metro where the VLAN is deployed.   |






## Return Values

- `resources` - Found resources

    - Sample Response:
        ```json
        
        [
          {
            "vxlan": 1234,
            "metro": "se",
            "id": "845b45a3-c565-47e5-b9b6-a86204a73d29",
            "description": "My VLAN"
          }
        ]
        ```


