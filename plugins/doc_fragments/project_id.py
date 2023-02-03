# Copyright: (c) 2021, Equinix Metal
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class ModuleDocFragment(object):
    # Standard documentation
    DOCUMENTATION = '''
    options:
        project_id:
            description:
                - UUID of the project containing the resource.
                - You can supply this in the C(METAL_PROJECT_ID) environment variable.
            type: str
    '''
