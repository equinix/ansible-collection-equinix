# metal_hardware_reservation_info

Gather information about Equinix Metal hardware_reservations


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Gather information about all hardware_reservations in parent project 
  hosts: localhost
  tasks:
      - equinix.cloud.metal_hardware_reservation_info:
          project_id: 2a5122b9-c323-4d5c-b53c-9ad3f54273e7

```

```yaml

```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `project_id` | <center>`str`</center> | <center>**Required**</center> | UUID of parent project containing the hardware_reservations.   |






## Return Values

- `hardware_reservations` - Found hardware reservations

    - Sample Response:
        ```json
        
        [
            {
                "device_id": "",
                "id": "84363c08-a7f5-4e09-8b34-634e82e527c1",
                "plan": "m3.small.x86",
                "project_id": "c6ba3fb2-ee46-4623493a8-de324234a33b",
                "provisionable": false,
                "spare": false,
                "switch_uuid": "00a324b7"
            }
        ]
        ```


