from __future__ import print_function
from __future__ import unicode_literals

import imp
import json
import os
import re
import sys
import yaml

from contextlib import contextmanager
from functools import wraps
from getpass import getpass
from getpass import getuser
from glob import glob
from posixpath import join

import database as db
import environment as en
import fabric
import hosts as target
import system as system

from fabric.api import cd
from fabric.api import env as _env
from fabric.api import hide
from fabric.api import local as _local
from fabric.api import prefix
from fabric.api import run as _run
from fabric.api import sudo as _sudo
from fabric.api import task
from fabric.colors import blue
from fabric.colors import green
from fabric.colors import red
from fabric.colors import yellow
from fabric.contrib.files import exists
from fabric.contrib.files import upload_template
from settings import config

# ENVIRONMENTS


sys.path.append(os.getcwd())

try:
    from fabfile import *
    fabfile_path = os.path.join(os.getcwd(), "fabfile.py")
    fab = imp.load_source('fabfile', fabfile_path)
except Exception, e:
    print("Warning: No file 'fabfile.py' found.")


def load_ymal_config():
    current_path = os.getcwd()
    config_yml = os.path.join(current_path, "config.yaml")
    config_yml2 = os.path.join(current_path, "config.yml")

    if os.path.exists(config_yml):
        pass
    elif os.path.exists(config_yml2):
        config_yml = config_yml2
    else:
        return

    ym_file = open(config_yml, "r")
    yMap = yaml.safe_load(ym_file)
    if not yMap:
        return

    for k, v in yMap.get("enviroments", {}).iteritems():
        # print(k, **v)
        new_task = target.new_environment_wrapper(k, **v)
        new_task.__doc__ = " %s host" % k
        setattr(target, k, new_task)

load_ymal_config()


def run_command(command):

    if command.startswith("dokku") and not command.startswith("dokkutils"):
        command = command.replace("dokku", '', 1)
        command = "%s %s" % (_env.dokku_command, command)
        res = _local(command)
    else:
        _local(command)


def parse_commands(script):
    commands = script.replace("\n", '').replace("\\", '').split(";")
    commands = [' '.join(x.strip().split()) for x in commands]
    return filter(lambda x: not x.startswith("#"), commands)


@task
def run(command=""):
    """ Run custom commands from dokku """
    run_command("dokku " + command)


@task
def logs(args=""):
    run_command("dokku logs %s" % _env.app_name_dokku)
