# Equinix Ansible Collection
[![Ansible Galaxy](https://img.shields.io/badge/galaxy-equinix.cloud-660198.svg?style=flat)](https://galaxy.ansible.com/equinix/cloud/) 
![Tests](https://img.shields.io/github/actions/workflow/status/equinix-labs/ansible-collection-equinix/integration-tests.yml?branch=main)

The Ansible Collection Equinix contains various plugins for managing Equinix services.

<!--start requires_ansible-->
## Ansible version compatibility

This collection has been tested against following Ansible versions: **>=2.9.10**.

Plugins and modules within a collection may be tested with only specific Ansible versions.
A collection may contain metadata that identifies these versions.
PEP440 is the schema used to describe the versions of Ansible.
<!--end requires_ansible-->

<!--start collection content-->
### Modules

Modules for managing equinix infrastructure.

Name | Description |
--- | ------------ |
[equinix.cloud.metal_device](https://github.com/equinix-labs/ansible-collection-equinix/blob/0.0.1/docs/modules/metal_device.md)|Create, update, or delete Equinix Metal devices|
[equinix.cloud.metal_ip_assignment](https://github.com/equinix-labs/ansible-collection-equinix/blob/0.0.1/docs/modules/metal_ip_assignment.md)|Asign reserved IPs to Equinix Metal devices.|
[equinix.cloud.metal_project](https://github.com/equinix-labs/ansible-collection-equinix/blob/0.0.1/docs/modules/metal_project.md)|Manage Projects in Equinix Metal. You can use *id* or *name* to lookup a project. If you want to create new project, you must provide *name*.|
[equinix.cloud.metal_reserved_ip_block](https://github.com/equinix-labs/ansible-collection-equinix/blob/0.0.1/docs/modules/metal_reserved_ip_block.md)|When a user provisions first device in a facility, Equinix Metal API automatically allocates IPv6/56 and private IPv4/25 blocks. The new device then gets IPv6 and private IPv4 addresses from those block. It also gets a public IPv4/31 address. Every new device in the project and facility will automatically get IPv6 and private IPv4 addresses from these pre-allocated blocks. The IPv6 and private IPv4 blocks can't be created, only imported. With this resource, it's possible to create either public IPv4 blocks or global IPv4 blocks.|


### Info Modules

Modules for retrieving information about existing equinix infrastructure.

Name | Description |
--- | ------------ |
[equinix.cloud.metal_available_ips_info](https://github.com/equinix-labs/ansible-collection-equinix/blob/0.0.1/docs/modules/metal_available_ips_info.md)|Get list of avialable IP addresses from a reserved IP block|
[equinix.cloud.metal_device_info](https://github.com/equinix-labs/ansible-collection-equinix/blob/0.0.1/docs/modules/metal_device_info.md)|Select list of Equinix Metal devices|
[equinix.cloud.metal_ip_assignment_info](https://github.com/equinix-labs/ansible-collection-equinix/blob/0.0.1/docs/modules/metal_ip_assignment_info.md)|Gather IP address assignments for a device|
[equinix.cloud.metal_project_info](https://github.com/equinix-labs/ansible-collection-equinix/blob/0.0.1/docs/modules/metal_project_info.md)|Gather information about Equinix Metal projects|
[equinix.cloud.metal_reserved_ip_block_info](https://github.com/equinix-labs/ansible-collection-equinix/blob/0.0.1/docs/modules/metal_reserved_ip_block_info.md)|Gather information about Equinix Metal projects|


### Inventory Plugins

Dynamically add equinix infrastructure to an Ansible inventory.

Name |
--- |
[equinix.cloud.metal_device](https://github.com/equinix-labs/ansible-collection-equinix/blob/0.0.1/docs/inventory/metal_device.md)|


<!--end collection content-->

## Installation

You can install the equinix collection with the Ansible Galaxy CLI:

```shell
ansible-galaxy collection install equinix.cloud
```

The Python module dependencies are not installed by `ansible-galaxy`.  They can
be manually installed using pip:

```shell
pip install -r https://raw.githubusercontent.com/equinix-labs/ansible-collection-equinix/0.0.1/requirements.txt
```

## Usage
Once the equinix Ansible collection is installed, it can be referenced by its [Fully Qualified Collection Namespace (FQCN)](https://github.com/ansible-collections/overview#terminology): `equinix.cloud.module_name`.

In order to use this collection, you should have account in the relevant Equinix service. For example you should have an account Equinix Metal to use the `metal_*` plugins.

You can authenticate either by exporting auth tokens as environment variables, or by supplying `*_api_token` attributes to modules. For example, to use `metal_device`, you can export `METAL_AUTH_TOKEN` (or `METAL_API_TOKEN`), or you can supply `metal_auth_token` attribute.

#### Example Playbook
```yaml
---
- name: create Equinix Metal device
  hosts: localhost
  tasks:
    - equinix.cloud.instance:
        project_id: "3b516842-c8b1-485e-9f76-c891bd804c5e"
        hostname: "my new device"
        operating_system: ubuntu_20_04
        plan: c3.small.x86
        metro: sv
```

For more information on Ansible collection usage, see [Ansible's official usage guide](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html).

## Examples

Use-case examples for this collection can be found [here](./examples/README.md).

## Licensing

GNU General Public License v3.0.

See [COPYING](COPYING) to see the full text.