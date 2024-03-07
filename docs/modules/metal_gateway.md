# metal_gateway

Manage Metal Gateway in Equinix Metal. You can use *id* or *ip_reservation_id* to lookup a Gateway. If you want to create new resource, you must provide *project_id*, *virtual_network_id* and either *ip_reservation_id* or *private_ipv4_subnet_size*.


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Create new gateway with existing IP reservation
  hosts: localhost
  tasks:
  - equinix.cloud.metal_gateway:
      project_id: "a4cc87f9-e00f-48c2-9460-74aa60beb6b0"
      ip_reservation_id: "83b5503c-7b7f-4883-9509-b6b728b41491"
      virtual_network_id: "eef49903-7a09-4ca1-af67-4087c29ab5b6"

```

```yaml
- name: Create new gateway with new private /29 subnet
  hosts: localhost
  tasks:
  - equinix.cloud.metal_gateway:
      project_id: "{{ project.id }}"
      virtual_network_id: "{{ vlan.id }}"
      private_ipv4_subnet_size: 8

```

```yaml
- name: Lookup a gateway by ID
  hosts: localhost
  tasks:
  - equinix.cloud.metal_gateway:
      id: "eef49903-7a09-4ca1-af67-4087c29ab5b6"
    register: gateway

```

```yaml
- name: Lookup a gateway by IP reservation ID
  hosts: localhost
  tasks:
  - equinix.cloud.metal_gateway:
      ip_reservation_id: "a4cc87f9-e00f-48c2-9460-74aa60beb6b0"
    register: gateway

```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`str`</center> | <center>Optional</center> | UUID of the gateway.   |
| `project_id` | <center>`str`</center> | <center>Optional</center> | UUID of the project where the gateway is scoped to.   |
| `ip_reservation_id` | <center>`str`</center> | <center>Optional</center> | UUID of Public Reservation to associate with the gateway, the reservation must be in the same metro as the VLAN, conflicts with private_ipv4_subnet_size.   |
| `private_ipv4_subnet_size` | <center>`int`</center> | <center>Optional</center> | Size of the private IPv4 subnet to create for this metal gateway, must be one of 8, 16, 32, 64, 128. Conflicts with ip_reservation_id.   |
| `virtual_network_id` | <center>`str`</center> | <center>Optional</center> | UUID of the VLAN where the gateway is scoped to.   |
| `timeout` | <center>`int`</center> | <center>Optional</center> | Timeout in seconds for gateway to get to "ready" state, and for gateway to be removed  **(Default: `10`)** |






## Return Values



### Sample Responses for metal_gateway
```json
{
  "changed": true,
  "id": "1f4d30da-4041-406d-8d94-6ce929340d98",
  "ip_reservation_id": "fa017281-b10e-4b22-b449-35a93fb88d85",
  "metal_state": "ready",
  "project_id": "2e85a66a-ea6a-4e33-8029-cc5ab9a0bc91",
  "virtual_network_id": "4a06c542-e47c-4e3c-ab85-bfc3cba4004d"
}
```
```json
{
  "changed": true,
  "id": "be809e36-42a0-4a3b-982c-8f4487b9b9fc",
  "ip_reservation_id": "e5c4be29-e238-431a-8c5f-f44f30fd5098",
  "metal_state": "ready",
  "private_ipv4_subnet_size": 8,
  "project_id": "0491c16b-376d-4842-89d2-da3efead4991",
  "virtual_network_id": "f46ab2c8-1332-4f87-91e9-f3a6a81d9769"
}
```


