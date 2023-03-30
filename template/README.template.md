# Equinix Ansible Collection
[![Ansible Galaxy](https://img.shields.io/badge/galaxy-equinix.cloud-660198.svg?style=flat)](https://galaxy.ansible.com/equinix/cloud/) 
![Tests](https://img.shields.io/github/actions/workflow/status/equinix-labs/ansible-collection-equinix/integration-tests.yml?branch=main)

The Ansible Collection Equinix contains various plugins for managing Equinix services.

<!--start requires_ansible-->
## Ansible version compatibility

This collection has been tested against following Ansible version **6.7.0**, core version **2.13.8**.

Plugins and modules within a collection may be tested with only specific Ansible versions.
A collection may contain metadata that identifies these versions.
PEP440 is the schema used to describe the versions of Ansible.
<!--end requires_ansible-->

<!--start collection content-->
### Modules

Modules for managing Equinix infrastructure.

Name | Description |
--- | ------------ |
{% for mod in modules %}[equinix.cloud.{{ mod.name }}]({% if is_release %}https://github.com/equinix-labs/ansible-collection-equinix/blob/{{ collection_version }}/docs/modules/{{ mod.name }}.md{% else %}./docs/modules/{{ mod.name }}.md{% endif %})|{{ mod.description }}|
{% endfor %}

### Info Modules

Modules for retrieving information about existing Equinix infrastructure.

Name | Description |
--- | ------------ |
{% for mod in info_modules %}[equinix.cloud.{{ mod.name }}]({% if is_release %}https://github.com/equinix-labs/ansible-collection-equinix/blob/{{ collection_version }}/docs/modules/{{ mod.name }}.md{% else %}./docs/modules/{{ mod.name }}.md{% endif %})|{{ mod.description }}|
{% endfor %}

### Inventory Plugins

Dynamically add Equinix infrastructure to an Ansible inventory.

Name |
--- |
{% for name in inventory %}[equinix.cloud.{{ name }}]({% if is_release %}https://github.com/equinix-labs/ansible-collection-equinix/blob/{{ collection_version }}/docs/inventory/{{ name }}.md{% else %}./docs/inventory/{{ name }}.md{% endif %})|
{% endfor %}

<!--end collection content-->

## Installation

You can install the Equinix collection with the Ansible Galaxy CLI:

```shell
ansible-galaxy collection install equinix.cloud
```

The Python module dependencies are not installed by `ansible-galaxy`.  They can
be manually installed using pip:

```shell
pip install -r https://raw.githubusercontent.com/equinix-labs/ansible-collection-equinix/{{collection_version}}/requirements.txt
```

## Usage
Once the Equinix Ansible collection is installed, it can be referenced by its [Fully Qualified Collection Namespace (FQCN)](https://github.com/ansible-collections/overview#terminology): `equinix.cloud.module_name`.

In order to use this collection, you should have account in the relevant Equinix service. For example you should have an account Equinix Metal to use the `metal_*` plugins.

You can authenticate either by exporting auth tokens as environment variables, or by supplying `*_api_token` attributes to modules. For example, to use `metal_device`, you can export `METAL_AUTH_TOKEN` (or `METAL_API_TOKEN`), or you can supply `metal_auth_token` attribute.

#### Example Playbook
```yaml
---
- name: create Equinix Metal device
  hosts: localhost
  tasks:
    - equinix.cloud.metal_device:
        project_id: "3b516842-c8b1-485e-9f76-c891bd804c5e"
        hostname: "my new device"
        operating_system: ubuntu_20_04
        plan: c3.small.x86
        metro: sv
```

For more information on Ansible collection usage, see [Ansible's official usage guide](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html).

## Examples

Use-case examples for this collection can be found [here](./examples).

## Licensing

GNU General Public License v3.0.

See [COPYING](COPYING) to see the full text.
