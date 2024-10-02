# Metal Device network types

This example playbook demonstrates the use of the `equinix.cloud.metal_port` modules to configure various [network types](https://deploy.equinix.com/developers/docs/metal/layer2-networking/overview/#network-configuration-types) for an Equinix Metal device. The playbook is available on GitHub at https://github.com/equinix/ansible-collection-equinix/tree/examples/device_network_types.

## Overview

The [playbook](main.yml) creates a new project, creates 2 VLANs, provisions a device, and configures the device through different [network types](https://deploy.equinix.com/developers/docs/metal/layer2-networking/overview/#network-configuration-types).


## Prerequisites

Before running the playbook, you will need to have the following:

- Ansible installed on your local machine.
- The Equinix Ansible Collection installed. You can install it using the following command:
  ```bash
  ansible-galaxy collection install equinix.cloud
  ```
- An Equinix Metal API token. You can obtain an API token from the Equinix Metal Portal. Set the environment variable METAL_AUTH_TOKEN to your API token:
  ```bash
  export METAL_AUTH_TOKEN=your_api_token_here
  ```

## Variables

You can customize some variables from [vars/equinix_metal_vars.yml](vars/equinix_metal_vars.yml).

## Running the Playbook

To run the playbook, navigate to the directory containing the playbook file `main.yml` and run the following command:

```bash
ansible-playbook main.yml
```

## What does the Playbook do?

### Accessing port IDs

To configure a Metal port, you must specify the port ID.  These IDs can be obtained from the output of a `metal_device` module (registered as `device` in this example) as follows:

```yaml
- name: capture port ids for device
  set_fact:
    bond_port_id: "{{ device.network_ports | selectattr('name', 'match', 'bond0') | map(attribute='id') | first }}"
    eth1_port_id: "{{ device.network_ports | selectattr('name', 'match', 'eth1') | map(attribute='id') | first }}"
```

### Layer 3 mode

Layer 3 (Bonded) is the default port configuration on Equinix Metal devices. The following is provided to illustrate the usage of the `metal_port` module. This task configuration should not be needed in practice, however it may be useful in some configurations to assert the correct mode is set.

```yaml
- name: convert bond port to layer3 bonded mode
  equinix.cloud.metal_port:
    id: "{{ bond_port_id }}"
    bonded: true
    layer2: false
```

### Layer 2 unbonded mode

This example configures an Equinix Metal server with a [pure layer 2 unbonded](https://deploy.equinix.com/developers/docs/metal/layer2-networking/layer2-mode/#:~:text=Layer%202%20Unbonded%20Mode) network configuration and adds two VLANs to its `eth1` port; one of them set as the [native VLAN](https://deploy.equinix.com/developers/docs/metal/layer2-networking/native-vlan/).

```yaml

- name: convert bond port to layer 2 unbonded mode
  equinix.cloud.metal_port:
    id: "{{ bond_port_id }}"
    bonded: false
    layer2: true

- name: attach VLANs to eth1 and assign native VLAN
  equinix.cloud.metal_port:
    id: "{{ eth1_port_id }}"
    bonded: false
    vlan_ids:
      - "{{ first_vlan.id }}"
      - "{{ second_vlan.id }}"
    native_vlan_id: "{{ first_vlan.id }}"
```

### Layer 2 bonded mode

```yaml
- name: convert bond port to layer 2 bonded mode
  equinix.cloud.metal_port:
    id: "{{ bond_port_id }}"
    bonded: true
    layer2: true
```

### Hybrid unbonded mode

```yaml
- name: convert eth1 port to hybrid unbonded mode
  equinix.cloud.metal_port:
    id: "{{ eth1_port_id }}"
    bonded: false
```

### Hybrid bonded mode

```yaml
- name: convert bond port to hybrid bonded mode
  equinix.cloud.metal_port:
    id: "{{ bond_port_id }}"
    bonded: true
    layer2: false
    vlan_ids:
      - "{{ first_vlan.id }}"
      - "{{ second_vlan.id }}"
```
