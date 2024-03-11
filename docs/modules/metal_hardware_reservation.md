# metal_hardware_reservation

Lookup a single hardware_reservation by ID in Equinix Metal. This resource only fetches a single hardware_reservation by resource ID. It doesn't allow to create or update hardware_reservations.


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Lookup a single hardware_reservation by id
  hosts: localhost
  tasks:
  - equinix.cloud.metal_hardware_reservation:
      id: 7624f0f7-75b6-4271-bc64-632b80f87de2

```

```yaml
# Move hardware reservation between projects
- name: fetch hw reservation resource 
  equinix.cloud.metal_hardware_reservation:
    id: "{{ metal_hardware_reservation_id }}"
    register: hwres

- name: create new project to move the hw res to
  equinix.cloud.metal_project:
    name: "destination-project"
    register: project

- name: move hw reservation to new project
  equinix.cloud.metal_hardware_reservation:
    id: "{{ metal_hardware_reservation_id }}"
    project_id: "{{ project.id }}"

- name: move hw reservation to original project
  equinix.cloud.metal_hardware_reservation:
    id: "{{ metal_hardware_reservation_id }}"
    project_id: "{{ hwres.project_id }}"     

```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`str`</center> | <center>**Required**</center> | UUID of the hardware_reservation.   |
| `project_id` | <center>`str`</center> | <center>Optional</center> | UUID of parent project containing the hardware_reservation. It can be changed.  **(Updatable)** |






## Return Values



### Sample Response for metal_hardware_reservation
```json
{
  "changed": false,
  "device_id": "",
  "id": "82323c08-a7f5-4e09-8b34-634e82e527c1",
  "plan": "m3.small.x86",
  "project_id": "52436fb2-ee46-4673-93a8-de2c2bdba33b",
  "provisionable": true,
  "spare": false,
  "switch_uuid": "00a5dbb7"
}
```


