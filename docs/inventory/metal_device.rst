.. _metal_device_module:


metal_device -- Equinix Metal Device inventory source
=====================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Reads device inventories from Equinix Metal. Uses YAML configuration file that ends with equinix_metal.(yml|yaml). ansible_host is set to first public IP address of the device.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3
- metal_python >= 0.0.1



Parameters
----------

  **plugin (Required, type=str):**
    \• Token that ensures this is a source file for the plugin.

    \• Options: `equinix_metal`, `equinix.cloud.metal_device`


  **metal_api_token (Required, type=str):**
    \• Equinix Metal API token. Can also be specified via METAL_AUTH_TOKEN environment variable.



  **project_ids (type=list):**
    \• List of Equinix Metal project IDs to query for devices.


  **strict (type=bool):**
    \• If V(yes) make invalid entries a fatal error, otherwise skip and continue.

    \• Since it is possible to use facts in the expressions they might not always be available and we ignore those errors by default.


  **compose (type=dict):**
    \• Create vars from jinja2 expressions.


  **groups (type=dict):**
    \• Add hosts to group based on Jinja2 conditionals.


  **keyed_groups (type=list):**
    \• Add hosts to group based on the values of a variable.


      **parent_group (type=str):**
        \• parent group for keyed group


      **prefix (type=str):**
        \• A keyed group name will start with this prefix


      **separator (type=str, default=_):**
        \• separator used to build the keyed group name


      **key (type=str):**
        \• The key from input dictionary used to generate groups


      **default_value (type=str):**
        \• The default value when the host variable's value is an empty string.

        \• This option is mutually exclusive with O(keyed_groups[].trailing_separator).


      **trailing_separator (type=bool, default=True):**
        \• Set this option to V(False) to omit the O(keyed_groups[].separator) after the host variable when the value is an empty string.

        \• This option is mutually exclusive with O(keyed_groups[].default_value).



  **use_extra_vars (type=bool):**
    \• Merge extra vars into the available variables for composition (highest precedence).


  **leading_separator (type=boolean, default=True):**
    \• Use in conjunction with keyed_groups.

    \• By default, a keyed group that does not have a prefix or a separator provided will have a name that starts with an underscore.

    \• This is because the default prefix is "" and the default separator is "_".

    \• Set this option to False to omit the leading underscore (or other separator) if no prefix is given.

    \• If the group name is derived from a mapping the separator is still used to concatenate the items.

    \• To not use a separator in the group name at all, set the separator for the keyed group to an empty string instead.







Examples
--------

.. code-block:: yaml+jinja

    
    plugin: equinix.cloud.metal_device
    strict: false
    keyed_groups:
      - prefix: tag
        key: tags
      - prefix: equinix_metal_plan
        key: plan
      - key: metro
        prefix: equinix_metal_metro
      - key: state
        prefix: equinix_metal_state






Status
------





Authors
~~~~~~~

- Equinix DevRel Team (@equinix) <support@equinix.com>

