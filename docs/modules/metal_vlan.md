# metal_vlan

Manage the VLAN in Equinix Metal. You can use *id* or *vxlan* to lookup the resource. If you want to create new resource, you must provide *metro*.


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Create new VLAN
  hosts: localhost
  tasks:
  - equinix.cloud.metal_vlan:
      description: "This is my new VLAN."
      metro: "se"
      vxlan: 1234
      project_id: "778h50f7-75b6-4271-bc64-632b80f87de2"

```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`str`</center> | <center>Optional</center> | UUID of vlan   |
| `project_id` | <center>`str`</center> | <center>Optional</center> | ID of parent project   |
| `description` | <center>`str`</center> | <center>Optional</center> | Description of the VLAN   |
| `metro` | <center>`str`</center> | <center>Optional</center> | Metro in which to create the VLAN   |
| `vxlan` | <center>`int`</center> | <center>Optional</center> | VLAN ID, must be unique in metro   |






## Return Values



### Sample Response for metal_vlan
```json
{
  "changed": false,
  "description": "This is my new VLAN.",
  "id": "7624f0f7-75b6-4271-bc64-632b80f87de2",
  "metro": "se",
  "project_id": "778h50f7-75b6-4271-bc64-632b80f87de2",
  "vxlan": 1234
}
```


