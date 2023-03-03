# Equinix Ansible Collection
[![Ansible Galaxy](https://img.shields.io/badge/galaxy-equinix.cloud-660198.svg?style=flat)](https://galaxy.ansible.com/equinix-labs/cloud/) 
![Tests](https://img.shields.io/github/actions/workflow/status/equinix-labs/ansible-collection-equinix/integration-tests.yml?branch=main)

The Ansible equinix Collection contains various plugins for managing equinix services.

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
{% for mod in modules %}[equinix.cloud.{{ mod.name }}]({% if is_release %}https://github.com/equinix-labs/ansible-collection-equinix/blob/{{ collection_version }}/docs/modules/{{ mod.name }}.md{% else %}./docs/modules/{{ mod.name }}.md{% endif %})|{{ mod.description }}|
{% endfor %}

### Info Modules

Modules for retrieving information about existing equinix infrastructure.

Name | Description |
--- | ------------ |
{% for mod in info_modules %}[equinix.cloud.{{ mod.name }}]({% if is_release %}https://github.com/equinix-labs/ansible-collection-equinix/blob/{{ collection_version }}/docs/modules/{{ mod.name }}.md{% else %}./docs/modules/{{ mod.name }}.md{% endif %})|{{ mod.description }}|
{% endfor %}

### List Modules

Modules for retrieving and filtering on multiple equinix resources.

Name | Description |
--- | ------------ |
{% for mod in list_modules %}[equinix.cloud.{{ mod.name }}]({% if is_release %}https://github.com/equinix-labs/ansible-collection-equinix/blob/{{ collection_version }}/docs/modules/{{ mod.name }}.md{% else %}./docs/modules/{{ mod.name }}.md{% endif %})|{{ mod.description }}|
{% endfor %}

### Inventory Plugins

Dynamically add equinix infrastructure to an Ansible inventory.

Name |
--- |
{% for name in inventory %}[equinix.cloud.{{ name }}]({% if is_release %}https://github.com/equinix-labs/ansible-collection-equinix/blob/{{ collection_version }}/docs/inventory/{{ name }}.md{% else %}./docs/inventory/{{ name }}.rst{% endif %})|
{% endfor %}

<!--end collection content-->

## Installation

You can install the equinix collection with the Ansible Galaxy CLI:

```shell
ansible-galaxy collection install equinix.cloud
```

The Python module dependencies are not installed by `ansible-galaxy`.  They can
be manually installed using pip:

```shell
pip install -r https://raw.githubusercontent.com/equinix-labs/ansible-collection-equinix/{{collection_version}}/requirements.txt
```

## Usage
Once the equinix Ansible collection is installed, it can be referenced by its [Fully Qualified Collection Namespace (FQCN)](https://github.com/ansible-collections/overview#terminology): `equinix.cloud.module_name`.

In order to use this collection, the `equinix_API_TOKEN` environment variable must be set to a valid equinix API v4 token. 
Alternatively, you can pass your equinix API v4 token into the `api_token` option for each equinix module you reference.

The `equinix_UA_PREFIX` or the `ua_prefix` module option can be used to specify a custom User-Agent prefix.

#### Example Playbook
```yaml
---
- name: create equinix instance
  hosts: localhost
  tasks:
    - name: Create a equinix instance    
      equinix.cloud.instance:
        label: my-equinix
        type: g6-nanode-1
        region: us-east
        image: equinix/ubuntu20.04
        root_pass: verysecurepassword!!!
        state: present
```

For more information on Ansible collection usage, see [Ansible's official usage guide](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html).

## Examples

Use-case examples for this collection can be found [here](./examples/README.md).

## Licensing

GNU General Public License v3.0.

See [COPYING](COPYING) to see the full text.
