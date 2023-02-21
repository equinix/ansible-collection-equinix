#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from typing import Any, Dict, List, Optional, Tuple, Union, Callable
import inspect

SKIPPED_PARAMS = [
    "state",
    "metal_api_token",
    "metal_api_url",
    "metal_ua_prefix",
]

OPTIONAL_REQUEST_PARAMS = [
    "include",
    "exclude",
    "page"
    "per_page",
]


class ParamsParser:
    """
    A class to parse the module parameters into a tuple:
    (id_params for URL path, params for request body)

    Right now it only pops ids from the module params, later it might also
    do some validation and/or transformation of the params for the request
    body.
    """

    def __init__(
        self,
        param_names: Union[str, List[str]] = [],
        as_list: List[str] = []):
        self.positional_param_names = param_names if isinstance(param_names, list) else [param_names]

        # def find_ip_reservations(
        #    self,
        #    id: str,
        #    types: Optional[List[Union[str, "_models.Enum18"]]] = None,
        #    include: Optional[List[str]] = None,
        #    exclude: Optional[List[str]] = None,
        #    per_page: int = 250,
        #    **kwargs: Any
        self.as_list = as_list

    def parse(self, params):
        id_params = []
        for name in self.positional_param_names:
            if name not in params:
                raise ValueError('Missing required option: {0}'.format(name))
            if name in self.as_list:
                id_params.append([params.pop(name)])
            else:
                id_params.append(params.pop(name))
        return id_params, params


class MPParamsParser:

    def __init__(
        self,
        sdk_required_params: List[str] = [],
        sdk_optional_params: List[str] = [],
        as_list: List[str] = []):
        self.sdk_required_params = sdk_required_params
        self.sdk_optional_params = sdk_optional_params
        self.as_list = as_list

        # def find_ip_reservations(
        #    self,
        #    id: str,
        #    types: Optional[List[Union[str, "_models.Enum18"]]] = None,
        #    include: Optional[List[str]] = None,
        #    exclude: Optional[List[str]] = None,
        #    per_page: int = 250,
        #    **kwargs: Any

    def parse(self, params):
        sdk_kwargs = {}
        for name in self.sdk_required_params:
            if name not in params:
                raise ValueError('Missing required option: {0}'.format(name))
            if name in self.as_list:
                sdk_kwargs[name] = [params.pop(name)]
            else:
                sdk_kwargs[name] = params.pop(name)
        for name in self.sdk_optional_params:
            if name in params:
                if name in self.as_list:
                    sdk_kwargs[name] = [params.pop(name)]
                else:
                    sdk_kwargs[name] = params.pop(name)
        return sdk_kwargs


class Specs(object):
    """
    Specification of API call for certain resource type, action and parameters parser.

    An instance might specify API calls for GETting metal_device and parsing 
    resource attributes to ansible dict.
    """

    def __init__(self,
                 func: Callable,
                 params_parser: Optional[ParamsParser] = None,
                 request_model_class: Optional[Callable] = None,
                 ):
        self.func = func
        self.params_parser = params_parser
        self.request_model_class = request_model_class
        if self.request_model_class is not None:
            if not inspect.isclass(request_model_class):
                raise ValueError('request_model_class must be a class, is {0}'.format(type(request_model_class)))


class MPSpecs(object):
    """
    Specification of API call for certain resource type, action and parameters parser.

    An instance might specify API calls for GETting metal_device and parsing 
    resource attributes to ansible dict.
    """

    def __init__(self,
                 func: Callable,
                 named_args_mapping: Optional[Dict[str, str]] = None,
                 request_model_class: Optional[Callable] = None,
                 ):
        self.func = func
        self.named_args_mapping = named_args_mapping
        self.request_model_class = request_model_class
        if self.request_model_class is not None:
            if not inspect.isclass(request_model_class):
                raise ValueError('request_model_class must be a class, is {0}'.format(type(request_model_class)))


def dict_get(d, key):
    """
    Get a value from a nested dict using a dot-separated key.
    """
    import q
    q(d, key)
    for k in key.split("."):
        if k in d:
            d = d[k]
            if isinstance(d, dict):
                continue
            return d
        else:
            return None
    return d
