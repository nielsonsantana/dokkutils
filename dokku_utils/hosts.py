from fabric.api import env as _env, cd, local as _local
from fabric.api import hide, task
from settings import config
import yaml

def base_environment(environment=""):
    """ Base environment for all environments """
    _env.environment = environment.lower()
    environment = environment.upper()
    application_name = config(environment+"_APPLICATION_NAME", '') or \
                        config("APPLICATION_NAME", '')

    _env.host = config(environment + "_SERVER_HOST")
    _env.user = config(environment +"_OS_USER",'root')
    _env.environment_variables = config(environment+"_ENVIRONMENT_VARIABLES",
                                        "env-config/production_env.env")
    _env.dokku_command = "ssh dokku@" + config(environment+"_SERVER_HOST",'')
    _env.app_name_dokku = application_name

    print("Connecting to %s..." % environment.lower())

@task
def base_environment_ymal(environment="", **kwargs):
    """ %s config for deployment """

    def wrapper():
        _env.environment = environment.lower()
        environment = environment.upper()
        application_name = kwargs.get("application_name", '')

        _env.host = kwargs.get("host", '')
        _env.user = kwargs.get("os_user",'root')
        _env.environment_variables = kwargs.get("enviroment_vaiables_file", "")
        _env.dokku_command = "ssh dokku@" + kwargs.get("host", '')
        _env.app_name_dokku = application_name
        return _env
        # print("Connecting to %s..." % environment.lower())

    func = wrapper()    
    return func

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
            _env.host = kwargs.get("host", '')
        
        _env.user = kwargs.get("os_user",'root')
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
def dbproduction():
    """test config for deployment"""
    base_environment("dbproduction")

@task
def dbstaging():
    """test config for deployment"""
    base_environment("dbstaging")

@task
def dblocal():
    """test config for deployment"""
    base_environment("dblocal")



