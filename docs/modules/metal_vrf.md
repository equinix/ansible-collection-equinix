# metal_vrf

Create a VRF in a metro, with IP ranges that you want the VRF to route and forward.


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Create new Equinix Metal VRF
  hosts: localhost
  tasks:
    - equinix.cloud.metal_vrf:
        name: "example-vrf"
        description: "VRF with ASN 65000 and a pool of address space that includes 192.168.100.0/25"
        metro: "da"
        local_asn: 65000
        ip_ranges:
          - "192.168.100.0/25"
          - "192.168.200.0/25"
        project_id: "your_project_id_here"

```

```yaml
- name: Create new Equinix Metal VRF
  hosts: localhost
  tasks:
    - equinix.cloud.metal_vrf:
        name: "example-vrf"
        description: "VRF with ASN 65000 and a pool of address space that includes 192.168.100.0/25"
        metro: "da"
        local_asn: 65000
        ip_ranges:
          - "192.168.100.0/25"
          - "192.168.200.0/25"
        project_id: "your_project_id_here"
        bgp_dynamic_neighbors_bfd_enabled: 

```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`str`</center> | <center>Optional</center> | UUID of the VRF.   |
| `description` | <center>`str`</center> | <center>Optional</center> | Description of the VRF.   |
| `name` | <center>`str`</center> | <center>Optional</center> | User-supplied name of the VRF, unique to the project.   |
| `metro` | <center>`str`</center> | <center>Optional</center> | Metro ID or Code where the VRF will be deployed.   |
| `local_asn` | <center>`int`</center> | <center>Optional</center> | The 4-byte ASN set on the VRF.  **(Updatable)** |
| `ip_ranges` | <center>`list`</center> | <center>Optional</center> | All IPv4 and IPv6 Ranges that will be available to BGP Peers. IPv4 addresses must be /8 or smaller with a minimum size of /29. IPv6 must be /56 or smaller with a minimum size of /64. Ranges must not overlap other ranges within the VRF.  **(Updatable)** |
| `project_id` | <center>`str`</center> | <center>Optional</center> | Project ID where the VRF will be deployed.   |
| `bgp_dynamic_neighbors_bfd_enabled` | <center>`bool`</center> | <center>Optional</center> | Toggle BFD on dynamic bgp neighbors sessions.  **(Updatable)** |
| `bgp_dynamic_neighbors_enabled` | <center>`bool`</center> | <center>Optional</center> | Toggle to enable the dynamic bgp neighbors feature on the VRF.  **(Updatable)** |
| `bgp_dynamic_neighbors_export_route_map` | <center>`bool`</center> | <center>Optional</center> | Toggle to export the VRF route-map to the dynamic bgp neighbors.  **(Updatable)** |






## Return Values

- `metal_vrf` - The module object

    - Sample Response:
        ```json
        
        {
            "changed": false,
            "description": "Test VRF with ASN 65000",
            "id": "f4a7863c-fcbf-419c-802c-3c6d3ad9529e",
            "invocation": {
                "module_args": {
                    "description": null,
                    "id": "f4a7863c-fcbf-419c-802c-3c6d3ad9529e",
                    "ip_ranges": [
                        "192.168.100.0/25",
                        "192.168.200.0/25"
                    ],
                    "local_asn": 65000,
                    "metal_api_token": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER",
                    "metal_api_url": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER",
                    "metal_ua_prefix": "",
                    "metro": "am",
                    "name": "ansible-integration-test-vrf-6yww6pyz",
                    "project_id": "9934e474-04a1-46a3-842b-5f3dc0ed0eba",
                    "state": "present"
                }
            },
            "ip_ranges": [
                "192.168.100.0/25",
                "192.168.200.0/25"
            ],
            "local_asn": 65000,
            "metro": {
                "href": "/metal/v1/locations/metros/108b2cfb-246b-45e3-885a-bf3e82fce1a0",
                "id": "108b2cfb-246b-45e3-885a-bf3e82fce1a0"
            },
            "name": "ansible-integration-test-vrf-6yww6pyz",
            "project_id": "9934e474-04a1-46a3-842b-5f3dc0ed0eba"
        }
        
        ```


