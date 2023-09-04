# metal_operating_system_info

Gather information about Operating Systems available in Equinix Metal


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Select all operating_systems and filter Ubuntu-based distros
  hosts: localhost
  tasks:
    - name: Select all operating_systems
      equinix.cloud.metal_operating_system_info:
      register: operating_systems

    - name: Store Ubuntu operating_systems to fact uoss
      set_fact:
        uoss: "{{ operating_systems.resources | selectattr('distro', 'equalto', 'ubuntu') | list }}"

```










## Return Values

- `resources` - Found Operating Systems

    - Sample Response:
        ```json
        
        [
            {
                "distro": "windows",
                "distro_label": "Windows",
                "id": "897c6a00-4fb7-4bc6-80db-83478e1ce1ba",
                "licensed": true,
                "name": "Windows 2019 Standard",
                "preinstallable": false,
                "pricing": {
                    "hour": {
                        "multiplier": "cores",
                        "price": 0.01
                    }
                },
                "provisionable_on": [
                    "c2.medium.x86",
                    "c3.medium.opt-c1",
                ],
                "slug": "windows_2019",
                "version": "2019"
            },
            {
                "distro": "windows",
                "distro_label": "Windows",
                "id": "fefd6fa7-6f6e-46eb-918b-6839f5ca59cf",
                "licensed": true,
                "name": "Windows 2022 Standard",
                "preinstallable": false,
                "pricing": {
                    "hour": {
                        "multiplier": "cores",
                        "price": 0.01
                    }
                },
                "provisionable_on": [
                    "c2.medium.x86",
                    "c3.medium.opt-c1",
                ],
                "slug": "windows_2022",
                "version": "2022"
            }
        ]
        ```


