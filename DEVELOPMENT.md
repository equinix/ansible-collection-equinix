# Development Guide for the Collection

<!-- vscode-markdown-toc -->
* 0. [Development environment setup](#Developmentenvironmentsetup)
* 1. [Running integration tests](#Runningintegrationtests)
    * 1.1. [Debugging](#Debugging)
* 2. [Adding a new module](#Addinganewmodule)
	* 2.1. [Module structure](#Modulestructure)
	* 2.2. [Documentation and the Specdoc fields](#DocumentationandtheSpecdocfields)
	* 2.3. [main() function](#mainfunction)
	* 2.4. [API routes](#APIroutes)
	* 2.5. [Attribute maps in metal_api.py](#Attributemapsinmetal_api.py)
* 3. [_info modules](#infomodules)
* 4. [Generating documentation](#Generatingdocumentation)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->

##  0. <a name="Developmentenvironmentsetup"></a>Development environment setup

We use Python for collection development.  The Python version that is currently used in GitHub Actions workflows is tracked in the `.python-version` file in the root of this repository.  We recommend using the same Python version for local development.  Some tools, such as `pyenv`, may reference the `.python-version` file automatically, but in other cases you may have to manually install the specified Python version and add it to your path.

Development of the collection is best done if your repository is located in a path that concludes with `ansible_collections/equinix/cloud`. This is a requirement specific to Ansible. You can clone the repository using the following command:

```
git clone https://github.com/equinix/ansible-collection-equinix ansible_collections/equinix/cloud
```

You also need to export your METAL_AUTH_TOKEN in the environment variables:

```
export METAL_AUTH_TOKEN=<your_auth_token>
```


##  1. <a name='Runningintegrationtests'></a>Running integration tests

At the repository root, execute `make create-integration-config`. This generates a YAML config file in tests/integration/integration_config.yml with your auth token and other test configurations.

After that, you can run individual tests as, for example:
```
ansible-test integration -vvvv metal_project
ansible-test integration -vvvv metal_device
[...]
```

You can run all the tests with `make test`. You can also run the tests in parallel (like in the CI) with `make testall`. The parallel run is faster but it's harder to read the output.

### 1.1. <a name='Debugging'></a>Debugging

Since Ansible is supressing stdout, it's really hard to debug values of variables in module code.

Ansbile devs recommend [the "q" debugging library](https://github.com/zestyping/q) installed like `pip install -U q`, which is simple to use and logs to `/tmp/q`. For example:

(open `tail -f /tmp/q` in a terminal)

```python
import q; q(some_var)
```

Just make sure you remove all the "q" calls before merging to main.


##  2. <a name='Addinganewmodule'></a>Adding a new module

The primary task for this collection is the addition of new modules with the aim of achieving parity with the [Terraform Provider Equinix](https://github.com/equinix/terraform-provider-equinix). Each Terraform resource should have a corresponding module, and each needed datasource should have an accompanying `_info` module.

For instance, the [equinix_metal_device resource](https://registry.terraform.io/providers/equinix/equinix/latest/docs/resources/equinix_metal_device) in Terraform Provider corresponds to the [metal_device resource](https://github.com/equinix/ansible-collection-equinix/blob/main/docs/modules/metal_device.md) in this collection. In the same vein, the [equinix_metal_device datasource](https://registry.terraform.io/providers/equinix/equinix/latest/docs/data-sources/equinix_metal_device) correlates with the [metal_device_info module](https://github.com/equinix/ansible-collection-equinix/blob/main/docs/modules/metal_device_info.md) in our collection.

Issues have been created for every plausible existing Terraform resource and datasource within this repository. If you decide to work on a new module, please assign the corresponding issue to yourself.


###  2.1. <a name='Modulestructure'></a>Module structure

The basic template for a resoruce is outlined in [template/metal_resource.py](template/metal_resource.py). 

###  2.2. <a name='DocumentationandtheSpecdocfields'></a>Documentation and the Specdoc fields

Ansible module documentation requires three fields in the module script: DOCUMENTATION, EXAMPLES, and RETURN. A standardized method exists to generate Sphinx docs from these fields, resulting in a format like [this](https://docs.ansible.com/ansible/latest/collections/google/cloud/gcp_compute_disk_module.html#ansible-collections-google-cloud-gcp-compute-disk-module), which can then be incorporated into https://docs.ansible.com. 

However, this approach often leads to duplication between the documentation of module parameters and the initialization of the Ansible module object, as similar information is required for the module object constructor. 

To mitigate this redundancy and gain additional benefits, we utilize [ansible-specdoc](https://github.com/linode/ansible-specdoc/).

`ansible-specdoc` populates DOCUMENTATION, EXAMPLES and RETURN from [SPECDOC_META variable](https://github.com/linode/ansible-specdoc/#declaring-module-metadata) in Ansible module Python code. The fields are populated/injected from a Makefile task and we only need to initialize the 3 fields with empty strings:

```python
DOCUMENTATION = ""
EXAMPLES = ""
RETURN = ""
``` 

Our documentation efforts should primarily concentrate on the `SPECDOC_META` variable. This variable includes an `options` field where we can define the parameters of the Ansible module. These parameters are populated from the `module_spec` variable, a dictionary with parameter names as keys and SpecField objects as values.

For examples of SpecField usage in the collection, refer to existing modules. Additionally, the class definition is available in the [ansible-specdoc repository](https://github.com/linode/ansible-specdoc/).

SPECDOC_META has other parameters that are quite self-explanatory. Just note that the `examples` value, and the `sample` for SpecRetrunValue should both be lists.

The `return_values` should be formatted as a list of dictionaries. If the output of module called `metal_project` is
```json
changed: [testhost] => {
    "backend_transfer_enabled": false,
    "changed": true,
    "customdata": {},
    "description": "",
    "id": "e4a49767-824d-4b60-a55e-d66f4baaf7ea",
    "invocation": {},
    "name": "ansible-integration-test-project-j9sa85k8-project2",
    "organization_id": "4d12f460-8c5e-43ea-986d-529d328815ee",
    "payment_method_id": ""
}
```
.. define `return_values` in module script (in Python code) as

```python
return_values = [
  {
    "backend_transfer_enabled": False,
    "changed": True,
    "customdata": {},
    "description": "",
    "id": "e4a49767-824d-4b60-a55e-d66f4baaf7ea",
    "name": "ansible-integration-test-project-csle6t2y-project1_renamed",
    "organization_id": "70c2f878-9f32-452e-8c69-ab15480e1d99",
    "payment_method_id": "845b45a3-c565-47e5-b9b6-a86204a73d29"
  },
]

# .. and in SPECDOC_META:

SPECDOC_META = getSpecDocMeta(
    # ...
    return_values={
        "metal_project": SpecReturnValue(
            description='The module object',
            type=FieldType.dict,
            sample=return_values,
        ),
    },
)
```

All the samples will be rendered in markdown docs visible in the GitHub repo, only the first sample will be rendered in ansible-doc visible in Ansible Galaxy.


###  2.3. <a name='mainfunction'></a>main() function

The collection is structured to maintain consistency in the `main()` function across all modules. Modifications to the `main()` logic are only necessary for non-standard behavior. For instance, the `backend_transfer` attribute of the Project resource cannot be specified in the API call that creates a Project. As a result, we need to extend the `main()` function of the [metal_project module](https://github.com/equinix/ansible-collection-equinix/blob/10fca6a7e1ea06b86204fd301454ab9eff254ef5/plugins/modules/metal_project.py#L256) to accommodate this.

The module initialization leverages the parameter specification from SPECDOC_META.ansible_spec. This is where ansible-specdoc proves beneficial, as it eliminates the redundancy that would occur in the parameter specification documentation with standard Ansible use.

As implied by the code, a module initially attempts to locate a resource by its ID or name, with only one of `id` and `name` being specifiable. If precisely one such resource is identified and the desired state is `present`, its MUTABLE_ATTRIBUTES will be examined and updated as needed. If no matching resource is found and the desired state is `present`, the module will aim to create a new resource. The `absent` state is similarly handled in both scenarios. The `changed` flag is set accordingly. The exit JSON is formatted from the processed API response.

###  2.4. <a name='APIroutes'></a>API routes

Rather than directly calling the Equinix API, the module code invokes semantic actions such as get_by_id, get_one_from_list, update_by_id, delete_by_id, create, and list. The specific API calls for each module type (resource type) are defined in separate files, with [plugins/module_utils/metal/api_routes.py](plugins/module_utils/metal/api_routes.py) being the reference for the Metal API. 

The `get_routes()` function outlines specific API calls and their parameters for each (resource_type, action_type) pairing. If you're adding support for a new resource (i.e., creating a new module), you need to identify the relevant SDK functions and request classes from [equinix-sdk-python](https://github.com/equinix/equinix-sdk-python).

The specification looks like:

```python
    ('metal_device', action.CREATE): spec_types.Specs(
        equinix_metal.DevicesApi(mpc).create_device,
        {'id': 'project_id'},
        equinix_metal.CreateDeviceRequest,
    ),
```

This indicates that the "create" action for "metal_device" will invoke the `equinix_metal.DevicesApi(mpc).create_device` method from [equinix-sdk-python](https://github.com/equinix/equinix-sdk-python). The `project_id` argument will be mapped to the positional parameter `id`, while the remaining relevant module arguments will be used to populate an object of the `equinix_metal.CreateDeviceRequest` class, which will then be passed to the `create_device` method.

The arguments in spec_types.Specs constructor are

- client method for the resource action
- mapping of Ansible-module arguments to HTTP Path variables (or positional arguments in the client method)
- (optional) class for HTTP request body
- (optional) superclass for HTTP request body (see next subsection)

For example, method `create_device` is defined as:

```python
def create_device(
    self,
    id : Annotated[StrictStr, Field(..., description="ProjectUID")],
    create_device_request : Annotated  [CreateDeviceRequest,...],
    **kwargs,
) -> Device:
```

Having Ansible task specified as:

```yaml
    equinix.cloud.metal_device:
        hostname: my-device2
        operating_system: ubuntu_20_04
        project_id: 234db2b2-ee46-4673-93a8-de2c2bdba33b
        plan: c3.small.x86
        metro: sv
        state: present
```

The Specs object will ensure that when we call `module.create("metal_device")`, the `create_device` will be called as:

```python
create_device(
    "234db2b2-ee46-4673-93a8-de2c2bdba33b",
    equinix_metal.CreateDeviceRequest(
        hostname="my-device2",
        operating_system="ubuntu_20_04",
        plan="c3.small.x86",
        metro="sv",
    ),
)
```

Note that `project_id` isn't used in `CreateDeviceRequest` but as the first positional parameter `id` of `create_device`. This is due to the second parameter (mapping dict) of `spec_types.Specs`.

For API methods that don't require a positional parameter (no parent resource), like creating a project (HTTP POST to `/projects`), an empty dict should be passed as the mapping. Additionally, there are API methods that don't have a JSON body (such as getters or delete methods). In these cases, the third parameter to Specs should be left unspecified. Examples of all these scenarios can be found in [plugins/module_utils/metal/api_routes.py](plugins/module_utils/metal/api_routes.py).

#### 2.4.1 Superclass for HTTP request body of an API call

Sometimes it's not enough to specify only a class for request body. For example, there's only one API route to create dedicated interconnection, VLAN Fabric interconnection and VRF interconnection. In other words, all the connection types are created in the same API endpoint, and it's the request body json that distinguishes which type of interconnection should be created. The generated Python SDK then offers separate classes for the different types. For interconnection it's `DedicatedPortCreateInput`, `VlanFabricVcCreateInput`, `VrfFabricVcCreateInput`. However, we can't pass instances of these classes to the `InterconnectionsApi.create_project_interconnection`, we need to wrap it in an instance of `CreateOrganizationInterconnectionRequest`, created like 
```python
input = CreateOrganizationInterconnectionRequest(actual_instance=VrfFabricVcCreateInput())
```

That's why we had to add the fourth parameters of `spec_types.Specs`. The fourth parameter ("superclass") is a wrapping class for the input class (specified in the third parameters). It shouldn't be frequently needed.



###  2.5. <a name='Attributemapsinmetal_api.py'></a>Attribute maps in metal_api.py

We convert resources from the Equinix API response to Ansible modules, which allows us to query the API and identify attribute differences for updates. API responses can contain nested dictionaries, but Ansible modules tend to be more flat. As a result, we must explicitly map attributes from API responses to module parameters.

The attribute mappings for the Metal API are defined in [plugins/module_utils/metal/metal_api.py](plugins/module_utils/metal/metal_api.py). Some attributes are directly mapped, others may have different names in the API response and Ansible module, and some may be more complex to extract. For instance, refer to `METAL_DEVICE_RESPONSE_ATTRIBUTE_MAP`.

If you're developing support for a new module/resource, you'll need to add a corresponding ..._RESPONSE_ATTRIBUTE_MAP and augment the `get_attribute_mapper` function.

##  3. <a name='infomodules'></a>_info modules

Modules which end on `_info` are alternative of Terraform datasources. They query existing resources in Equinix API. You can see template for info module in [template/metal_resource_info.py](template/metal_resource_info.py).

If you add a new `_info` module, you must add an entry to variable `LIST_KEYS` in [plugins/module_utils/metal/metal_api.py](plugins/module_utils/metal/metal_api.py). It's because responses to listing API methods have the resource lists in specifically names keys.

##  4. <a name='Generatingdocumentation'></a>Generating documentation

Documentation is generated from the `SPECDOC_META` variable in module scripts by running the `make docs` command. This process:

- Creates markdown in the `docs/modules` folder and reStructuredText in the `docs/inventory` folder (as ansible-specdoc does not support inventory plugins)
- Generates `README.md` based on existing modules and a template
- Injects `DOCUMENTATION`, `EXAMPLES`, and `RETURN` into module plugins

The logic for generating documentation is implemented in scripts. To view the details, examine the Makefile target specification.
