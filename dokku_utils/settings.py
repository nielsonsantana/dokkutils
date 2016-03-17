import os
from decouple import AutoConfig

def _caller_path(self):
    return os.getcwd()

AutoConfig._caller_path = _caller_path
config = AutoConfig()
