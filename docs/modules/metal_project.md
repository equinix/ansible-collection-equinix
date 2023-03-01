# metal_project

Manage Projects in Equinix Metal. You can use *id* or *name* to lookup a project. If you want to create new project, you must provide *name*.


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Create new project
  hosts: localhost
  tasks:
    equinix.cloud.metal_project:
      name: "new project"

```

```yaml
- name: Create new project within non - default organization
  hosts: localhost
  tasks:
    equinix.cloud.metal_project:
      name: "my org project"
      organization_id: "a4cc87f9-e00f-48c2-9460-74aa60beb6b0"

```

```yaml
- name: Remove project by id
  hosts: localhost
  tasks:
    equinix.cloud.metal_project:
      id: "eef49903-7a09-4ca1-af67-4087c29ab5b6"
      state: absent

```

```yaml
- name: Create new project with non - default billing method
  hosts: localhost
  tasks:
    equinix.cloud.metal_project:
      name: "newer project"
      payment_method_id: "abf49903-7a09-4ca1-af67-4087c29ab343"

```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`str`</center> | <center>Optional</center> | UUID of the project.   |
| `name` | <center>`str`</center> | <center>Optional</center> | The name of the project.  **(Updatable)** |
| `organization_id` | <center>`str`</center> | <center>Optional</center> | UUID of the organization containing the project. When not specified, the default organization will be used.   |
| `payment_method_id` | <center>`str`</center> | <center>Optional</center> | UUID of payment method to use for the project. When blank, the API assumes default org payment method.  **(Updatable)** |
| `customdata` | <center>`str`</center> | <center>Optional</center> | Custom data about the project to create.  **(Updatable)** |
| `backend_transfer_enabled` | <center>`bool`</center> | <center>Optional</center> | Enable backend transfer for the project.  **(Updatable)** |






## Return Values

- `metal_project` - The module object

    - Sample Response:
        ```json
        
        {
          "backend_transfer_enabled": false,
          "changed": false,
          "customdata": {},
          "description": "",
          "id": "7624f0f7-75b6-4271-bc64-632b80f87de2",
          "name": "ansible-integration-test-project-csle6t2y-project1_renamed",
          "organization_id": "70c2f878-9f32-452e-8c69-ab15480e1d99",
          "payment_method_id": "845b45a3-c565-47e5-b9b6-a86204a73d29"
        }
        
        ```


