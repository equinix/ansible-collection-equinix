# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

try:
    import equinix_metal
except ImportError:
    # This is handled in raise_if_missing_equinix_metal()
    pass

from ansible_collections.equinix.cloud.plugins.module_utils import (
    action,
    utils,
)

from ansible_collections.equinix.cloud.plugins.module_utils.metal import (
    metal_client,
    spec_types,
)


def build_api_call(specs: spec_types.Specs, params: dict):
    return spec_types.ApiCall(specs, params)


def get_routes(mpc):
    """
    This function returns a dictionary of API call configurations.
    """

    # we check for the presence of the equinix_metal module here, because
    # the ApiCallConfigs use classes straight from the equinix_metal module
    # and we prefer to fail early and hopefully into module.fail_json()
    metal_client.raise_if_missing_equinix_metal()

    return {
        # GETTERS
        ('metal_device', action.GET): spec_types.Specs(
            equinix_metal.DevicesApi(mpc).find_device_by_id,
            ),
        ('metal_project', action.GET): spec_types.Specs(
            equinix_metal.ProjectsApi(mpc).find_project_by_id,
            ),
        ('metal_ip_reservation', action.GET): spec_types.Specs(
            equinix_metal.IPAddressesApi(mpc).find_ip_address_by_id,
        ),
        ('metal_ip_assignment', action.GET): spec_types.Specs(
            equinix_metal.IPAddressesApi(mpc).find_ip_address_by_id,
        ),
        ('metal_ssh_key', action.GET): spec_types.Specs(
            equinix_metal.SSHKeysApi(mpc).find_ssh_key_by_id,
        ),

        # LISTERS
        ('metal_project_device', action.LIST): spec_types.Specs(
            equinix_metal.DevicesApi(mpc).find_project_devices,
            {'id': 'project_id'},
        ),
        ('metal_organization_device', action.LIST): spec_types.Specs(
            equinix_metal.DevicesApi(mpc).find_organization_devices,
            {'id': 'organization_id'},
        ),
        ('metal_project', action.LIST): spec_types.Specs(
            equinix_metal.ProjectsApi(mpc).find_projects,
        ),
        ('metal_organization_project', action.LIST): spec_types.Specs(
            equinix_metal.OrganizationsApi(mpc).find_organization_projects,
            {'id': 'organization_id'},
        ),
        ('metal_ip_reservation', action.LIST): spec_types.Specs(
            equinix_metal.IPAddressesApi(mpc).find_ip_reservations,
            {'id': 'project_id'},
        ),
        ('metal_available_ip', action.LIST): spec_types.Specs(
            equinix_metal.IPAddressesApi(mpc).find_ip_availabilities,
            {'id': 'reserved_ip_block_id'},
        ),
        ('metal_ip_assignment', action.LIST): spec_types.Specs(
            equinix_metal.DevicesApi(mpc).find_ip_assignments,
            {'id': 'device_id'}
        ),
        ('metal_ssh_key', action.LIST): spec_types.Specs(
            equinix_metal.SSHKeysApi(mpc).find_ssh_keys,
        ),
        ('metal_operating_system', action.LIST): spec_types.Specs(
            equinix_metal.OperatingSystemsApi(mpc).find_operating_systems,
        ),
        ('metal_metro', action.LIST): spec_types.Specs(
            equinix_metal.MetrosApi(mpc).find_metros,
        ),

        # DELETERS
        ('metal_device', action.DELETE): spec_types.Specs(
            equinix_metal.DevicesApi(mpc).delete_device,
            ),
        ('metal_project', action.DELETE): spec_types.Specs(
            equinix_metal.ProjectsApi(mpc).delete_project,
            ),
        ('metal_ip_reservation', action.DELETE): spec_types.Specs(
            equinix_metal.IPAddressesApi(mpc).delete_ip_address,
        ),
        ('metal_ip_assignment', action.DELETE): spec_types.Specs(
            equinix_metal.IPAddressesApi(mpc).delete_ip_address,
        ),
        ('metal_ssh_key', action.DELETE): spec_types.Specs(
            equinix_metal.SSHKeysApi(mpc).delete_ssh_key,
        ),


        # CREATORS
        ('metal_device', action.CREATE): spec_types.Specs(
            equinix_metal.DevicesApi(mpc).create_device,
            {'id': 'project_id'},
            equinix_metal.CreateDeviceRequest,
        ),
        ('metal_project', action.CREATE): spec_types.Specs(
            equinix_metal.ProjectsApi(mpc).create_project,
            {},
            equinix_metal.ProjectCreateFromRootInput,
        ),
        ('metal_organization_project', action.CREATE): spec_types.Specs(
            equinix_metal.OrganizationsApi(mpc).create_organization_project,
            {'id': 'organization_id'},
            equinix_metal.ProjectCreateInput,
            ),
        ('metal_ip_reservation', action.CREATE): spec_types.Specs(
            equinix_metal.IPAddressesApi(mpc).request_ip_reservation,
            {'id': 'project_id'},
            equinix_metal.models.RequestIPReservationRequest,
        ),
        ('metal_ip_assignment', action.CREATE): spec_types.Specs(
            equinix_metal.DevicesApi(mpc).create_ip_assignment,
            {'id': 'device_id'},
            equinix_metal.models.IPAssignmentInput,
        ),
        ('metal_ssh_key', action.CREATE): spec_types.Specs(
            equinix_metal.SSHKeysApi(mpc).create_ssh_key,
            {},
            equinix_metal.SSHKeyCreateInput,
        ),

        # UPDATERS
        ('metal_device', action.UPDATE): spec_types.Specs(
            equinix_metal.DevicesApi(mpc).update_device,
            {},
            equinix_metal.DeviceUpdateInput,
        ),
        ('metal_project', action.UPDATE): spec_types.Specs(
            equinix_metal.ProjectsApi(mpc).update_project,
            {},
            equinix_metal.ProjectUpdateInput,
        ),
        ('metal_ip_reservation', action.UPDATE): spec_types.Specs(
            equinix_metal.IPAddressesApi(mpc).update_ip_address,
            {},
            equinix_metal.models.IPAssignmentUpdateInput,
        ),
        ('metal_ssh_key', action.UPDATE): spec_types.Specs(
            equinix_metal.SSHKeysApi(mpc).update_ssh_key,
            {},
            equinix_metal.SSHKeyInput,
        ),
    }
