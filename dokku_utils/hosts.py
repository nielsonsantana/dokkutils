# -*- coding: utf-8 -*-

import yaml

from fabric.api import cd
from fabric.api import env as _env
from fabric.api import hide
from fabric.api import local as _local
from fabric.api import task
from settings import config


def base_environment(environment=""):
    """ Base environment for all environments """
    _env.environment = environment.lower()
    environment = environment.upper()
    application_name = config(environment + "_APPLICATION_NAME", '') or \
        config("APPLICATION_NAME", '')

    _env.host = config(environment + "_SERVER_HOST", '')
    _env.user = config(environment + "_OS_USER", 'root')
    _env.environment_variables = config(
        environment + '_ENVIRONMENT_VARIABLES', '')
    _env.dokku_command = "ssh dokku@" + \
        config(environment + "_SERVER_HOST", '')
    _env.app_name_dokku = application_name

    print("Connecting to %s..." % environment.lower())


def new_environment_wrapper(environment="", **kwargs):
    """ %s config for deployment """

    def func():
        environment = func.environment
        kwargs = func.kwargs

        _env.environment = environment.lower()
        environment = environment.upper()
        application_name = kwargs.get("application_name", '')

        if type(kwargs.get("host", '')) == list:
            host = kwargs.get("host", '')[0]
            _env.hosts = kwargs.get("host", '')
        else:
            host = kwargs.get("host", '')
            _env.host = kwargs.get("host", '')

        _env.user = kwargs.get("os_user", 'root')
        _env.environment_variables = kwargs.get("enviroment_vaiables_file", "")

        _env.dokku_command = "ssh dokku@" + host
        _env.app_name_dokku = application_name

        return ""

    def wrapper(environment, **kwargs):
        func.environment = environment
        func.kwargs = kwargs
        return task(name=environment.lower(),
                    environment=environment,
                    kwargs=kwargs)(func)

    return wrapper(environment, **kwargs)
