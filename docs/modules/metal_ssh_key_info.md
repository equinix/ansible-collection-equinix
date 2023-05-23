# metal_ssh_key_info

Gather personal SSH keys. Read more about personal vs project SSH keys in [Equinix Metal documentation](https://metal.equinix.com/developers/docs/accounts/ssh-keys/#personal-keys-vs-project-keys).


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml

- set_fact:
    desired_name_substring: "tkarasek"
    
- name: list ssh_keys
  equinix.cloud.metal_ssh_key_info:
  register: ssh_keys_listed

- name: filter found ssh keys
  set_fact:
    both_ssh_keys_listed: "{{ ssh_keys_listed.resources | selectattr('label', 'match', desired_name_substring) }}"

```










## Return Values

- `resources` - Found resources

    - Sample Response:
        ```json
        
        [
            {
                "fingerprint": "70:c1:73:8b:3f:2f:a4:18:ea:4d:79:13:52:7b:c4:3e",
                "id": "6edfcbc2-17e5-4221-9eac-2f40dbe60daf",
                "key": "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAt5gwVMhwcCrxyxpMEKwiS0xgit3PIIEgVXt6SQHc8eONq0mYJJ5TOBNTnySqXd9RtSv/Jbf5Aq9BzBGWeoZ6sZfKwh984Ip35StJtjXtyIOlY3skovndtupBIwlGXgX/WQzyLr+G/+Yu9/nhdxQi801PDZnDvKoeomM0rMD29nV+m0ud+GrtsAt6VFul2PxqpypZ1TYviyED6IKo7rgQsQDkE9QHcNdfT1FZWiJbfP7o8TIurQJcAXg+MtLoc8rKKcxFMeZ9FSydgtTC7nP1h558RtECGWiUgaBPI7TpBmcdMtbEfAiBoGT17GWnT8qmy2u5xnEKPD9Qft4w4fjfpw==",
                "label": "tkarasek"
            },
            {
                "fingerprint": "ba:70:af:b3:0f:0e:7f:e5:eb:97:e2:27:b1:f5:6f:94",
                "id": "d00c596d-b42a-44a7-ac14-e299b85e73d3",
                "key": "ssh-dss AAAAB3NzaC1kc3MAAACBAOpXVtmc0Bla98bt0o5/Zj7sb4mHIukgVFZu7F32R3VK1cEKB4rEE8uS0oLS/qMRLue45TWVJwRMYGlPjt3p/VyraelxoyJZLuITIsqa5hBc9w0oTlB5Bmbkn16umW96WCaWEoq/aitpocbRChTiP5biI6FyQTQlIHDaYzBDOi11AAAAFQDUXy7cmuzphDpJSYYTiudiUhVokwAAAIEAyUQ9m8qL/1HPkFe6jbXAvtSSmW27F4c+G2xR5HizaHQzXgBOxPcsOsY17KTU+Ddbg+OF9soWNwSpm9pyVjVmNGqH3S8R1pwvuJF/O2Asy1m6wpWhbPw8JdEBW7WHoptBpfuzJoS2LOzJUEmUu4Eb+xS237KG1d1BVny/49KAoH0AAACBAJKBSsm9Xey0fUN6vYtTQgoYeGxxj/LqAIAOs/TpCxZDntly860y/SzHYai8x48k4t7whENY1CJ41fpMcPlz8xIsrNP3326Wbr0ExwOIvJKAVN1YLYqF8NXWzaVrjo5WbSeI8PiWTYemvLAujVxZssIrApTZBhp55nnwge6K1zTG tomk@air",
                "label": "ansible-integration-test-ssh_key-ztiapihf-ssh_key1_renamed"
            }
        ]
        
        ```


