# metal_vrf_info

Gather information about Equinix VRFs


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Gather information about VRFs in a project
  hosts: localhost
  tasks:
      - equinix.cloud.metal_vrf_info:
          project_id: 2a5122b9-c323-4d5c-b53c-9ad3f54273e7

```

```yaml
- name: Retrieve information about resources within a specific VRF
  hosts: localhost
  tasks:
      - equinix.cloud.metal_vrf_info:
          project_id: 2a5122b9-c323-4d5c-b53c-9ad3f54273e7
          vrf_id: f421024d-c1e6-4886-a64d-5b2515696200

```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `project_id` | <center>`str`</center> | <center>**Required**</center> | Project ID where to look up VRFs.   |
| `vrf_id` | <center>`str`</center> | <center>Optional</center> | ID of the VRF resource   |






## Return Values

- `resources` - Found resources

    - Sample Response:
        ```json
        
        
        [
                {
                    "description": "Test VRF with ASN 65000",
                    "id": "8b24de5b-c70e-4a4e-9dd2-064ceb09c587",
                    "ip_ranges": [
                        "192.168.100.0/25",
                        "192.168.200.0/25"
                    ],
                    "local_asn": 65000,
                    "metro": {
                        "href": "/metal/v1/locations/metros/108b2cfb-246b-45e3-885a-bf3e82fce1a0",
                        "id": "108b2cfb-246b-45e3-885a-bf3e82fce1a0"
                    },
                    "name": "ansible-integration-test-vrf-nw6dgvh5",
                    "project_id": "06aea391-fd87-4cc7-9f4b-76f9e38fd4a4"
                }
            ]
        ```


