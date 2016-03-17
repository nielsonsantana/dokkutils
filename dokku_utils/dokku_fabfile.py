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
import system as system
import hosts

##### ENVIRONMENTS

# import yaml

# current_path = os.getcwd()

# stream = open(os.path.join(current_path,"hosts.yml"), "r")
# docs = yaml.load(stream)
# dic = dict()
# new_tasks = []
# for k in docs.keys():
#     dic[k] = {}
#     lev2 = docs.get(k)
#     for v in lev2:
#         if type(v) == dict:
#             dic[k].update(v)
#     new_task = task(name = k, **dic[k])(hosts.base_environment2)
#     new_task.__doc__  = " %s host" % k
#     setattr(hosts, k, new_task)


def run_command(command):
    print(command)
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
    run_command("dokku " + command)

@task
def deploy(args=""):
    """ Initial deployment of an applicatin  
        require file deploy.sh """
    deploy_file = open("deploy.sh", 'r')
    script = deploy_file.read() % (_env)
    commands = parse_commands(script)

    for command in commands:
        if command.startswith("dokku"):
            command = command.replace("dokku", '', 1)
            run_dokku(command)

@task
def deploy(args=""):
    """ Initial deployment of an applicatin  
        require file deploy.sh """
    deploy_file = open("deploy.sh", 'r')
    script = deploy_file.read() % (_env)
    commands = parse_commands(script)

    for command in commands:
        run_command(command)
