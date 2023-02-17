# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

try:
    import equinixmetalpy
    import metal_python
except ImportError:
    # This is handled in raise_if_missing_equinixmetalpy()
    pass

from ansible_collections.equinix.cloud.plugins.module_utils import (
    metal_client,
    action,
    utils,
)


id_getter = utils.ParamsParser("id")
mp_id_getter = utils.MPParamsParser(["id"])
mp_no_params = utils.MPParamsParser([])


def get_configs(mpc):
    """
    This function returns a dictionary of API call configurations.
    """

    # we check for the presence of the equinixmetalpy module here, because
    # the ApiCallConfigs use classes straight from the equinixmetalpy module
    # and we prefer to fail early and hopefully into module.fail_json()
    metal_client.raise_if_missing_equinixmetalpy()
    metal_client.raise_if_missing_metal_python()

    return {
        # GETTERS
        ('metal_device', action.GET): utils.Specs(
            equinixmetalpy.Client.find_device_by_id,
            id_getter,
            ),
        ('metal_project', action.GET): utils.MPSpecs(
            metal_python.ProjectsApi(mpc).find_project_by_id,
            mp_id_getter,
            ),
        ('metal_ip_reservation', action.GET): utils.Specs(
            equinixmetalpy.Client.find_ip_address_by_id,
            id_getter,
        ),
        ('metal_ip_assignment', action.GET): utils.Specs(
            equinixmetalpy.Client.find_ip_address_by_id,
            id_getter,
        ),

        # LISTERS
        ('metal_project_device', action.LIST): utils.Specs(
            equinixmetalpy.Client.find_project_devices,
            utils.ParamsParser("project_id"),
        ),
        ('metal_organization_device', action.LIST): utils.Specs(
            equinixmetalpy.Client.find_organization_devices,
            utils.ParamsParser("organization_id"),
            ),
        ('metal_project', action.LIST): utils.MPSpecs(
            metal_python.ProjectsApi(mpc).find_projects,
            mp_no_params,
        ),
        ('metal_organization_project', action.LIST): utils.Specs(
            equinixmetalpy.Client.find_organization_projects,
            utils.ParamsParser("organization_id"),
            ),
        ('metal_ip_reservation', action.LIST): utils.Specs(
            equinixmetalpy.Client.find_ip_reservations,
            utils.ParamsParser(["project_id", "type"], as_list=["type"]),
            ),
        ('metal_ip_assignment', action.LIST): utils.Specs(
            equinixmetalpy.Client.find_ip_assignments,
            utils.ParamsParser("device_id"),
        ),

        # DELETERS
        ('metal_device', action.DELETE): utils.Specs(
            equinixmetalpy.Client.delete_device,
            id_getter,
            ),
        ('metal_project', action.DELETE): utils.MPSpecs(
            metal_python.ProjectsApi(mpc).delete_project,
            mp_id_getter,
            ),
        ('metal_ip_reservation', action.DELETE): utils.Specs(
            equinixmetalpy.Client.delete_ip_address,
            id_getter,
        ),
        ('metal_ip_assignment', action.DELETE): utils.Specs(
            equinixmetalpy.Client.delete_ip_address,
            id_getter,
        ),


        # CREATORS
        ('metal_device_metro', action.CREATE): utils.Specs(
            equinixmetalpy.Client.create_device,
            utils.ParamsParser("project_id"),
            equinixmetalpy.models.DeviceCreateInMetroInput,
            ),
        ('metal_device_facility', action.CREATE): utils.Specs(
            equinixmetalpy.Client.create_device,
            utils.ParamsParser("project_id"),
            equinixmetalpy.models.DeviceCreateInFacilityInput,
        ),
        ('metal_project', action.CREATE): utils.MPSpecs(
            metal_python.ProjectsApi(mpc).create_project,
            mp_no_params,
            'project_create_from_root_input',
            metal_python.ProjectCreateFromRootInput,
        ),
        ('metal_organization_project', action.CREATE): utils.MPSpecs(
            metal_python.OrganizationsApi(mpc).create_organization_project,
            utils.MPParamsParser(["organization_id"]),
            "project_create_input",
            metal_python.ProjectCreateInput,
            ),
        ('metal_ip_reservation', action.CREATE): utils.Specs(
            equinixmetalpy.Client.request_ip_reservation,
            utils.ParamsParser("project_id"),
            equinixmetalpy.models.IPReservationRequestInput,
        ),
        ('metal_ip_assignment', action.CREATE): utils.Specs(
            equinixmetalpy.Client.create_ip_assignment,
            utils.ParamsParser("device_id"),
            equinixmetalpy.models.IPAssignmentInput,
        ),

        # UPDATERS
        ('metal_device', action.UPDATE): utils.Specs(
            equinixmetalpy.Client.update_device,
            id_getter,
            equinixmetalpy.models.DeviceUpdateInput,
        ),
        ('metal_project', action.UPDATE): utils.MPSpecs(
            metal_python.ProjectsApi(mpc).update_project,
            mp_id_getter,
            'project_update_input',
            metal_python.ProjectUpdateInput,
        ),
        ('metal_ip_reservation', action.UPDATE): utils.Specs(
            equinixmetalpy.Client.update_ip_address,
            id_getter,
            equinixmetalpy.models.IPAssignmentUpdateInput,
        ),
    }
