# encoding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

import distutils.version
import os

import yaml

# Inits the logging system. Only shell logging, and exception and warning catching.
# File logging can be started by calling log.start_file_logger(name).
from .utils import log


def merge(user, default):
    """Merges a user configuration with the default one."""

    if isinstance(user, dict) and isinstance(default, dict):
        for kk, vv in default.items():
            if kk not in user:
                user[kk] = vv
            else:
                user[kk] = merge(user[kk], vv)

    return user


NAME = '{{cookiecutter.package_name}}'


# Loads config
yaml_kwds = dict()
yaml_version = distutils.version.StrictVersion(yaml.__version__)
if yaml_version >= distutils.version.StrictVersion('5.1'):
    yaml_kwds.update(Loader=yaml.FullLoader)

config_path = os.path.join(os.path.dirname(__file__), '/etc/{0}.yml'.format(NAME))
with open(config_path, "r") as fp:
    config = yaml.load(fp, **yaml_kwds)

# If there is a custom configuration file, updates the defaults using it.
custom_config_path = os.path.expanduser('~/.{0}/{0}.yml'.format(NAME))
if os.path.exists(custom_config_path):
    with open(custom_config_path, "r") as fp:
        custom_config = yaml.load(custom_config_path, **yaml_kwds)
    config = merge(custom_config, config)


__version__ = '{{cookiecutter.version}}'
