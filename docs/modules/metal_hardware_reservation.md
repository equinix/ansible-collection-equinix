# metal_hardware_reservation

Lookup a single hardware_reservation by ID in Equinix Metal. 

This resource only fetches a single hardware_reservation by resource ID. 

It doesn't allow to create or update hardware_reservations.


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Lookup a single hardware_reservation by id
  hosts: localhost
  tasks:
  - equinix.cloud.metal_hardware_reservation:
      id: 7624f0f7-75b6-4271-bc64-632b80f87de2

```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`str`</center> | <center>**Required**</center> | UUID of the hardware_reservation.   |






## Return Values

- `metal_hardware_reservation` - The module object

    - Sample Response:
        ```json
        
        
        {
            "changed": false,
            "device_id": "",
            "id": "82323c08-a7f5-4e09-8b34-634e82e527c1",
            "plan": "m3.small.x86",
            "project_id": "52436fb2-ee46-4673-93a8-de2c2bdba33b",
            "provisionable": true,
            "spare": false,
            "switch_uuid": "00a5dbb7"
        }
        
        ```


