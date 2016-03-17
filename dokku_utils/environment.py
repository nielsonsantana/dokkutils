from fabric.api import env as _env, cd
from fabric.api import hide, task
from settings import config

def base_environment(environment=""):
    """ Base environment for all environments """
    _env.environment = environment.lower()
    environment = environment.upper()
    application_name = config(environment+"_APPLICATION_NAME", '') or \
                        config("APPLICATION_NAME", '')

    _env.hosts = [config(environment + "_SERVER_HOST")]
    _env.user = config(environment +"_OS_USER",'root')
    _env.environment_variables = config(environment+"_ENVIRONMENT_VARIABLES",
                                        "env-config/production_env.env")
    _env.dokku_command = "ssh dokku@" + config(environment+"_SERVER_HOST",'')
    _env.app_name_dokku = application_name

    print("Connecting to %s..." % environment.lower())

@task
def production():
    """Staging config for deployment"""
    base_environment("production")

@task
def staging():
    """staging config for deployment"""
    base_environment("staging")

@task
def local():
    """local config for deployment"""
    base_environment("local")

@task
def test():
    """test config for deployment"""
    base_environment("test")

@task
def envs_update(args=""):
    """
    Setup all evironmnt varables
        example of usage:
        * fab staging update_envs_dokku

    """
    envs_map = enviroment_keys(_env.environment_variables)[1]
    _local(_env.dokku_command + " config:set %s %s %s " % (_env.app_name_dokku, envs_map, args))

@task
def envs_delete(args=""):
    """ Unset all envs on dokku"""
    envs_keys = enviroment_keys(_env.environment_variables)[0]
    _local(_env.dokku_command + " config:unset %s %s " % (_env.app_name_dokku, envs_keys))
