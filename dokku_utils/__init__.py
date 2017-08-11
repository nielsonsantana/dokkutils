#! encoding: utf-8
import os
import sys

from fabric import main as main_fabric
from fabric import state
from fabric.tasks import execute
from optparse import Option

# Adding default dokku_fabfile to no conflit with user created fabfile
sys.argv.append('--fabfile')
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.argv.append(os.path.join(dir_path, 'dokku_fabfile.py'))

# The default is show all dokkutils commands availables
# sys.argv.append("--list")


def main():
    # if sys.argv[-1] != "--list":
    #     sys.argv.remove("--list")
    main_fabric.main()

if __name__ == "__main__":
    main()
