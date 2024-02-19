# metal_bgp_session

Manage BGP sessions in Equinix Metal.Create, update or delete BGP session. To look up an existing session, pass only the *id* attribute.


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

```yaml
- name: Delete bgp session
  hosts: localhost
  tasks:
  - equinix.cloud.metal_bgp_session:
      id: 1273edef-39af-4df0-85bb-02a847a484d1
      state: absent

```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`str`</center> | <center>Optional</center> | UUID of the BGP session to look up   |
| `device_id` | <center>`str`</center> | <center>Optional</center> | Device ID for the BGP session   |
| `address_family` | <center>`str`</center> | <center>Optional</center> | BGP session address family, "ipv4" or "ipv6"   |
| `default_route` | <center>`bool`</center> | <center>Optional</center> | Boolean flag to set the default route policy. False by default.   |






## Return Values

- `metal_bgp_session` - The module object

    - Sample Response:
        ```json
        
         [
                {
                    "address_family": "ipv4",
                    "default_route": true,
                    "device_id": "2066d33e-7c43-4d78-87a3-aaa434913f7f",
                    "id": "fc2d43e6-d606-47f7-9611-9d77aee443b5"
                },
                {
                    "address_family": "ipv6",
                    "default_route": true,
                    "device_id": "bfab58c0-0723-49aa-a64e-6caf1b8ea2e2",
                    "id": "277d4a7a-82dd-4e7c-bf79-8a1de6882982"
                }
            ]
        
        ```


