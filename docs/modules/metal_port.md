# metal_port

This module doesn't create a resource in Equinix Metal, but rather provides finer control for [Layer 2 networking](https://deploy.equinix.com/developers/docs/metal/layer2-networking/overview/).


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: capture first bond port id for my_device
  set_fact:
    bond_port_id: "{{ my_device.network_ports | selectattr('name', 'match', 'bond0') | map(attribute='id') | first }}"

- name: convert first bond port to layer 2
  equinix.cloud.metal_port:
    id: "{{ bond_port_id }}"
    bonded: true
    layer2: true


- name: attach VLANs by UUID
  equinix.cloud.metal_port:
    id: "{{ bond_port_id }}"
    bonded: true
    layer2: true
    vlan_ids:
      - "<some_vlan_id>"
      - "<another_vlan_id>"

- name: assign native VLAN by UUID
  equinix.cloud.metal_port:
    id: "{{ bond_port_id }}"
    bonded: true
    layer2: true
    native_vlan_id: "{{ test_vlan1.id }}"


- name: disbond the bond port
  equinix.cloud.metal_port:
    id: "{{ bond_port_id }}"
    bonded: false
    layer2: true

```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`str`</center> | <center>**Required**</center> | UUID of the port.   |
| `bonded` | <center>`bool`</center> | <center>**Required**</center> | Whether the port should be bonded.   |
| `layer2` | <center>`bool`</center> | <center>Optional</center> | Whether the port should be in Layer 2 mode.  **(Updatable)** |
| `vlan_ids` | <center>`list`</center> | <center>Optional</center> | UUIDs of VLANs that should be assigned to the port  **(Updatable)** |
| `native_vlan_id` | <center>`str`</center> | <center>Optional</center> | UUID of native VLAN of the port  **(Updatable)** |






## Return Values



### Sample Response for metal_port
```json
{
  "bonded": true,
  "id": "7624f0f7-75b6-4271-bc64-632b80f87de2",
  "layer2": true
}
```


