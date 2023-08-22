# metal_connection

Manage the interconnection in Equinix Metal. You can use *id* or *name* to lookup the resource. If you want to create new resource, you must provide *project_id*, *name*, *type*, *redundancy* and *speed*.


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Create new connection
  hosts: localhost
  tasks:
  - equinix.cloud.metal_connection:
      project_id: "Bhf47603-7a09-4ca1-af67-4087c13ab5b6"
      name: "new connection"
      type: "dedicated"
      redundancy: "primary"
      speed: "50Mbps"
      metro: "am"

```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`str`</center> | <center>Optional</center> | UUID of the connection.   |
| `project_id` | <center>`str`</center> | <center>Optional</center> | UUID of the project this connection belongs to.   |
| `contact_email` | <center>`str`</center> | <center>Optional</center> | Email for the person to contact for inquires.  **(Updatable)** |
| `description` | <center>`str`</center> | <center>Optional</center> | Description of the connection.  **(Updatable)** |
| `metro` | <center>`str`</center> | <center>Optional</center> | Metro where the connection will be created   |
| `mode` | <center>`str`</center> | <center>Optional</center> | Mode for connections in IBX facilities with the dedicated type - standard or tunnel  **(Updatable)** |
| `name` | <center>`str`</center> | <center>Optional</center> | Name of the connection resource  **(Updatable)** |
| `redundancy` | <center>`str`</center> | <center>Optional</center> | Connection redundancy - redundant or primary  **(Updatable)** |
| `service_token_type` | <center>`str`</center> | <center>Optional</center> | Only used with shared connection. Type of service token to use for the connection, a_side or z_side   |
| `speed` | <center>`int`</center> | <center>Optional</center> | Port speed. Required for a_side connections. Allowed values are ['50Mbps', '200Mbps', '500Mbps', '1Gbps', '2Gbps', '5Gbps', '10Gbps']   |
| `tags` | <center>`int`</center> | <center>Optional</center> | Tags attached to the connection  **(Updatable)** |
| `type` | <center>`int`</center> | <center>Optional</center> | Connection type - dedicated or shared   |
| `vlans` | <center>`list`</center> | <center>Optional</center> | Only used with shared connection. VLANs to attach. Pass one vlan for Primary/Single connection and two vlans for Redundant connection   |
| `vrfs` | <center>`list`</center> | <center>Optional</center> | List of connection ports - primary (`ports[0]`) and secondary (`ports[1]`)   |






## Return Values

- `metal_resource` - The module object

    - Sample Response:
        ```json
        
        {
            "project_id": "Bhf47603-7a09-4ca1-af67-4087c13ab5b6"
            "name": "new connection"
            "type": "dedicated"
            "redundancy": "primary"
            "speed": "50Mbps"
            "metro": "am"
        }
        
        ```


