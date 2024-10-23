# Layer 2 networking with Equinix Metal

This example demonstrates the use of the `equinix.cloud.metal_connection`, `equinix.cloud.metal_device`, and `equinix.cloud.metal_port` modules--as well as a variety of AWS modules--to configure Layer 2 connectivity from an Equinix Metal device to AWS S3 over a Metal-billed Fabric interconnection.

## Overview

The [Metal playbook](metal.yml) creates a new project, a VLAN, a VRF, a VRF Metal Gateway, and a device, converts the device to [hybrid bonded mode](https://deploy.equinix.com/developers/docs/metal/layer2-networking/overview/#network-configuration-types), and then creates a Metal-billed VRF interconnection and configures BGP peering settings on the interconnection's virtual circuit.

Manual intervention is needed in order to finish setting up the interconnection and accept the Direct Connect request in AWS.

The [AWS playbook](aws.yml) creates a new VPC, a VPC endpoint for S3, and a Virtual Private Gateway attached to the specified Direct Connect.

## Prerequisites

Before running the playbook, you will need to have the following:

- [Ansible installed on your local machine.](https://docs.ansible.com/ansible/latest/installation_guide/installation_distros.html)
- The Community.Aws, and Equinix Ansible Collections installed. You can install them using the following commands:
  ```bash
  ansible-galaxy collection install equinix.cloud
  ansible-galaxy collection install community.aws
  ```
- You will also need to ensure that the necessary Python libraries are installed:
  ```bash
  # Install Equinix Ansible collection dependencies
  pip install -r https://raw.githubusercontent.com/equinix/ansible-collection-equinix/v0.11.1/requirements.txt
  # Install AWS collection and Ansible IP function dependencies
  pip install boto3 netaddr
  ```
- An [Equinix Metal API token](https://deploy.equinix.com/developers/docs/metal/identity-access-management/api-keys/). You can obtain an API token from the Equinix Metal Portal. Set the environment variable METAL_AUTH_TOKEN to your API token:
  ```bash
  export METAL_AUTH_TOKEN=your_api_token_here
  ```

## Variables

You can customize some variables, such as Equinix Metal device hostname and IP ranges for Equinix Metal and AWS, from [vars/vars.yml](vars/vars.yml).

## Running the Playbooks

This example contains multiple playbooks and requires manual intervention between the playbooks.

To create the Equinix Metal infrastructure for this example, navigate to the directory containing the playbook file `metal.yml` and run the following command:

```bash
ansible-playbook metal.yml -extra-vars "bgp_md5_password=<some_value>"
```

*NOTE:* The API performs some validation on the md5 for BGP.  For the latest rules refer to [the VRF virtual circuit API docs](https://deploy.equinix.com/developers/api/metal/#tag/Interconnections/operation/updateVirtualCircuit). As of this writing, the md5:
* must be 10-20 characters long
* may not include punctuation
* must be a combination of numbers and letters
* must contain at least one lowercase, uppercase, and digit character

The last task in the `metal.yml` playbook will print out the service token for your Metal connection:

```bash
TASK [print service token to redeem in Fabric portal] **************************************************************************
ok: [localhost] => {
    "connection.service_tokens[0].id": "<service_token_id>"
}
```

After the Equinix Metal infrastructure is created, you will need to redeem the service token for your connection in the [Fabric portal](https://fabric.equinix.com).
After the Equinix Metal infrastructure is created, you will need to redeem the service token for your connection in the [Equinix portal](https://portal.equinix.com). Navigate to Fabric -> Connect to Provider, choose AWS, and finally AWS Direct Connect. Choose Primary, put in your account number, choose the metro, click next, then choose "Service Token" from the drop down, and put in the service token.

Once the service token is redeemed, you will need to accept the Direct Connect request in the [AWS console](https://console.aws.amazon.com). Take note of the Direct Connect ID and the Direct Connect VLAN when you accept the connection.  You will need the ID and VLAN for the next playbook.

To finish setting up the AWS infrastructure, wait for the connection to be available, then run the following command:

```bash
ansible-playbook aws.yml --extra-vars "bgp_md5_password=<some_value>" --extra-vars "aws_connection_id=<your_direct_connect_id>" --extra-vars "aws_connection_vlan=<your_direct_connect_vlan>"
```
