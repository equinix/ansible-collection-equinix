# Layer 2 networking with Equinix Metal

This example demonstrates the use of the `equinix.cloud.metal_connection`, `equinix.cloud.metal_device`, and `equinix.cloud.metal_port` modules--as well as a variety of AWS modules--to configure Layer 2 connectivity from an Equinix Metal device to AWS S3 over a Metal-billed Fabric interconnection.

## Overview

The [pre-Fabric playbook](pre_fabric.yml) creates a new project, a VLAN, a VRF, a VRF Metal Gateway, and a device, converts the device to [hybrid bonded mode](https://deploy.equinix.com/developers/docs/metal/layer2-networking/overview/#network-configuration-types), and then creates a Metal-billed VRF interconnection and configures BGP peering settings on the interconnection's virtual circuit.

Manual intervention is needed in order to finish setting up the interconnection and accept the Direct Connect request in AWS.

The [post-Fabric playbook](post_fabric.yml) creates a new VPC, a VPC endpoint for S3, and a Virtual Private Gateway attached to the specified Direct Connect, and configures BGP peering between the Direct Connect and your Metal VRF.

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

To create the Equinix Metal infrastructure for this example, navigate to the directory containing the playbook file `pre_fabric.yml` and run the following command:

```bash
ansible-playbook pre_fabric.yml -extra-vars "bgp_md5_password=<some_value>"
```

*NOTE:* The API performs some validation on the md5 for BGP.  For the latest rules refer to [the VRF virtual circuit API docs](https://deploy.equinix.com/developers/api/metal/#tag/Interconnections/operation/updateVirtualCircuit). As of this writing, the md5:
* must be 10-20 characters long
* may not include punctuation
* must be a combination of numbers and letters
* must contain at least one lowercase, uppercase, and digit character

The last task in the `pre_fabric.yml` playbook will print out the service token for your Metal connection:

```bash
TASK [print service token to redeem in Fabric portal] **************************************************************************
ok: [localhost] => {
    "connection.service_tokens[0].id": "<service_token_id>"
}
```

After the Equinix Metal infrastructure is created, you will need to redeem the service token for your connection in the [Equinix portal](https://portal.equinix.com). Navigate to Fabric -> Connect to Provider, choose AWS, and finally AWS Direct Connect. Choose Primary, put in your account number, choose the metro, click next, then choose "Service Token" from the drop down, and put in the service token.  You will be prompted to name your connection; **take note of the name you use**, you will need it for the next playbook.

To finish setting up the AWS infrastructure, run the following command which will accept the direct connect request in AWS; wait for the connection to become active; create an AWS VPC, VPC endpoint, and VPN gateway; create a virtual interface connecting the VPC to your direct connect, and configure the Metal side of your interconnection to connect to the virtual interface in AWS:

```bash
ansible-playbook post_fabric.yml --extra-vars "bgp_md5_password=<some_value>" --extra-vars "aws_connection_name=<your_direct_connect_name>"
```

The last task in the `post_fabric.yml` playbook will print the DNS hostname for your S3 VPC endpoint:

```bash
TASK [print DNS name for VPC endpoint] *****************************************************************************************
ok: [localhost] => {
    "msg": "vpce-<some_id>.s3.us-west-1.vpce.amazonaws.com"
}
```



## Testing the VPC endpoint and interconnection

The DNS entry for your VPC endpoint is public, so you can look up the corresponding IP address from any Internet-connected computer.  You will see that it resolves to an IP address within your private VPC address space (the example below uses the default VPC CIDR for this module, `172.16.0.0/16`):

```bash
$ dig vpce-<some_id>.s3.us-west-1.vpce.amazonaws.com
# ...
;; ANSWER SECTION:
vpce-<some_id>.s3.us-west-1.vpce.amazonaws.com. 60 IN A 172.16.94.176
# ...
```

Since this address resolves to an IP within your VPC, though, you can only connect to it from an EC2 instance in your VPC or from the Metal device you deployed earlier.

SSH in to the Metal device that was created by the `pre_fabric.yml` playbook.

Install the AWS CLI:

```bash
$ apt install -y awscli
```

Configure your [AWS CLI credentials](https://docs.aws.amazon.com/cli/v1/userguide/cli-chap-authentication.html).  For example, if you want to store your credentials in environment variables, it will look something like this:

```bash
$ export AWS_ACCESS_KEY_ID=<some_aws_key_id>
$ export AWS_SECRET_ACCESS_KEY=<some_aws_access_key>
$ export AWS_DEFAULT_REGION=us-west-1
```

You can now use the AWS CLI with your VPC endpoint to interact with the S3 service by adding the `bucket.` prefix to your VPC endpoint hostname:

```bash
$ aws s3 ls --endpoint-url https://bucket.vpce-<some_id>.s3.us-west-1.vpce.amazonaws.com
2021-03-22 11:13:54 <some_bucket>
2021-03-22 11:13:54 <some_other_bucket>
...
```

You can learn about other usages of the S3 VPC endpoint with AWS CLI in [the AWS PrivateLink docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/privatelink-interface-endpoints.html).
