# IP Assignment to Metal Device

This example playbook demonstrates the use of `equinix.cloud.metal_*` modules to manage resources on Equinix Metal. The playbook is available on GitHub at https://github.com/equinix/ansible-collection-equinix/tree/examples/device_assign_ip.

## Overview

The [playbook](main.yml) creates a new project, reserves an IP block, provisions a device, and assigns an IP address from the reserved block to the device. It also demonstrates how to query information about the resources and clean up the resources after use.


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


