# (c) 2023, Equnix DevRel Team (@equinix)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


import traceback
import re

HAS_EQUINIX_METAL = True
HAS_EQUINIX_METAL_EXC = None
try:
    import equinix_metal
    from equinix_metal.rest import ApiException
    from equinix_metal.exceptions import NotFoundException
except ImportError:
    HAS_EQUINIX_METAL = False
    HAS_EQUINIX_METAL_EXC = traceback.format_exc()

USER_AGENT = 'ansible-equinix'
API_URL = 'https://api.equinix.com/metal/v1'
TOKEN_ENVVARS = ['METAL_API_TOKEN', 'METAL_AUTH_TOKEN']
URL_ENVVARS = ['METAL_API_URL']

RESOURCE_NAME_RE = r'^({0}|{0}{1}*{0})$'.format(r'[a-zA-Z0-9]', r'[a-zA-Z0-9\-_ ]')
HOSTNAME_RE = r'^({0}\.)*{0}$'.format(RESOURCE_NAME_RE)
UUID_RE = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'


class MissingMetalPythonError(Exception):
    def __init__(self, exception_traceback):
        self.exception_traceback = exception_traceback


def has_equinix_metal():
    return HAS_EQUINIX_METAL


def raise_if_missing_equinix_metal():
    if not HAS_EQUINIX_METAL:
        raise MissingMetalPythonError(HAS_EQUINIX_METAL_EXC)


def get_equinix_metal_client(api_token, api_url=API_URL, ua_prefix=""):
    raise_if_missing_equinix_metal()
    ua = ua_prefix + USER_AGENT
    conf = equinix_metal.Configuration(
        host=api_url,
    )
    conf.api_key['x_auth_token'] = api_token
    #conf.debug = True
    mpc = equinix_metal.ApiClient(conf)
    mpc.user_agent = ua
    return mpc


def is_valid_uuid(uuid):
    return re.match(UUID_RE, uuid) is not None


def raise_if_invalid_uuid(uuid):
    if not is_valid_uuid(uuid):
        raise ValueError("Invalid UUID: %s, regexp for UUID is %s" % (uuid, UUID_RE))


def is_valid_hostname(hostname):
    return re.match(HOSTNAME_RE, hostname) is not None


def raise_if_invalid_hostname(hostname):
    if not is_valid_hostname(hostname):
        raise ValueError("Invalid hostname: %s, regexp for hostname is %s" % (hostname, HOSTNAME_RE))


def is_valid_resource_name(name):
    return re.match(RESOURCE_NAME_RE, name) is not None


def raise_if_invalid_resource_name(name):
    if not is_valid_resource_name(name):
        raise ValueError("Invalid resource name: %s, regexp for resource name is %s" % (name, RESOURCE_NAME_RE))
