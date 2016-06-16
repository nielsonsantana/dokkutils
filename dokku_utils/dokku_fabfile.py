from __future__ import print_function, unicode_literals

import os
import re
import sys
import imp
from functools import wraps
from getpass import getpass, getuser
from glob import glob
from contextlib import contextmanager
from posixpath import join
import json
import yaml

import fabric
from fabric.api import env as _env, cd, prefix, sudo as _sudo, run as _run
from fabric.api import hide, task, local as _local
from fabric.contrib.files import exists, upload_template
from fabric.colors import yellow, green, blue, red
from settings import config
import environment as env
import database as db
import system as system
import hosts

##### ENVIRONMENTS


sys.path.append(os.getcwd())

try:
    from fabfile import *
    fabfile_path = os.path.join(os.getcwd(), "fabfile.py")
    l = imp.load_source('fabfile', fabfile_path)
except Exception, e:
    print("Warning: No file 'fabfile.py' found.")

def load_ymal_config():
    current_path = os.getcwd()
    ym_file = open(os.path.join(current_path, "config.yml"), "r")
    yMap = yaml.safe_load(ym_file)
    if not yMap:
        return

    for k, v in yMap.get("enviroments", {}).iteritems():
        new_task = hosts.new_environment_wrapper(k, **v)
        new_task.__doc__  = " %s host" % k
        setattr(hosts, k, new_task)

load_ymal_config()


def run_command(command):
    
    if command.startswith("dokku") and not command.startswith("dokkutils"):
        command = command.replace("dokku", '', 1)
        command = "%s %s" % (_env.dokku_command, command)
        res = _local(command)
    else:
        _local(command)

def parse_commands(script):
    commands = script.replace("\n",'').replace("\\",'').split(";")
    commands = [' '.join(x.strip().split()) for x in commands]
    return filter(lambda x: not x.startswith("#"), commands)

@task
def run(command=""):
    """ Run custom commands from dokku """
    run_command("dokku " + command)

@task
def deploy(args=""):
    """ Initial deployment of an applicatin  
        require file deploy.sh """
    folder = os.path.dirname(__file__)
    deploy_file = open(os.path.join(folder,"scripts","setup_application.sh"), 'r')
    script = deploy_file.read() % (_env)
    commands = parse_commands(script)
    print(commands)
    for command in commands:
        if command.startswith("dokku"):
            command = command.replace("dokku", '', 1)
            run(command)
        else:
            run_command(command)

@task
def deploy(args=""):
    """ Initial deployment of an applicatin  
        require file deploy.sh """
    folder = os.path.dirname(__file__)
    deploy_file = open(os.path.join(folder,"scripts","setup_application.sh"), 'r')
    # deploy_file = open("setup_application.sh", 'r')
    script = deploy_file.read() % (_env)
    commands = parse_commands(script)

    for command in commands:
        run_command(command)
