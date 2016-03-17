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
def migrate():
    """tasks for migrating database"""
    print("database")

@task
def sync_db():
    """tasks for migrating database"""
    print("database")
