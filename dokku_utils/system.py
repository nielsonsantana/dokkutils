from fabric.api import env as _env, cd, local as _local, sudo as _sudo
from fabric.api import hide, task
from settings import config


@task
def add_swap(size=0):
    """ Add swap space to a system:
        parameters:
            size: size in megabits
        """
    _sudo("sudo fallocate -l %sMB /swapfile;" % size)  # Create /swapfile
    _sudo("sudo chmod 600 /swapfile;")        # Lock down permissions.
    _sudo("sudo mkswap /swapfile")  # Criar arquivos
