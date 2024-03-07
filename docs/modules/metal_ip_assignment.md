# metal_ip_assignment

Asign reserved IPs to Equinix Metal devices.


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
    - name: request ip reservation
      equinix.cloud.metal_reserved_ip_block:
        type: "public_ipv4"
        metro: "sv"
        quantity: 1
        project_id: "{{ project.id }}"
      register: ip_reservation

    - name: available addresses from reservation
      equinix.cloud.metal_available_ips_info:
        reserved_ip_block_id: "{{ ip_reservation.id }}"
        cidr: 32
      register: available_ips
    
    - assert:
        that:
          - "available_ips.available | length == 1"  


    - name: create device
      equinix.cloud.metal_device:
        project_id: "{{ project.id }}"
        hostname: "device1"
        operating_system: ubuntu_20_04
        plan: c3.small.x86
        metro: sv
        state: present
      register: device

    - name: assign available IP
      equinix.cloud.metal_ip_assignment:
        device_id: "{{ device.id }}"
        address: "{{ available_ips.available[0] }}"
      register: assignment

```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `id` | <center>`str`</center> | <center>Optional</center> | UUID of the ip_assignment.   |
| `device_id` | <center>`str`</center> | <center>Optional</center> | UUID of the device to assign the IP to.   |
| `address` | <center>`str`</center> | <center>Optional</center> | IP address to assign to the device.   |
| `customdata` | <center>`dict`</center> | <center>Optional</center> | Custom data about the ip_assignment to create.   |
| `manageable` | <center>`bool`</center> | <center>Optional</center> | Whether the IP address is manageable.   |






## Return Values



### Sample Response for metal_ip_assignment
```json
{
  "address": "147.75.71.192/32",
  "address_family": 4,
  "changed": true,
  "cidr": 32,
  "device_id": "a8c5dd81-9f7a-4c70-81c6-a168782931ab",
  "id": "83b5503c-7b7f-4883-9509-b6b728b41491",
  "management": false,
  "metro": "sv",
  "netmask": "255.255.255.255",
  "network": "147.75.71.192",
  "public": true
}
```


