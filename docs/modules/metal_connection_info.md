# metal_connection_info

Gather information about Interconnections


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Gather information about all connection in a project
  hosts: localhost
  tasks:
      - equinix.cloud.metal_connection_info:
          project_id: "2a5122b9-c323-4d5c-b53c-9ad3f54273e7"

```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `name` | <center>`str`</center> | <center>Optional</center> | Filter connections on substring in name attribute.   |
| `project_id` | <center>`str`</center> | <center>Optional</center> | ID of the project where the connection is scoped to.   |
| `organization_id` | <center>`str`</center> | <center>Optional</center> | ID of the organization where the connection is scoped to.   |






## Return Values



### Sample Response for resources
```json
{
  "id": "31d3ae8b-bd5a-41f3-a420-055211345cc7",
  "metro": "am",
  "name": "my_test_connection",
  "project_id": "845b45a3-c565-47e5-b9b6-a86204a73d29",
  "redundancy": "primary",
  "speed": "50Mbps",
  "type": "dedicated"
}
```


