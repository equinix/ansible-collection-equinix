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
        ('metal_hardware_reservation', action.GET): spec_types.Specs(
            equinix_metal.HardwareReservationsApi(mpc).find_hardware_reservation_by_id,
        ),
        ("metal_organization", action.GET): spec_types.Specs(
            equinix_metal.OrganizationsApi(mpc).find_organization_by_id,
        ),
        ("metal_vlan", action.GET): spec_types.Specs(
            equinix_metal.VLANsApi(mpc).get_virtual_network,
        ),
        ("metal_connection", action.GET): spec_types.Specs(
            equinix_metal.InterconnectionsApi(mpc).get_interconnection,
        ),
        ('metal_vrf', action.GET): spec_types.Specs(
            equinix_metal.VRFsApi(mpc).find_vrf_by_id,
        ),
        ("metal_gateway", action.GET): spec_types.Specs(
            equinix_metal.MetalGatewaysApi(mpc).find_metal_gateway_by_id,
            extra_kwargs={"include": ["ip_reservation"]},
        ),
        ("metal_bgp_session", action.GET): spec_types.Specs(
            equinix_metal.BGPApi(mpc).find_bgp_session_by_id,
        ),
        ('metal_project_bgp_config', action.GET): spec_types.Specs(
            equinix_metal.BGPApi(mpc).find_bgp_config_by_project,
        ),
        ("metal_plan", action.GET): spec_types.Specs(
            equinix_metal.PlansApi(mpc).find_plans_by_project,
        ),
        ('metal_virtual_circuit', action.GET): spec_types.Specs(
            equinix_metal.InterconnectionsApi(mpc).get_virtual_circuit,
        ),
        ('metal_virtual_circuit_vrf', action.GET): spec_types.Specs(
            equinix_metal.InterconnectionsApi(mpc).get_virtual_circuit,
        ),
        ('metal_user', action.GET): spec_types.Specs(
            equinix_metal.UsersApi(mpc).find_current_user,
        ),

        # LISTERS
        ('metal_project_device', action.LIST): spec_types.Specs(
            equinix_metal.DevicesApi(mpc).find_project_devices_all_pages,
            {'id': 'project_id'},
        ),
        ('metal_organization_device', action.LIST): spec_types.Specs(
            equinix_metal.DevicesApi(mpc).find_organization_devices_all_pages,
            {'id': 'organization_id'},
        ),
        ('metal_project', action.LIST): spec_types.Specs(
            equinix_metal.ProjectsApi(mpc).find_projects_all_pages,
        ),
        ('metal_organization_project', action.LIST): spec_types.Specs(
            equinix_metal.OrganizationsApi(mpc).find_organization_projects_all_pages,
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
        ('metal_project_ssh_key', action.LIST): spec_types.Specs(
            equinix_metal.SSHKeysApi(mpc).find_project_ssh_keys,
            {'id': 'project_id'}
        ),
        ('metal_organization', action.LIST): spec_types.Specs(
            equinix_metal.OrganizationsApi(mpc).find_organizations_all_pages,
            {'personal': 'personal', 'with_projects': 'with_projects'},
        ),
        ('metal_operating_system', action.LIST): spec_types.Specs(
            equinix_metal.OperatingSystemsApi(mpc).find_operating_systems,
        ),
        ('metal_metro', action.LIST): spec_types.Specs(
            equinix_metal.MetrosApi(mpc).find_metros,
        ),
        ('metal_project_hardware_reservation', action.LIST): spec_types.Specs(
            equinix_metal.HardwareReservationsApi(mpc).find_project_hardware_reservations_all_pages,
            {'id': 'project_id'},
        ),
        ('metal_vlan', action.LIST): spec_types.Specs(
            equinix_metal.VLANsApi(mpc).find_virtual_networks,
            {'id': 'project_id'},
        ),
        ('metal_connection_project', action.LIST): spec_types.Specs(
            equinix_metal.InterconnectionsApi(mpc).project_list_interconnections_all_pages,
            {'id': 'project_id'},
        ),
        ('metal_connection_organization', action.LIST): spec_types.Specs(
            equinix_metal.InterconnectionsApi(mpc).organization_list_interconnections,
            {'id': 'organization_id'},
        ),
        ('metal_vrf', action.LIST): spec_types.Specs(
            equinix_metal.VRFsApi(mpc).find_vrfs,
            {'id': 'project_id'},
        ),
        ('metal_gateway', action.LIST): spec_types.Specs(
            equinix_metal.MetalGatewaysApi(mpc).find_metal_gateways_by_project,
            {'project_id': 'project_id'},
            extra_kwargs={"include": ["ip_reservation"]},
        ),
        ('metal_bgp_session', action.LIST): spec_types.Specs(
            equinix_metal.DevicesApi(mpc).find_bgp_sessions,
            {'id': 'device_id'},
        ),
        ('metal_bgp_session_by_project', action.LIST): spec_types.Specs(
            equinix_metal.BGPApi(mpc).find_bgp_config_by_project,
            {'id': 'project_id'},
        ),
        ('metal_plan', action.LIST): spec_types.Specs(
            equinix_metal.PlansApi(mpc).find_plans,
            {'category': 'category', 'type': 'type', 'slug': 'slug', 'include': 'include', 'exclude': 'exclude'},
        ),
        ('metal_virtual_circuit', action.LIST): spec_types.Specs(
            equinix_metal.InterconnectionsApi(mpc).list_interconnection_virtual_circuits,
            {'connection_id': 'connection_id'},
        ),
        ('metal_virtual_circuit_vrf', action.LIST): spec_types.Specs(
            equinix_metal.InterconnectionsApi(mpc).list_interconnection_virtual_circuits,
            {'connection_id': 'connection_id'},
        ),
        ('metal_port_virtual_circuit', action.LIST): spec_types.Specs(
            equinix_metal.InterconnectionsApi(mpc).list_interconnection_port_virtual_circuits,
            {'connection_id': 'connection_id', 'port_id': 'port_id'},
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
        ('metal_vlan', action.DELETE): spec_types.Specs(
            equinix_metal.VLANsApi(mpc).delete_virtual_network,
        ),
        ('metal_connection', action.DELETE): spec_types.Specs(
            equinix_metal.InterconnectionsApi(mpc).delete_interconnection,
        ),
        ('metal_vrf', action.DELETE): spec_types.Specs(
            equinix_metal.VRFsApi(mpc).delete_vrf,
        ),
        ('metal_gateway', action.DELETE): spec_types.Specs(
            equinix_metal.MetalGatewaysApi(mpc).delete_metal_gateway,
            extra_kwargs={"include": ["ip_reservation"]},
        ),
        ('metal_bgp_session', action.DELETE): spec_types.Specs(
            equinix_metal.BGPApi(mpc).delete_bgp_session,
        ),
        ('metal_virtual_circuit', action.DELETE): spec_types.Specs(
            equinix_metal.InterconnectionsApi(mpc).delete_virtual_circuit,
        ),
        ('metal_virtual_circuit_vrf', action.DELETE): spec_types.Specs(
            equinix_metal.InterconnectionsApi(mpc).delete_virtual_circuit,
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
        ('metal_project_ssh_key', action.CREATE): spec_types.Specs(
            equinix_metal.SSHKeysApi(mpc).create_project_ssh_key,
            {'id': 'project_id'},
            equinix_metal.SSHKeyCreateInput,
        ),
        ('metal_vlan', action.CREATE): spec_types.Specs(
            equinix_metal.VLANsApi(mpc).create_virtual_network,
            {'id': 'project_id'},
            equinix_metal.VirtualNetworkCreateInput,
        ),
        ('metal_connection_organization_dedicated', action.CREATE): spec_types.Specs(
            equinix_metal.InterconnectionsApi(mpc).create_organization_interconnection,
            {'id': 'organization_id'},
            equinix_metal.DedicatedPortCreateInput,
            equinix_metal.CreateOrganizationInterconnectionRequest,
        ),
        ('metal_connection_project_dedicated', action.CREATE): spec_types.Specs(
            equinix_metal.InterconnectionsApi(mpc).create_project_interconnection,
            {'id': 'project_id'},
            equinix_metal.DedicatedPortCreateInput,
            equinix_metal.CreateOrganizationInterconnectionRequest,
        ),
        ('metal_connection_project_vlanfabric', action.CREATE): spec_types.Specs(
            equinix_metal.InterconnectionsApi(mpc).create_project_interconnection,
            {'id': 'project_id'},
            equinix_metal.VlanFabricVcCreateInput,
            equinix_metal.CreateOrganizationInterconnectionRequest,
        ),
        ('metal_connection_project_vrf', action.CREATE): spec_types.Specs(
            equinix_metal.InterconnectionsApi(mpc).create_project_interconnection,
            {'id': 'project_id'},
            equinix_metal.VrfFabricVcCreateInput,
            equinix_metal.CreateOrganizationInterconnectionRequest,
        ),
        ('metal_vrf', action.CREATE): spec_types.Specs(
            equinix_metal.VRFsApi(mpc).create_vrf,
            {'id': 'project_id'},
            equinix_metal.VrfCreateInput,
        ),
        ('metal_gateway', action.CREATE): spec_types.Specs(
            equinix_metal.MetalGatewaysApi(mpc).create_metal_gateway,
            {'project_id': 'project_id'},
            equinix_metal.MetalGatewayCreateInput,
            equinix_metal.CreateMetalGatewayRequest,
            {"include": ["ip_reservation"]},
        ),

        ('metal_bgp_session', action.CREATE): spec_types.Specs(
            equinix_metal.DevicesApi(mpc).create_bgp_session,
            {'id': 'device_id'},
            equinix_metal.BGPSessionInput,
        ),
        ('metal_project_bgp_config', action.CREATE): spec_types.Specs(
            equinix_metal.BGPApi(mpc).request_bgp_config,
            {'id': 'project_id'},
            equinix_metal.BgpConfigRequestInput,
        ),
        ('metal_virtual_circuit', action.CREATE): spec_types.Specs(
            equinix_metal.InterconnectionsApi(mpc).create_interconnection_port_virtual_circuit,
            {'connection_id': 'connection_id', 'port_id': 'port_id'},
            equinix_metal.VlanVirtualCircuitCreateInput,
            equinix_metal.VirtualCircuitCreateInput,
        ),
        ('metal_virtual_circuit_vrf', action.CREATE): spec_types.Specs(
            equinix_metal.InterconnectionsApi(mpc).create_interconnection_port_virtual_circuit,
            {'connection_id': 'connection_id', 'port_id': 'port_id'},
            equinix_metal.VrfVirtualCircuitCreateInput,
            equinix_metal.VirtualCircuitCreateInput,
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
        ('metal_connection', action.UPDATE): spec_types.Specs(
            equinix_metal.InterconnectionsApi(mpc).update_interconnection,
            {},
            equinix_metal.InterconnectionUpdateInput,
        ),
        ('metal_hardware_reservation', action.UPDATE): spec_types.Specs(
            equinix_metal.HardwareReservationsApi(mpc).move_hardware_reservation,
            {},
            equinix_metal.MoveHardwareReservationRequest,
        ),
        ('metal_vrf', action.UPDATE): spec_types.Specs(
            equinix_metal.VRFsApi(mpc).update_vrf,
            {},
            equinix_metal.VrfUpdateInput,
        ),
        ('metal_bgp_session', action.UPDATE): spec_types.Specs(
            equinix_metal.BGPApi(mpc).update_bgp_session,
            {},
            equinix_metal.BGPSessionInput,
        ),
        ('metal_virtual_circuit', action.UPDATE): spec_types.Specs(
            equinix_metal.InterconnectionsApi(mpc).update_virtual_circuit,
            {},
            equinix_metal.VlanVirtualCircuitUpdateInput,
            equinix_metal.VirtualCircuitUpdateInput,
        ),
        ('metal_virtual_circuit_vrf', action.UPDATE): spec_types.Specs(
            equinix_metal.InterconnectionsApi(mpc).update_virtual_circuit,
            {},
            equinix_metal.VrfVirtualCircuitUpdateInput,
            equinix_metal.VirtualCircuitUpdateInput,
        ),
    }
