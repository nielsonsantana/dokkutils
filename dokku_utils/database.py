from fabric.api import cd
from fabric.api import env as _env
from fabric.api import hide
from fabric.api import task
from settings import config


@task
def migrate():
    """tasks for migrating database"""
    print("database")


@task
def sync_db():
    """tasks for migrating database"""
    print("database")
