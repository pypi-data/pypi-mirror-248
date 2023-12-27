#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
scf
~~~~~~~~~~~~~~
This module implements scf api
"""

import os
import json
#from enginefaas.exception import FaasException
#from enginefaas.common import credential
#from enginefaas.common.exception.sdk_exception import SDKException
from enginefaas.common.abstract_client import AbstractClient
from enginefaas.common.profile.http_profile import HttpProfile
from enginefaas.common.profile.client_profile import ClientProfile
import enginefaas.mapper as mapper


class Client(AbstractClient):
    """
    Client
    ~~~~~~~~~~~~~~
    This class default a client for scf api
    """

    def __init__(self,
                 secret_id=None,
                 secret_key=None,
                 token=None):

        self.secret_id = secret_id

        self.secret_key = secret_key

        self.token = token

        self.endpoint = os.environ.get("sdk_faas_gateway", None)
        if self.endpoint is None:
            self.endpoint = "gateway.openfaas.svc.cluster.local:8080"

        super().__init__("", "", profile=ClientProfile(httpProfile=HttpProfile(protocol='http', endpoint=self.endpoint, reqMethod="POST")))

    def invoke(self,
               component_full_name,
               data=None,
               deployment_env=None):

        self.secret_id = self.secret_id if self.secret_id is not None \
            else os.environ.get("FAAS_SECRETID", None)

        self.secret_key = self.secret_key if self.secret_key is not None \
            else os.environ.get("FAAS_SECRETKEY", None)

        self.token = self.token if self.token is not None \
            else os.environ.get("FAAS_SESSIONTOKEN", None)

        if deployment_env is None:
            self.env = os.environ.get("sdk_deployment_env", None)
        else:
            self.env = deployment_env
        self.user_id = os.environ.get("sdk_user_id", None)

        try:
            component_ns, component_last_name = get_ns_and_name(component_full_name)
            self.uri = "/function/" + mapper.map_svc(component_ns, component_last_name) + "." + mapper.map_ns(component_ns, self.env, self.user_id)
            res = self.call_json("Invoke", self.uri, data, options={"SkipSign": True})   
        except json.JSONDecodeError as e:
            print(e)
            res = self.call("Invoke", self.uri, data, options={"SkipSign": True})

        return res

    def __getattr__(self, attr_name):
        def wrap(*l, **args):
            log_type = None
            if 'log_type' in args:
                log_type = args['log_type']
                del args['log_type']
            invocation_type = None
            if 'invocation_type' in args:
                invocation_type = args['invocation_type']
                del args['invocation_type']

            qualifier = '$LATEST'
            if 'qualifier' in args:
                qualifier = args['qualifier']
                del args['qualifier']

            namespace = 'default'
            if 'namespace' in args:
                namespace = args['namespace']
                del args['namespace']

            return self.invoke(function_name=attr_name, namespace=namespace,
                               qualifier=qualifier,
                               log_type=log_type,
                               invocation_type=invocation_type, data=args)
        return wrap

    def __getitem__(self, attr_name):
        return self.__getattr__(attr_name)


def invoke(component_full_name,
           data=None,
           deployment_env=None):
    client = Client()
    return client.invoke(component_full_name=component_full_name, data=data, deployment_env=deployment_env)


def get_ns_and_name(component_full_name):
    split_list = component_full_name.split('.')
    name = split_list[-1]
    split_list.pop()
    ns = '.'.join(split_list)
    return ns, name