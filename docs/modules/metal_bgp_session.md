# metal_bgp_session

Manage the resource kind in Equinix Metal. You can use *id* or *device_id* to lookup the resource. 


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Start first test bgp session
  hosts: localhost
  tasks:
  - equinix.cloud.metal_bgp_session:
      device_id: 8ea9837a-6d19-4607-b166-f7f7bb04b022
      address_family: ipv6
      default_route: true

```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`str`</center> | <center>Optional</center> | UUID of the BGP session.   |
| `device_id` | <center>`str`</center> | <center>Optional</center> | (Required) ID of device.   |
| `address_family` | <center>`str`</center> | <center>Optional</center> | (Required) ipv4 or ipv6.   |
| `default_route` | <center>`bool`</center> | <center>Optional</center> | (Optional) Boolean flag to set the default route policy. False by default.   |






## Return Values

- `metal_bgp_session` - The module object

    - Sample Response:
        ```json
        
        {
            "address_family": "ipv6",
            "changed": false,
            "device_id": "b068984f-f7d9-43a2-aa45-de04dcf4fe06",
            "id": "43cc0fa9-4b73-4629-a60b-2904ca919155",
        }
        
        ```


