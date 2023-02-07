# (c) 2023, Equnix DevRel Team (@equinix)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible.module_utils.basic import missing_required_lib

import traceback

HAS_METAL_SDK = True
try:
    import equinixmetalpy
except ImportError:
    HAS_METAL_SDK = False
    HAS_METAL_SDK_EXC = traceback.format_exc()

METAL_USER_AGENT = 'ansible-metal'


class MissingEquinixSDK(Exception):
    def __init__(self, exception_traceback):
        self.exception_traceback = exception_traceback


def get_metal_client(api_token, api_url, ua_prefix):
    if not HAS_METAL_SDK:
        raise MissingEquinixSDK(missing_required_lib('equinixmetalpy'), HAS_METAL_SDK_EXC)
    ua = ua_prefix + METAL_USER_AGENT
    return equinixmetalpy.Client(
        credential=api_token,
        base_url=api_url,
        base_user_agent=ua,
        user_agent_overwrite=True,
    )
