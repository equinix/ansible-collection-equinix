# (c) 2023, Tomas Karasek (@t0mk) <tom.to.the.k@gmail.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import equinixmetalpy
from functools import partial


def _list_metal_organization_projects(params, client):
    org_id = params.get('organization_id')
    if org_id:
        return partial(client.find_organization_projects, org_id)
    raise Exception('no organization_id in module params when listing projects, this is a module bug')


def _list_metal_project_devices(params, client):
    project_id = params.get('project_id')
    if project_id:
        return partial(client.list_project_devices, project_id)
    raise Exception('no project_id in module params when listing devices, this is a module bug')

def _list_metal_organization_devices(params, client):
    org_id = params.get('organization_id')
    if org_id:
        return partial(client.list_organization_devices, org_id)
    raise Exception('no organization_id in module params when listing devices, this is a module bug')

def _create_metal_organization_project(params, client):
    org_id = params.get('organization_id')
    if org_id:
        return partial(client.create_organization_project, org_id)
    raise Exception('no organization_id in module params when creating project, this is a module bug')


def _create_metal_project_device(params, client):
    project_id = params.get('project_id')
    if project_id:
        return partial(client.create_project_device, project_id)
    raise Exception('no project_id in module params when creating device, this is a module bug')


def pick_creator(client: equinixmetalpy.Client, params: dict, resource_type: str):
    simple_creators = {
        'metal_project': client.create_project,
    }
    partial_creators = {
        'metal_organization_project': _create_metal_organization_project,
        'metal_device': _create_metal_project_device,
    }
    if resource_type in simple_creators:
        return simple_creators[resource_type]
    if resource_type in partial_creators:
        return partial_creators[resource_type](params, client)
    raise NotImplementedError(f'Creation of {resource_type} not implemented')


def pick_lister(client: equinixmetalpy.Client, params: dict, resource_type: str):
    simple_listers = {
        'metal_project': client.find_projects,
    }
    partial_listers = {
        'metal_organization_project': _list_metal_organization_projects,
        'metal_project_device': _list_metal_project_devices,
        'metal_organization_device': _list_metal_organization_devices,
    }

    if resource_type in simple_listers:
        return simple_listers[resource_type]
    if resource_type in partial_listers:
        return partial_listers[resource_type](params, client)
    raise NotImplementedError(f'Listing of {resource_type} not implemented')


def pick_getter(client: equinixmetalpy.Client, params: dict, resource_type: str):
    simple_getters = {
        'metal_project': client.find_project_by_id,
        'metal_device': client.find_device_by_id,
    }
    if resource_type in simple_getters:
        return simple_getters[resource_type]
    raise NotImplementedError(f'ID lookup for {resource_type} not implemented')


def pick_deleter(client: equinixmetalpy.Client, resource_type: str):
    simple_deleters = {
        'metal_project': client.delete_project,
        'metal_device': client.delete_device,
    }
    if resource_type in simple_deleters:
        return simple_deleters[resource_type]
    raise NotImplementedError(f'Delete of {resource_type} not implemented')


def pick_updater(client: equinixmetalpy.Client, params: dict, resource_type: str):
    simple_updaters = {
        'metal_project': client.update_project,
    }
    if resource_type in simple_updaters:
        return simple_updaters[resource_type]
    raise NotImplementedError(f'Update of {resource_type} not implemented')


SKIPPED_MODULE_PARAMS = [
    "state",
    "metal_api_token",
    "metal_api_url",
    "metal_ua_prefix",
]

CREATOR_REQUEST_MODEL_MAP = {
    'metal_project': equinixmetalpy.models.ProjectCreateFromRootInput,
    'metal_organization_project': equinixmetalpy.models.ProjectCreateFromRootInput,
}

UPDATER_REQUEST_MODEL_MAP = {
    'metal_project': equinixmetalpy.models.ProjectUpdateInput,
}
