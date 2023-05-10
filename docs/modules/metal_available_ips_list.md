# metal_available_ips_list

Get list of avialable IP addresses from a reserved IP block


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
name: available addresses from reservation
equinix.cloud.metal_available_ips_list:
  reserved_ip_block_id: "{{ ip_reservation.id }}"
  cidr: 32
  register: available_ips

```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `reserved_ip_block_id` | <center>`str`</center> | <center>**Required**</center> | UUID of the reserved IP block to list available IPs for.   |
| `cidr` | <center>`str`</center> | <center>Optional</center> | CIDR of the reserved IP block to list available IPs for.   |






## Return Values

- `available` - Available IP addresses from the reservation.

    - Sample Response:
        ```json
        
        {
            "available": [
                "147.75.71.192/32"
            ],
        }
        
        ```


