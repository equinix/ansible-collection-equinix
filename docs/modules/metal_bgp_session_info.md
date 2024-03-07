# metal_bgp_session_info

Gather information BGP sessions in Equinix Metal. You can fetch it by device ID or project ID.


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Gather information about all BGP sessions in a project
  hosts: localhost
  tasks:
      - equinix.cloud.metal_bgp_session_info:
          project_id: 2a5122b9-c323-4d5c-b53c-9ad3f54273e7

```

```yaml

```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `device_id` | <center>`str`</center> | <center>Optional</center> | Find BGP sessions by device ID.   |
| `project_id` | <center>`str`</center> | <center>Optional</center> | Find BGP sessions by project ID.   |






## Return Values



### Sample Response for resources
```json
{
  "address_family": "ipv6",
  "default_route": true,
  "device_id": "b068984f-f7d9-43a2-aa45-de04dcf4fe06",
  "id": "03912bd6-a158-47ad-8bc7-c93df338fe0d"
}
```


