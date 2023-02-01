# Copyright: (c) 2023, Equinix Metal
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class ModuleDocFragment(object):
    # Standard documentation
    DOCUMENTATION = '''
    author:
        - Equinix DevRel Team (@equinix)
    options:
        metal_api_token:
            description:
                - The Equinix Metal API token to use
                - If not set, then the value of the METAL_API_TOKEN or METAL_AUTH_TOKEN environment variable is used.
            type: str
            required: true
        metal_api_url:
            description:
                - The Equinix Metal API URL to use
                - If not set, and the value of the METAL_API_URL environment variable is not set, then the default value is used.
            type: str
            default: https://api.equinix.com/metal/v1
        metal_ua_prefix:
            description:
                - The prefix to use for the User-Agent header
                - If not set, and the value of the METAL_UA_PREFIX environment variable is not set, then the empty string is used.
            type: str
    requirements:
        - "equinixmetalpy >= 0.0.1"
    '''
