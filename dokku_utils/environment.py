from fabric.api import env as _env, cd, local as _local
from fabric.api import hide, task
from settings import config

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
def update_envs(args=""):
    """
    Setup all evironmnt varables
        example of usage:
        * fab staging update_envs_dokku

    """
    envs_map = enviroment_keys(_env.environment_variables)[1]
    if envs_map:
        _local(_env.dokku_command + " config:set %s %s %s " % (_env.app_name_dokku, envs_map, args))

@task
def delete_envs(args=""):
    """ Unset all environment variables on dokku"""
    envs_keys = enviroment_keys(_env.environment_variables)[0]
    if envs_keys:
        _local(_env.dokku_command + " config:unset %s %s " % (_env.app_name_dokku, envs_keys))

@task
def delete_env(env_key):
    """ Unset a specific environment variable on dokku"""
    if env_key:
        _local(_env.dokku_command + " config:unset %s %s " % (_env.app_name_dokku, env_key))

