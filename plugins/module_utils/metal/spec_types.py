# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import inspect
from typing import Callable, Dict, Optional
from re import sub

from ansible_collections.equinix.cloud.plugins.module_utils import (
    utils,
)


class Specs(object):
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
                raise ValueError('request_model_class must be a class, is {-1}'.format(type(request_model_class)))


class ApiCall(object):
    """
    A class representing an API call. It holds the configuration of the
    API call (ApiCallConfig) and the module parameters which are parsed
    into URL params and body params.

    API call body (if necessary) is created from the module parameters.
    """
    @staticmethod
    def _get_relevant_params(params):
        return {k: v for k, v in params.items() if v and k not in utils.SKIPPED_PARAMS}

    def __init__(self,
                 conf: Specs,
                 params: Optional[dict] = {},
                 ):
        self.conf = conf

        param_names = set(inspect.signature(conf.func).parameters.keys())
        self.sdk_kwargs = {}
        arg_mapping = self.conf.named_args_mapping or {}
        for param_name in param_names:
            lookup_name = param_name
            if param_name in arg_mapping:
                lookup_name = arg_mapping[param_name]
            value_from_ansible_module = params.get(lookup_name, None)
            if value_from_ansible_module is not None:
                self.sdk_kwargs[param_name] = value_from_ansible_module
        self.path_kwargs = self.sdk_kwargs.copy()

        if self.conf.request_model_class is not None:
            body_params = {k: v for k, v in params.items() if
                           (k not in utils.SKIPPED_PARAMS)
                           and (k not in param_names)
                           }
            request_model_instance = self.conf.request_model_class.from_dict(body_params)
            model_arg_name = snake_case(self.conf.request_model_class.__name__)
            self.sdk_kwargs[model_arg_name] = request_model_instance

    def do(self):
        sdk_function = self.conf.func

        result = sdk_function(**self.sdk_kwargs)
        return result

    def describe(self):
        return "{0} to {1}".format(self.conf.func.__name__, self.path_kwargs)


def snake_case(s):
    return '_'.join(
        sub('([A-Z][a-z]+)', r' \1',
            sub('([A-Z]+)', r' \1',
                s.replace('-', ' '))).split()).lower()
