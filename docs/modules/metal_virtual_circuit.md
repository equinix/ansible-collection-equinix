# metal_virtual_circuit

Manage a Virtual Circuit in Equinix Metal. You can use *id* or *name* to lookup the resource. If you want to create new resource, you must provide *name*.


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: create first VRF virtual circuit for test
  hosts: localhost
  tasks:
  - equinix.cloud.metal_virtual_circuit:
      connection_id: "52373d96-ac4e-496c-8721-f7ef18a01331"
      port_id: "52373d96-ac4e-496c-8721-f7ef18a01331"
      name: "test_virtual_circuit"
      nni_vlan: 1056
      peer_asn: 66000
      project_id: "11e047e1-f51a-49c6-b5b2-1c7bfa4391e6"
      subnet: "192.168.151.126/31"
      vrf: "029c4219-04b7-4992-9fef-29ea7e2378a5"

```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`str`</center> | <center>Optional</center> | UUID of the Virtual Circuit.   |
| `name` | <center>`str`</center> | <center>Optional</center> | Name of the Virtual Circuit resource.  **(Updatable)** |
| `connection_id` | <center>`str`</center> | <center>Optional</center> | UUID of Connection where the VC is scoped to.   |
| `project_id` | <center>`str`</center> | <center>Optional</center> | UUID of the Project where the VC is scoped to.   |
| `port_id` | <center>`str`</center> | <center>Optional</center> | UUID of the Connection Port where the VC is scoped to.   |
| `nni_vlan` | <center>`int`</center> | <center>Optional</center> | Equinix Metal network-to-network VLAN ID.   |
| `vlan_id` | <center>`str`</center> | <center>Optional</center> | UUID of the VLAN to associate.   |
| `vnid` | <center>`str`</center> | <center>Optional</center> | VNID VLAN parameter, see the documentation for Equinix Fabric.   |
| `description` | <center>`str`</center> | <center>Optional</center> | Description for the Virtual Circuit resource.   |
| `tags` | <center>`str`</center> | <center>Optional</center> | Tags for the Virtual Circuit resource.   |
| `speed` | <center>`str`</center> | <center>Optional</center> | Speed of the Virtual Circuit resource.   |
| `vrf` | <center>`str`</center> | <center>Optional</center> | UUID of the VRF to associate.   |
| `peer_asn` | <center>`int`</center> | <center>Optional</center> | The BGP ASN of the peer. The same ASN may be the used across several VCs, but it cannot be the same as the local_asn of the VRF.   |
| `subnet` | <center>`str`</center> | <center>Optional</center> | A subnet from one of the IP blocks associated with the VRF that we will help create an IP reservation for. Can only be either a /30 or /31. For a /31 block, it will only have two IP addresses, which will be used for the metal_ip and customer_ip. For a /30 block, it will have four IP addresses, but the first and last IP addresses are not usable. We will default to the first usable IP address for the metal_ip.   |
| `metal_ip` | <center>`str`</center> | <center>Optional</center> | The Metal IP address for the SVI (Switch Virtual Interface) of the VirtualCircuit. Will default to the first usable IP in the subnet.   |
| `customer_ip` | <center>`str`</center> | <center>Optional</center> | The Customer IP address which the CSR switch will peer with. Will default to the other usable IP in the subnet.   |
| `md5` | <center>`str`</center> | <center>Optional</center> | The password that can be set for the VRF BGP peer   |
| `timeout` | <center>`int`</center> | <center>Optional</center> | Timeout in seconds for Virtual Circuit to get to "ready" state  **(Default: `15`)** |






## Return Values



### Sample Response for metal_virtual_circuit
```json
{
  "changed": false,
  "customer_ip": "192.168.151.127",
  "id": "84f35a2f-1e0c-43ee-bd94-87aec0c5ffec",
  "metal_ip": "192.168.151.126",
  "name": "test_virtual_circuit",
  "nni_vlan": 1056,
  "peer_asn": 66000,
  "port": {
    "href": "/metal/v1/connections/52373d96-ac4e-496c-8721-f7ef18a01331/ports/52373d96-ac4e-496c-8721-f7ef18a01331",
    "id": "4632fb7b-b1cf-48bc-8f20-a69b0a91d326"
  },
  "project": {
    "href": "/metal/v1/projects/11e047e1-f51a-49c6-b5b2-1c7bfa4391e6",
    "id": "11e047e1-f51a-49c6-b5b2-1c7bfa4391e6"
  },
  "project_id": "11e047e1-f51a-49c6-b5b2-1c7bfa4391e6",
  "status": "active",
  "subnet": "192.168.151.126/31",
  "tags": [],
  "type": "vrf",
  "vrf": {
    "bill": false,
    "href": "/metal/v1/vrfs/029c4219-04b7-4992-9fef-29ea7e2378a5",
    "id": "029c4219-04b7-4992-9fef-29ea7e2378a5"
  }
}
```


