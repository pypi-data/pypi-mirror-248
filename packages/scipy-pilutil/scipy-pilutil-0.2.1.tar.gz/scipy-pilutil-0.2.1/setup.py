# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from codecs import open
from os import path
import re


package_name = 'scipy-pilutil'
module_name = package_name.replace('-', '_')

root_dir = path.abspath(path.dirname(__file__))

def _requires_from_file(filename):
    return open(filename).read().splitlines()

with open(path.join(root_dir, module_name, '__init__.py')) as f:
    init_text = f.read()
    version = re.search(r'__version__\s*=\s*[\'\"](.+?)[\'\"]', init_text).group(1)
    license = re.search(r'__license__\s*=\s*[\'\"](.+?)[\'\"]', init_text).group(1)
    author = re.search(r'__author__\s*=\s*[\'\"](.+?)[\'\"]', init_text).group(1)
    author_email = re.search(r'__author_email__\s*=\s*[\'\"](.+?)[\'\"]', init_text).group(1)
    url = re.search(r'__url__\s*=\s*[\'\"](.+?)[\'\"]', init_text).group(1)

assert version
assert license
assert author
assert author_email
assert url

setup(
    name=package_name,
    version=version,
    license=license,
    description="scipy.misc.pilutil module for legacy code",
    author=author,
    author_email=author_email,
    url=url,
    packages=find_packages(),
    install_requires=_requires_from_file('requirements.txt')
)
