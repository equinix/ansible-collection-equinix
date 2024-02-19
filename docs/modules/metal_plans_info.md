# metal_plans_info

Gather information about Equinix Metal plans


- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Gather information about all plans
  hosts: localhost
  tasks:
      - equinix.cloud.metal_plans_info

```

```yaml
- name: Gather information for plans starting with c3.medium
  hosts: localhost
  tasks:
      - equinix.cloud.metal_plans_info:
          slug: c3.medium

```










## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `category` | <center>`list`</center> | <center>Optional</center> | Filter plans by its category.   |
| `type` | <center>`str`</center> | <center>Optional</center> | Filter plans by its plan type.   |
| `slug` | <center>`str`</center> | <center>Optional</center> | Filter plans by slug.   |
| `include` | <center>`list`</center> | <center>Optional</center> | Nested attributes to include. Included objects will return their full attributes. Attribute names can be dotted (up to 3 levels) to included deeply nested objects.   |
| `exclude` | <center>`list`</center> | <center>Optional</center> | Nested attributes to exclude. Excluded objects will return only the href attribute. Attribute names can be dotted (up to 3 levels) to exclude deeply nested objects.   |






## Return Values

- `resources` - Found resources

    - Sample Response:
        ```json
        
        
        [  
          {                                                                           
            "changed": false,                                                                         
            "resources": [                                                                                                                                                    
              {                                                                                     
                "available_in": [],                                                                                                                                                       
                "available_in_metros": [],
                "category": [
                  "compute",
                  "current_gen"
                ],
                "class": "a3.large.opt-m3a2",
                "deployment_types": [],
                "description": "a3.large.opt-m3a2.x86",
                "id": "8c04950a-87ab-5e52-a112-5a90bbca8868",
                "legacy": false,
                "line": "baremetal",
                "name": "a3.large.opt-m3a2.x86",
                "pricing_hour": 8.2,
                "pricing_month": null,
                "slug": "a3.large.opt-m3a2"
              },
            ]
          }
        ]
        ```


