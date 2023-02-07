# metal_project

Manage Projects in Equinix Metal.

You can use *id* or *name* to lookup a project.

If you want to create new project, you must provide *name*.


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
- name: Create new project within non-default organization
  hosts: localhost
  tasks:
      equinix.cloud.metal_project:
          name: "my org project"
          organization_id: a4cc87f9-e00f-48c2-9460-74aa60beb6b0

```

```yaml
- name: Remove project by id
  hosts: localhost
  tasks:
      equinix.cloud.metal_project:
          state: absent
          id: eef49903-7a09-4ca1-af67-4087c29ab5b6

```

```yaml
- name: Create new project with non-default billing method
  hosts: localhost
  tasks:
      equinix.cloud.metal_project:
          name: "newer project"
          payment_method_id: "abf49903-7a09-4ca1-af67-4087c29ab343"

```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `metal_api_token` | <center>`str`</center> | <center>**Required**</center> | API token for Equinix Metal. Can be set via METAL_API_TOKEN environment variable.   |
| `id` | <center>`str`</center> | <center>Optional</center> | UUID of the project.   |
| `name` | <center>`str`</center> | <center>Optional</center> | The name of the project.  **(Updatable)** |
| `organization_id` | <center>`str`</center> | <center>Optional</center> | UUID of the organization containing the project. When not specified, the default organization will be used.   |
| `payment_method_id` | <center>`str`</center> | <center>Optional</center> | UUID of payment method to use for the project. When blank, the API assumes default org payment method.  **(Updatable)** |
| `customdata` | <center>`str`</center> | <center>Optional</center> | Custom data about the project to create.  **(Updatable)** |
| `backend_transfer_enabled` | <center>`bool`</center> | <center>Optional</center> | Enable backend transfer for the project.  **(Updatable)** |
| `metal_api_url` | <center>`str`</center> | <center>Optional</center> | API URL for Equinix Metal. Can be set via METAL_API_URL environment variable.  **(Default: `https://api.equinix.com/metal/v1`)** |
| `metal_ua_prefix` | <center>`str`</center> | <center>Optional</center> | User agent prefix for Equinix Metal. Can be set via METAL_UA_PREFIX environment variable.   |
| `state` | <center>`str`</center> | <center>Optional</center> | Desired state of the resource.  **(Choices: `present`, `absent`; Default: `present`)** |






## Return Values

- `id` - UUID of the project.

    - Sample Response:
        ```json
        eef49903-7a09-4ca1-af67-4087c29ab5b6
        ```


- `name` - Name of the project.

    - Sample Response:
        ```json
        new project
        ```


- `organization_id` - UUID of the organization the project belongs to.

    - Sample Response:
        ```json
        a4cc87f9-e00f-48c2-9460-74aa60beb6b0
        ```


- `payment_method_id` - UUID of the payment method used for the project.

    - Sample Response:
        ```json
        abf49903-7a09-4ca1-af67-4087c29ab343
        ```


- `customdata` - Custom data about the project.

    - Sample Response:
        ```json
        {"setting": 12}
        ```


- `backend_transfer_enabled` - Whether backend transfer is enabled for the project.

    - Sample Response:
        ```json
        True
        ```


