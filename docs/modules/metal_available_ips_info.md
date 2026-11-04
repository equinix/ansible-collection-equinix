# metal_available_ips_info

Get list of avialable IP addresses from a reserved IP block

> [!WARNING]
> **Deprecated:** Equinix Metal reached end of life on June 30, 2026. This module will be removed in version 1.0.0. Alternative: None. Equinix Metal has reached end of life, see https://docs.equinix.com/metal/

- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
name: available addresses from reservation
equinix.cloud.metal_available_ips_info:
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



### Sample Response for available
```json
{
  "available": [
    "147.75.71.192/32"
  ]
}
```


