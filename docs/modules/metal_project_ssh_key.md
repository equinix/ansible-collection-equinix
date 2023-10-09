# metal_project_ssh_key

Manage project ssh key in Equinix Metal. Read more about personal and project SSH keys in [Equinix Metal documentation](https://deploy.equinix.com/developers/docs/metal/accounts/ssh-keys/#personal-keys-vs-project-keys). You can use *id* or *label* to lookup a project SSH key. If you want to create new resource, you must provide *label*, *key* and *project_id*.


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Create new project project ssh_key
  hosts: localhost
  tasks:
  - equinix.cloud.metal_project_ssh_key:
      label: "test_key"
      key: "ssh-dss AAAAB3NzaC1kc3MAAACBAPLEVntPO3L7VUbEwWZ2ErkQJ3KJ8o9kFXJrPcpvVfdNag4jIhQDqbtAUgUy6BclhhbfH9l5nlGTprrpEFkxm/GL91qJUX6xrPkDMjMqx2wSKa4YraReOrCOfkqqEkC3o3G/gYSuvTzLgp2rmPiflypftZyzNM4JZT8jDwFGotJhAAAAFQDPk43bayONtUxjkAcOf+6zP1qb6QAAAIBZHHH0tIlth5ot+Xa/EYuB/M4qh77EkrWUbER0Kki7suskw/ffdKQ0y/v+ZhoAHtBU7BeE3HmP98Vrha1i4cOU+A7DCqV+lK/a+5LoEpua0M2M+VzNSGluYuV4qGpAOxNh3mxUi2R7yXxheN1oks1ROJ/bqkF4BJQXU9Nv49GkZgAAAIByWcsFeOitvzyDaNJOZzEHv9fqGuj0L3maRVWb6O47HGzlMzniIy8WjL2dfgm2/ek+NxVR/yFnYTKDPr6+0uqSD/cb4eHaFbIj7v+k7H8hA1Ioz+duJ1ONAjn6KwneXxOXu15bYIR49P7Go0s9jCdSAP/r9NE5TnE3yiRiQzgEzw== tomk@node"
      project_id: "b8c6c653-3c96-446e-987e-9c4d12f25353"

```

```yaml
- name: Remove project ssh_key by id
  hosts: localhost
  tasks:
  - equinix.cloud.metal_project_ssh_key:
      id: "eef49903-7a09-4ca1-af67-4087c29ab5b6"
      state: absent

```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`str`</center> | <center>Optional</center> | UUID of the ssh_key.   |
| `label` | <center>`str`</center> | <center>Optional</center> | The name of the ssh_key.  **(Updatable)** |
| `key` | <center>`str`</center> | <center>Optional</center> | The public key of the project ssh_key.  **(Updatable)** |
| `project_id` | <center>`str`</center> | <center>Optional</center> | The ID of parent project.  **(Updatable)** |






## Return Values

- `metal_project_ssh_key` - The module object

    - Sample Response:
        ```json
        
        {
          "fingerprint": "98:9c:35:ed:f9:75:5b:52:e2:70:50:22:ea:77:5b:b6",
          "id": "eef49903-7a09-4ca1-af67-4087c29ab5b6",
          "key": "ssh-dss AAAAB4NzaC1kc3MAAACBAPLEVntPO3L7VUbEwWZ2ErkQJ3KJ8o9kFXJrPcpvVfdNag4jIhQDqbtAUgUy6BclhhbfH9l5nlGTprrpEFkxm/GL91qJUX6xrPkDMjMqx2wSKa4YraReOrCOfkqqEkC3o3G/gYSuvTzLgp2rmPiflypftZyzNM4JZT8jDwFGotJhAAAAFQDPk43bayONtUxjkAcOf+6zP1qb6QAAAIBZHHH0tIlth5ot+Xa/EYuB/M4qh77EkrWUbER0Kki7suskw/ffdKQ0y/v+ZhoAHtBU7BeE3HmP98Vrha1i4cOU+A7DCqV+lK/a+5LoEpua0M2M+VzNSGluYuV4qGpAOxNh3mxUi2R7yXxheN1oks1ROJ/bqkF4BJQXU9Nv49GkZgAAAIByWcsFeOitvzyDaNJOZzEHv9fqGuj0L3maRVWb6O47HGzlMzniIy8WjL2dfgm2/ek+NxVR/yFnYTKDPr6+0uqSD/cb4eHaFbIj7v+k7H8hA1Ioz+duJ1ONAjn6KwneXxOXu15bYIR49P7Go0s9jCdSAP/r9NE5TnE3yiRiQzgEzw== tomk@xps",
          "label": "test_key",
          "project_id": "b8c6c653-3c96-446e-987e-9c4d12f25353"
        }
        
        ```


