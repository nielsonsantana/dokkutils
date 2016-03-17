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

from fabric.api import env as _env, cd, prefix, sudo as _sudo, run as _run
from fabric.api import hide, task, local as _local
from fabric.contrib.files import exists, upload_template
from fabric.colors import yellow, green, blue, red
from settings import config
import environment as env
import database as db

##### ENVIRONMENTS

def run_dokku():
    _local(_env.dokku_command)

def enviroment_keys(enviroment):
    """"""
    env_file = open(_env.environment_variables, 'r')
    str_env_map = ''
    str_env_keys = ''
    for line in env_file.readlines():
        line = line.replace('\n','')
        if line and not line.startswith("#"):
            k,v = line.split('=', 1)
            str_env_map += ' %s="%s" ' % (k, v)
            str_env_keys += ' ' + k

    return str_env_keys, str_env_map

@task
def deploy(args=""):
    """ Initial deployment of an applicatin  
        require file deploy.sh """
    deploy_file = open("deploy.sh", 'r')
    script = deploy_file.read() % (_env)
    print(script)
    rim()