# metal_device

Reads device inventories from Equinix Metal. Uses YAML configuration file that ends with equinix_metal.(yml|yaml). ansible_host is set to first public IP address of the device.


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
# Minimal example using environment var credentials
plugin: equinix.cloud.metal_device

# Example using constructed features to create groups and set ansible_host
plugin: equinix.cloud.metal_device
# keyed_groups may be used to create custom groups
strict: False
keyed_groups:
  # Add devices to tag_Name groups for each tag
  - prefix: tag
    key: tags
  # Add devices to e.g. equinix_metal_plan_c3_small_x86
  - prefix: equinix_metal_plan
    key: plan
  # Create a group per region e.g. equinix_metal_metro_sv
  - key: metro
    prefix: equinix_metal_metro
  # Create a group per device state e.g. equinix_metal_state_active
  - key: state
    prefix: equinix_metal_state

```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `plugin` | <center>`str`</center> | <center>**Required**</center> | Token that ensures this is a source file for the plugin.  **(Choices: `equinix_metal`, `equinix.cloud.metal_device`)** |
| `metal_api_token` | <center>`str`</center> | <center>**Required**</center> | Equinix Metal API token. Can also be specified via METAL_AUTH_TOKEN environment variable.   |
| `project_ids` | <center>`list`</center> | <center>Optional</center> | List of Equinix Metal project IDs to query for devices.   |
| [`keyed_groups` (sub-options)](#keyed_groups) | <center>`list`</center> | <center>Optional</center> | List of groups to create based on the values of a variable.   |





### keyed_groups

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `key` | <center>`str`</center> | <center>Optional</center> | The key to group by.   |
| `prefix` | <center>`str`</center> | <center>Optional</center> | Prefix to prepend to the group name.   |
| `separator` | <center>`str`</center> | <center>Optional</center> | Separator to use when joining the key and value.   |






## Return Values

