# Migration Guide: equinix.metal to equinix.cloud

This migration guide is designed to help you transition from the [equinix.metal Ansible collection](https://github.com/equinix/ansible-collection-metal) to the newer [equinix.cloud collection](https://github.com/equinix-labs/ansible-collection-equinix) (on GitHub as [equinix-labs/ansible-collection-equinix](https://github.com/equinix-labs/ansible-collection-equinix)).

## Pre-Migration Checklist

- Ensure that you are using Ansible version >=2.9.10, as this is compatible with the equinix.metal collection
- Ensure that Python 2.7 or greater is installed, as it is required for equinix.metal
- Document all the equinix.metal modules and plugins you are currently using, as you will need to check for their equivalents or changes in the equinix.cloud collection.

## Installing equinix.cloud Collection

Follow instructions on https://github.com/equinix-labs/ansible-collection-equinix#installation

## Authentication changes

For the equinix.cloud collection, ensure that you have an Equinix Metal API token. Set the `METAL_AUTH_TOKEN` environment variable with your API token:

```sh
export METAL_AUTH_TOKEN=your_api_token_here
```

## Updating Playbooks

- Review and compare your current playbooks that use `equinix.metal`. Look for tasks that reference modules starting with `equinix.metal` (e.g., `equinix.metal.device`, `equinix.metal.project_info`, etc.)
- Replace these references with the new module names under the equinix.cloud namespace. For example, if you have a task that uses `equinix.metal.device`, you would update it to `equinix.cloud.metal_device`.
- Update any task parameters if there have been changes between the collections. This may require checking the documentation for each module within the equinix.cloud collection to confirm parameter names and acceptable values.

## Module-mapping Table

| equinix.metal Module                                                                                              | equinix.cloud Equivalent                                                                                              |
|-------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|
| [equinix.metal.device](https://github.com/equinix/ansible-collection-metal/blob/main/docs/equinix.metal.device_module.rst)                              | [equinix.cloud.metal_device](https://github.com/equinix-labs/ansible-collection-equinix/blob/main/docs/modules/metal_device.md)                              |
| [equinix.metal.device_info](https://github.com/equinix/ansible-collection-metal/blob/main/docs/equinix.metal.device_info_module.rst)                        | [equinix.cloud.metal_device_info](https://github.com/equinix-labs/ansible-collection-equinix/blob/main/docs/modules/metal_device_info.md)                         |
| [equinix.metal.facility_info](https://github.com/equinix/ansible-collection-metal/blob/main/docs/equinix.metal.facility_info_module.rst)                      | Not present in the new collection                                                                                      |
| [equinix.metal.ip_info](https://github.com/equinix/ansible-collection-metal/blob/main/docs/equinix.metal.ip_info_module.rst)                                | [equinix.cloud.metal_ip_assignment_info](https://github.com/equinix-labs/ansible-collection-equinix/blob/main/docs/modules/metal_ip_assignment_info.md)                   |
| [equinix.metal.ip_subnet](https://github.com/equinix/ansible-collection-metal/blob/main/docs/equinix.metal.ip_subnet_module.rst)                            | [equinix.cloud.metal_ip_assignment](https://github.com/equinix-labs/ansible-collection-equinix/blob/main/docs/modules/metal_ip_assignment.md)                           |
| [equinix.metal.operating_system_info](https://github.com/equinix/ansible-collection-metal/blob/main/docs/equinix.metal.operating_system_info_module.rst)      | [equinix.cloud.metal_operating_system_info](https://github.com/equinix-labs/ansible-collection-equinix/blob/main/docs/modules/metal_operating_system_info.md)             |
| [equinix.metal.org_info](https://github.com/equinix/ansible-collection-metal/blob/main/docs/equinix.metal.org_info_module.rst)                               | [equinix.cloud.metal_organization_info](https://github.com/equinix-labs/ansible-collection-equinix/blob/main/docs/modules/metal_organization_info.md)                      |
| [equinix.metal.plan_info](https://github.com/equinix/ansible-collection-metal/blob/main/docs/equinix.metal.plan_info_module.rst)                             | Not present in the new collection                                                                                      |
| [equinix.metal.project](https://github.com/equinix/ansible-collection-metal/blob/main/docs/equinix.metal.project_module.rst)                                | [equinix.cloud.metal_project](https://github.com/equinix-labs/ansible-collection-equinix/blob/main/docs/modules/metal_project.md)                                |
| [equinix.metal.project_info](https://github.com/equinix/ansible-collection-metal/blob/main/docs/equinix.metal.project_info_module.rst)                       | [equinix.cloud.metal_project_info](https://github.com/equinix-labs/ansible-collection-equinix/blob/main/docs/modules/metal_project_info.md)                       |
| [equinix.metal.sshkey](https://github.com/equinix/ansible-collection-metal/blob/main/docs/equinix.metal.sshkey_module.rst)                                   | [equinix.cloud.metal_ssh_key](https://github.com/equinix-labs/ansible-collection-equinix/blob/main/docs/modules/metal_ssh_key.md)                                   |
| [equinix.metal.sshkey_info](https://github.com/equinix/ansible-collection-metal/blob/main/docs/equinix.metal.sshkey_info_module.rst)                         | [equinix.cloud.metal_ssh_key_info](https://github.com/equinix-labs/ansible-collection-equinix/blob/main/docs/modules/metal_ssh_key_info.md)                         |
| [equinix.metal.user_info](https://github.com/equinix/ansible-collection-metal/blob/main/docs/equinix.metal.user_info_module.rst)                             | Not present in the new collection                                                                                      |
| [equinix.metal.capacity_info](https://github.com/equinix/ansible-collection-metal/blob/main/docs/equinix.metal.capacity_info_module.rst)                     | Not present in the new collection                                                                                      |
| [equinix.metal.operating_system_info](https://github.com/equinix/ansible-collection




## Testing

After updating your playbooks, it's essential to test them in a non-production environment to ensure that all tasks execute as expected and that there are no issues with the new collection.

## Support and Additional Resources

- Utilize the [Equinix Metal Community Slack](https://slack.equinixmetal.com/) and [Community Site](https://community.equinix.com/) for support and to engage with other users who have made similar migrations.
- Keep an eye on the [Ansible Collection for Equinix GitHub repository](https://github.com/equinix-labs/ansible-collection-equinix) for updates, and submit new feature requests on the Equinix Metal Roadmap.

Remember that while the equinix.metal and equinix.cloud collections may be similar, there may be differences in functionality and features. Always refer to the official documentation for the most accurate and up-to-date information.

