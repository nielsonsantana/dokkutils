from __future__ import print_function, unicode_literals

import os
import re
import sys
from functools import wraps
from getpass import getpass, getuser
from glob import glob
from contextlib import contextmanager
from posixpath import join
import json

from fabric.api import env, cd, prefix, sudo as _sudo, run as _run, hide, task, local
from fabric.contrib.files import exists, upload_template
from fabric.colors import yellow, green, blue, red
from decouple import config

@task
def staging():
    """Staging config for deployment"""
    env.hosts = [config("STAGING_SERVER_HOST", '')]
    env.user = config("STAGING_OS_USER",'root')
    env.environment = 'staging'
    env.environment_variables = config("STAGING_ENVIRONMENT_VARIABLES","config/staging_env.env")
    env.dokku_command = "ssh dokku@" + config("STAGING_SERVER_HOST",'')
    env.app_name_dokku = config("STAGING_APPLICATION_NAME")

def enviroment_keys(enviroment):
    """"""
    str_envs = open(env.environment_variables, 'r').read()
    json_envs = json.loads(str_envs)
    str_env_map = ''
    str_env_keys = ''
    for k, v in json_envs.items():
        str_env_map += ' %s="%s" ' % (k, v)
        str_env_keys += ' %s ' % k

    return str_env_keys, str_env_map

@task
def push_envs_dokku(args=""):
    """
    Setup all evironmnt varables
        example of usage:
        * fab staging_site setup_envs_openshift:'-l <account email>'

    """
    envs_keys = enviroment_keys(env.environment_variables)[1]
    
    dokku_command = env.dokku_command or staging_dokku_command 
    local(dokku_command + " config:set %s %s %s " % (env.app_name_dokku, envs_keys, args))




