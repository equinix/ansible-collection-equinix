# metal_organization_info

Gather information about Equinix Metal organizations


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Gather information about all organizations
  hosts: localhost
  tasks:
      - equinix.cloud.metal_organization_info:

```

```yaml
- name: Gather information about organizations without projects
  hosts: localhost
  tasks:
      - equinix.cloud.metal_organization_info:
            without_projects: true

```

```yaml
- name: Get IDs or organizations with "ansible" in name
  hosts: localhost
  tasks:
      - equinix.cloud.metal_organization_info:
        register: organizations

  name: filter organizations
  set_fact:
      ansible_orgs: "{{ organizations.resources | selectattr('name', 'match', desired_name_substring) }}"

```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `personal` | <center>`bool`</center> | <center>Optional</center> | If true, only personal organizations will be returned.   |
| `without_projects` | <center>`bool`</center> | <center>Optional</center> | If true, only organizations without projects will be returned.   |






## Return Values



### Sample Response for resources
```json
{
  "description": "",
  "id": "72342434-9423-454e-8423-ab6546461d99",
  "name": "Tomas\u2019 Projects",
  "projects": [
    "43767515-846c-46ed-b0f5-23423422ea06",
    "635673f1-bce5-4a62-a47c-133342342349"
  ],
  "website": ""
}
```


