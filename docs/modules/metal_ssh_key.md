# metal_ssh_key

Manage ssh_keys in Equinix Metal. You can use *id* or *label* to lookup a ssh_key. If you want to create new ssh_key, you must provide *name*.


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Create new ssh_key
  hosts: localhost
  tasks:
  - equinix.cloud.metal_ssh_key:
      name: "new ssh_key"

```

```yaml
- name: Create new ssh_key within non - default organization
  hosts: localhost
  tasks:
  - equinix.cloud.metal_ssh_key:
      name: "my org ssh_key"
      organization_id: "a4cc87f9-e00f-48c2-9460-74aa60beb6b0"

```

```yaml
- name: Remove ssh_key by id
  hosts: localhost
  tasks:
  - equinix.cloud.metal_ssh_key:
      id: "eef49903-7a09-4ca1-af67-4087c29ab5b6"
      state: absent

```

```yaml
- name: Create new ssh_key with non - default billing method
  hosts: localhost
  tasks:
  - equinix.cloud.metal_ssh_key:
      name: "newer ssh_key"
      payment_method_id: "abf49903-7a09-4ca1-af67-4087c29ab343"

```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`str`</center> | <center>Optional</center> | UUID of the ssh_key.   |
| `label` | <center>`str`</center> | <center>Optional</center> | The name of the ssh_key.  **(Updatable)** |
| `key` | <center>`str`</center> | <center>Optional</center> | The public key of the ssh_key.  **(Updatable)** |






## Return Values

- `metal_ssh_key` - The module object

    - Sample Response:
        ```json
        
        {
          "backend_transfer_enabled": false,
          "changed": false,
          "customdata": {},
          "description": "",
          "id": "7624f0f7-75b6-4271-bc64-632b80f87de2",
          "name": "ansible-integration-test-ssh_key-csle6t2y-ssh_key1_renamed",
          "organization_id": "70c2f878-9f32-452e-8c69-ab15480e1d99",
          "payment_method_id": "845b45a3-c565-47e5-b9b6-a86204a73d29"
        }
        
        ```


