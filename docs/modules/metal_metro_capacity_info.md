# metal_metro_capacity_info

Gather information about the current capacity for Equinix Metal metros.


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Gather a list of metros and plans with their current capacity
  hosts: localhost
  tasks:
    - equinix.cloud.metal_metro_capacity_info:
        metal_api_token: "{{ lookup('env', 'METAL_API_TOKEN') }}"
      register: result

    - debug:
        var: result

```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `metal_api_token` | <center>`str`</center> | <center>**Required**</center> | The Equinix Metal API token to use.   |
| `metal_api_url` | <center>`str`</center> | <center>**Required**</center> | The Equinix Metal API URL to use.   |






## Return Values



### Sample Response for capacity
```json
{
  "am": {
    "c2.medium.x86": {
      "available_servers": 25,
      "level": "string"
    },
    "m2.xlarge.x86": {
      "available_servers": 15,
      "level": "string"
    }
  },
  "da": {
    "c2.medium.x86": {
      "available_servers": 26,
      "level": "string"
    },
    "m2.xlarge.x86": {
      "available_servers": 11,
      "level": "string"
    }
  },
  "dc": {
    "c2.medium.x86": {
      "available_servers": 14,
      "level": "string"
    },
    "m2.xlarge.x86": {
      "available_servers": 10,
      "level": "string"
    }
  }
}
```


