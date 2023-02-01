# Copyright: (c) 2023, Equinix Metal
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class ModuleDocFragment(object):
    # Standard documentation
    DOCUMENTATION = '''
    options:
        filters:
            description:
                - Filter to apply to the list of resources.
                - For example
                - '`{"name": "resource_name_substring"}`'
                - '`{"hostname": "device_hostname_substring"}`'
            type: dict
    '''
