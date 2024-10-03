# Layer 2 networking with Equinix Metal

This example playbook demonstrates the use of the `equinix.cloud.metal_connection`, `equinix.cloud.metal_device`, and `equinix.cloud.metal_port` modules to configure Layer 2 connectivity from an Equinix Metal device to an AWS S3 bucket over a Metal-billed Fabric interconnection.

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
ansible-playbook main.yml -extra-vars "bgp_md5_password=<some_value>"
```
