# metal_organization

Lookup a single organization by ID in Equinix Metal. 

This resource only fetches a single organization by resource ID. 

It doesn't allow to create or update organizations.


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Lookup a single organization by id
  hosts: localhost
  tasks:
  - equinix.cloud.metal_organization:
      id: 7624f0f7-75b6-4271-bc64-632b80f87de2

```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`str`</center> | <center>**Required**</center> | UUID of the organization.   |






## Return Values

- `metal_organization` - The module object

    - Sample Response:
        ```json
        
        {
        
          "changed": false,
          "description": "",
          "id": "70c2f878-9f32-452e-8c69-ab15480e1d99",
          },
          "name": "Tomas’ Projects",
          "projects": [
              "18234234-0432-4eb5-9636-5f05671ff33a",
              "4394a515-8423-46ed-b0f5-8bfd09573a06",
              "52000324-e342-4673-93a8-de242342343b",
              "64234231-bce5-4a62-a47c-14234d7ea8d9",
              "81423459-f69d-40c4-9b72-51e23c324243",
              "e9324234-6423-4232-8423-854234238106"
          ],
          "website": ""
        }
        
        ```


