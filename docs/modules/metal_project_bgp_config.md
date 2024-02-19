# metal_project_bgp_config

You can use this module to enable BGP Config for a project. To lookup BGP Config of an existing project, call the module only with `project_id`. 


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Enable local BGP Config in Equinix Metal project
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
| `project_id` | <center>`str`</center> | <center>**Required**</center> | UUID of the project where BGP Config should be enabled   |
| `asn` | <center>`int`</center> | <center>**Required**</center> | Autonomous System Number for local BGP deployment   |
| `deployment_type` | <center>`str`</center> | <center>**Required**</center> | "local" or "global". Local deployment type is likely to be usable immediately,  "global" will need to be reviewed by Equinix Metal support.   |
| `md5` | <center>`str`</center> | <center>Optional</center> | Password for BGP session in plaintext (not a checksum)   |
| `use_case` | <center>`str`</center> | <center>Optional</center> | Description of your BGP use-case for Equinix Metal support   |






## Return Values

- `metal_project_bgp_config` - The module object

    - Sample Response:
        ```json
        
        {
            "changed": true
        }
        
        ```


