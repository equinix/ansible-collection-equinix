# metal_device_list

Select list of Equinix Metal devices


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Gather information about all devices
  hosts: localhost
  tasks:
      - equinix.metal.device_list:

```

```yaml
- name: Gather information about devices in a particular project using ID
  hosts: localhost
  tasks:
      - equinix.metal.device_list:
            project_id: 173d7f11-f7b9-433e-ac40-f1571a38037a

```

```yaml
- name: Gather information about devices in a particular organization using ID
  hosts: localhost
  tasks:
      - equinix.metal.device_list:
            organization_id: 173d7f11-f7b9-433e-ac40-f1571a38037a

```

```yaml
- name: Gather information about devices with "webserver" in hostname in a project
  hosts: localhost
  tasks:
      - equinix.metal.device_list:
            project_id: 173d7f11-f7b9-433e-ac40-f1571a38037a
            hostname: webserver

```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `hostname` | <center>`str`</center> | <center>Optional</center> | Hostname to look up a device.   |
| `project_id` | <center>`str`</center> | <center>Optional</center> | UUID of the project containing devices.   |
| `organization_id` | <center>`str`</center> | <center>Optional</center> | UUID of the organization containing devices.   |






## Return Values

- `resources` - List of devices

    - Sample Response:
        ```json
        
        [
            {
                "always_pxe": false,
                "billing_cycle": "hourly",
                "customdata": {},
                "facility": "sv15",
                "hardware_reservation_id": "",
                "hostname": "ansible-integration-test-device-yi4fbuo4-dev2",
                "id": "6dee3ce4-72f4-4d92-a035-dff5237b2841",
                "ip_addresses": [
                    {
                        "address": "147.75.71.193",
                        "address_family": 4,
                        "public": true
                    },
                    {
                        "address": "2604:1380:45e3:2c00::3",
                        "address_family": 6,
                        "public": true
                    },
                    {
                        "address": "10.67.168.18",
                        "address_family": 4,
                        "public": false
                    }
                ],
                "ipxe_script_url": "",
                "locked": false,
                "metal_state": "active",
                "metro": "sv",
                "operating_system": "ubuntu_20_04",
                "plan": "c3.small.x86",
                "project_id": "6ac17ea6-a304-4b01-a1f3-f13a7371cfab",
                "spot_instance": false,
                "spot_price_max": 0.0,
                "ssh_keys": [
                    {
                        "href": "/metal/v1/ssh-keys/1ffe4e4b-eaf9-45d9-a268-0d81af71ae55",
                        "id": "1ffe4e4b-eaf9-45d9-a268-0d81af71ae55"
                    },
                    {
                        "href": "/metal/v1/ssh-keys/d122d4e4-4832-41c8-abbb-40182930becf",
                        "id": "d122d4e4-4832-41c8-abbb-40182930becf"
                    },
                    {
                        "href": "/metal/v1/ssh-keys/b0f196c0-9cf2-4cb7-96c5-403b81ff6813",
                        "id": "b0f196c0-9cf2-4cb7-96c5-403b81ff6813"
                    },
                    {
                        "href": "/metal/v1/ssh-keys/4b011c75-e642-4f6d-85f4-590a5956ad28",
                        "id": "4b011c75-e642-4f6d-85f4-590a5956ad28"
                    },
                    {
                        "href": "/metal/v1/ssh-keys/217ff08c-057a-4933-8efe-2e9f723fbb5f",
                        "id": "217ff08c-057a-4933-8efe-2e9f723fbb5f"
                    },
                    {
                        "href": "/metal/v1/ssh-keys/10968e80-b234-469b-acb8-c5002b4111a4",
                        "id": "10968e80-b234-469b-acb8-c5002b4111a4"
                    },
                    {
                        "href": "/metal/v1/ssh-keys/6ff0810b-135c-48cf-ac68-b365bdfd338c",
                        "id": "6ff0810b-135c-48cf-ac68-b365bdfd338c"
                    },
                    {
                        "href": "/metal/v1/ssh-keys/6a71d7e1-db14-4dfd-9014-46032b507538",
                        "id": "6a71d7e1-db14-4dfd-9014-46032b507538"
                    },
                    {
                        "href": "/metal/v1/ssh-keys/413e2347-f89c-40af-ba9e-0864f2fde990",
                        "id": "413e2347-f89c-40af-ba9e-0864f2fde990"
                    },
                    {
                        "href": "/metal/v1/ssh-keys/9308b337-702a-4774-8351-37dfb8c90a57",
                        "id": "9308b337-702a-4774-8351-37dfb8c90a57"
                    }
                ],
                "tags": [],
                "userdata": ""
            },
            {
                "always_pxe": false,
                "billing_cycle": "hourly",
                "customdata": {},
                "facility": "sv15",
                "hardware_reservation_id": "",
                "hostname": "ansible-integration-test-device-yi4fbuo4-dev1",
                "id": "71a90c54-e0eb-414f-9ea2-9c39ecb32319",
                "ip_addresses": [
                    {
                        "address": "139.178.94.207",
                        "address_family": 4,
                        "public": true
                    },
                    {
                        "address": "2604:1380:45e3:2c00::1",
                        "address_family": 6,
                        "public": true
                    },
                    {
                        "address": "10.67.168.2",
                        "address_family": 4,
                        "public": false
                    }
                ],
                "ipxe_script_url": "",
                "locked": false,
                "metal_state": "active",
                "metro": "sv",
                "operating_system": "ubuntu_20_04",
                "plan": "c3.small.x86",
                "project_id": "6ac17ea6-a304-4b01-a1f3-f13a7371cfab",
                "spot_instance": false,
                "spot_price_max": 0.0,
                "ssh_keys": [
                    {
                        "href": "/metal/v1/ssh-keys/1ffe4e4b-eaf9-45d9-a268-0d81af71ae55",
                        "id": "1ffe4e4b-eaf9-45d9-a268-0d81af71ae55"
                    },
                    {
                        "href": "/metal/v1/ssh-keys/d122d4e4-4832-41c8-abbb-40182930becf",
                        "id": "d122d4e4-4832-41c8-abbb-40182930becf"
                    },
                    {
                        "href": "/metal/v1/ssh-keys/b0f196c0-9cf2-4cb7-96c5-403b81ff6813",
                        "id": "b0f196c0-9cf2-4cb7-96c5-403b81ff6813"
                    },
                    {
                        "href": "/metal/v1/ssh-keys/4b011c75-e642-4f6d-85f4-590a5956ad28",
                        "id": "4b011c75-e642-4f6d-85f4-590a5956ad28"
                    },
                    {
                        "href": "/metal/v1/ssh-keys/217ff08c-057a-4933-8efe-2e9f723fbb5f",
                        "id": "217ff08c-057a-4933-8efe-2e9f723fbb5f"
                    },
                    {
                        "href": "/metal/v1/ssh-keys/10968e80-b234-469b-acb8-c5002b4111a4",
                        "id": "10968e80-b234-469b-acb8-c5002b4111a4"
                    },
                    {
                        "href": "/metal/v1/ssh-keys/6ff0810b-135c-48cf-ac68-b365bdfd338c",
                        "id": "6ff0810b-135c-48cf-ac68-b365bdfd338c"
                    },
                    {
                        "href": "/metal/v1/ssh-keys/6a71d7e1-db14-4dfd-9014-46032b507538",
                        "id": "6a71d7e1-db14-4dfd-9014-46032b507538"
                    },
                    {
                        "href": "/metal/v1/ssh-keys/413e2347-f89c-40af-ba9e-0864f2fde990",
                        "id": "413e2347-f89c-40af-ba9e-0864f2fde990"
                    },
                    {
                        "href": "/metal/v1/ssh-keys/9308b337-702a-4774-8351-37dfb8c90a57",
                        "id": "9308b337-702a-4774-8351-37dfb8c90a57"
                    }
                ],
                "tags": [],
                "userdata": ""
            }
        ]
        
        ```


