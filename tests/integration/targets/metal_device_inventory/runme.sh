#!/usr/bin/env bash

set -eux

unique_id=$(cat /dev/urandom | tr -dc 'a-z0-9' | fold -w 8 | head -n 1)

cleanup() {
    ansible-playbook playbooks/teardown.yml --extra-vars "unique_id=${unique_id}" "$@"
}
trap cleanup EXIT

# Create testing device
ansible-playbook -vvv playbooks/setup_metal_device.yml --extra-vars "unique_id=${unique_id}" "$@"

# Test an inventory with no filter
ansible-playbook playbooks/create_inventory.yml --extra-vars "template=nofilter.metal_device.yml" "$@"
# Wait for file copy to complete. This prevents playbook errors in GitHub Actions tests.
timeout 15 bash -c 'until [ -f "nofilter.metal_device.yml" ]; do sleep 1; done'
cat nofilter.metal_device.yml || true
ls -la .
ANSIBLE_INVENTORY=nofilter.metal_device.yml ansible-playbook playbooks/test_inventory_nofilter.yml "$@"

# Test an inventory with a filter
ansible-playbook playbooks/create_inventory.yml --extra-vars "template=filter.metal_device.yml" "$@"
timeout 15 bash -c 'until [ -f "filter.metal_device.yml" ]; do sleep 1; done'
ANSIBLE_INVENTORY=filter.metal_device.yml ansible-playbook playbooks/test_inventory_filter.yml "$@"

# Test an inventory with keyed groups filter
ansible-playbook playbooks/create_inventory.yml --extra-vars "template=keyedgroups.metal_device.yml" "$@"
timeout 15 bash -c 'until [ -f "keyedgroups.metal_device.yml" ]; do sleep 1; done'
ANSIBLE_INVENTORY=keyedgroups.metal_device.yml ansible-playbook playbooks/test_inventory_keyedgroups.yml "$@"
