__version__ = "0.1.0.dev0"
virtualenv_version = __version__  # legacy

import sys
from fabric.tasks import execute
from fabric import main as main_fabric
from fabric import state
from optparse import Option

# Adding default dokku_fabfile to no conflit with user created fabfile
sys.argv.append('--fabfile')
sys.argv.append('dokku_fabfile.py')

def main(args=[]):
    main_fabric.main()

if __name__ == "__main__":
    main()
