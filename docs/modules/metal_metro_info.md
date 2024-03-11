# metal_metro_info

Gather information about Equinix Metal metros


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Select all metros and filter american metros
  hosts: localhost
  tasks:
    - name: Select all metros
      equinix.cloud.metal_metro_info:
      register: metros

    - name: Store american metros to fact ametros
      set_fact:
        ametros: "{{ metros.resources | selectattr('country', 'equalto', 'US') | list }}"

```










## Return Values



### Sample Responses for resources
```json
{
  "code": "sv",
  "country": "US",
  "id": "2991b022-b8c4-497e-8db7-5a407c3a209b",
  "name": "Silicon Valley"
}
```
```json
{
  "code": "la",
  "country": "US",
  "id": "bb059cc0-0b2a-4f5b-8a55-219e6b4240da",
  "name": "Los Angeles"
}
```
```json
{
  "code": "ch",
  "country": "US",
  "id": "60666d92-e00f-43a8-a9f8-fddf665390ca",
  "name": "Chicago"
}
```
```json
{
  "code": "da",
  "country": "US",
  "id": "d3d6b29f-042d-43b7-b3ce-0bf53d5754ca",
  "name": "Dallas"
}
```


