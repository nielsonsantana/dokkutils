import os
import re
import shutil
import sys

from setuptools import Command, find_packages, setup

def read_file(*paths):
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, *paths)) as f:
        return f.read()

def get_version():
    version_file = read_file('dokku_utils.py')
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

# Get long_description from index.rst:
long_description = read_file('docs', 'index.rst')
long_description = long_description.strip().split('split here', 1)[0]

setup(
    name='dokkutils',
    version=get_version(),
    description="Virtual Python Environment builder",
    long_description=long_description,
    include_package_data=True,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='setuptools deployment installation distutils',
    author='Nielson Santana',
    author_email='nielsonnas@gmail.com',
    maintainer='',
    license='MIT',
    py_modules=['dokku_utils'],
    packages=['dokku_utils'],
    install_requires=[
        'fabric>=1.10.2',
        'python-decouple>=3.0',
        'fabtools>=0.19.0',
        'pyyaml>=3.11',
    ],
    entry_points={
        'console_scripts': ['dokkutils=dokku_utils:main'],
    },
    zip_safe=False,
)