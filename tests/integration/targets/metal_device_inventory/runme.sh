#!/usr/bin/env bash

set -eux

cleanup() {
    ansible-playbook playbooks/teardown.yml "$@"
}
trap cleanup EXIT

# Create testing device
ansible-playbook -vvv playbooks/setup_metal_device.yml "$@"

# Test an inventory with no filter
ansible-playbook playbooks/create_inventory.yml --extra-vars "template=nofilter.metal_device.yml" "$@"
ANSIBLE_INVENTORY=nofilter.metal_device.yml ansible-playbook playbooks/test_inventory_nofilter.yml "$@"

# Test an inventory with a filter
ansible-playbook playbooks/create_inventory.yml --extra-vars "template=filter.metal_device.yml" "$@"
ANSIBLE_INVENTORY=filter.metal_device.yml ansible-playbook playbooks/test_inventory_filter.yml "$@"

# Test an inventory with keyed groups filter
ansible-playbook playbooks/create_inventory.yml --extra-vars "template=keyedgroups.metal_device.yml" "$@"
ANSIBLE_INVENTORY=keyedgroups.metal_device.yml ansible-playbook playbooks/test_inventory_keyedgroups.yml "$@"
