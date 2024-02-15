# metal_project_bgp_config

Manage BGP config within Projec in Equinix Metal. You can use *project_id* lookup a bgp_config.If you want to create new bgp_config, you must provide *asn* and *deployment_type*.


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Create new BGP config
  hosts: localhost
  tasks:
    - equinix.cloud.metal_project_bgp_config:
        deployment_type: local
        asn: 65000
        md5: null
        use_case: "ansible test"
        project_id: "{{ test_project.id }}"

```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `project_id` | <center>`str`</center> | <center>**Required**</center> | UUID of the project where the BGP config belongs to   |
| `asn` | <center>`int`</center> | <center>**Required**</center> | Autonomous System Number for local BGP deployment   |
| `deployment_type` | <center>`str`</center> | <center>**Required**</center> | ""local" or "global", the local is likely to be usable immediately,  the global will need to be review by Equinix Metal engineers   |
| `md5` | <center>`str`</center> | <center>Optional</center> | Password for BGP session in plaintext (not a checksum)   |
| `use_case` | <center>`str`</center> | <center>Optional</center> | Information regarding what you're attempting to achieve with BGP.   |






## Return Values

- `metal_project_bgp_config` - The module object

    - Sample Response:
        ```json
        
        {
            "changed": true
        }
        
        ```


