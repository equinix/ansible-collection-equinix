# metal_user_info

Gather information about the current user for Equinix Metal


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Gather information about the current current user
  hosts: localhost
  tasks:
    - equinix.cloud.metal_user_info:
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



### Sample Response for user
```json
{
  "avatar_thumb_url": "https://www.gravatar.com/avatar/49d55cbf53f2dae15bfa4c3a3fb884f9?d=mm",
  "avatar_url": "https://www.gravatar.com/avatar/49d55cbf53f2dae15bfa4c3a3fb884f9?d=mm",
  "created_at": "2019-08-24T14:15:22Z",
  "customdata": {},
  "default_organization_id": "7498eaa8-62af-4757-81e0-959250fc9cd5",
  "email": "john.doe@email.com",
  "emails": [
    {
      "href": "string"
    }
  ],
  "first_name": "John",
  "full_name": "John Doe",
  "href": "/metal/v1/users/497f6eca-6276-4993-bfeb-53cbbbba6f08",
  "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
  "last_login_at": "2019-08-24T14:15:22Z",
  "last_name": "Doe",
  "max_projects": 0,
  "short_id": "497f6eca",
  "timezone": "America/New_York",
  "two_factor_auth": "",
  "updated_at": "2019-08-24T14:15:22Z"
}
```


