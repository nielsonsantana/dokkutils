from fabric.api import env as _env, cd
from fabric.api import hide, task
from settings import config

@task
def migrate():
    """tasks for migrating database"""
    print("database")

@task
def sync_db():
    """tasks for migrating database"""
    print("database")
