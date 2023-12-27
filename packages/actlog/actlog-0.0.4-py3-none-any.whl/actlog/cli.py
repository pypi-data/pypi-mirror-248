import argparse
import os.path
import sys

import re

import yaml
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from . import helpformatter
from . import constants

from . import daemon
from . import log
from . import view
from . import passwordcli

help_long = """\
actlog-cli maintains and displays an action log
of what you are doing in your desktop environment.
"""

storage_help_long = """\
Where to store screenshots, logs, etc.
You may need space there.
"""


def resolve_config_file(args):

    def undash_dict_keys(data):
        """Recursively replace a-b with a_b in the keys of this dict.

        Does not handle arrays or any other types than dict
        """
        for k in list(data.keys()):
            if type(data[k]) is dict:
                undash_dict_keys(data[k])
            if re.search('-', k):
                new_key = re.sub('-', '_', k)
                data[new_key] = data[k]
                del data[k]

    def merge_dict_into_namespace(a_dict, ns):
        """Add the keys of the dict to the namespace."""
        for k in a_dict.keys():
            ns.__dict__[k] = a_dict[k]

    def use_config(config):
        undash_dict_keys(config)
        config_keys = ['global']
        if 'config_key' in args:
            config_keys.append(args.config_key)
        for k in config_keys:
            if k in config:
                merge_dict_into_namespace(config[k], args)

    config_file = os.path.expanduser(args.config_file)
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = yaml.load(f, Loader=Loader)
            use_config(config)


def cli_main():
    parser = argparse.ArgumentParser(
        prog='actlog',
        formatter_class=helpformatter.All,
        description=help_long)

    root_storage_dir = os.path.expanduser(constants.root_storage_dir)
    parser.add_argument(
        '--config-file',
        metavar="FILE",
        default=os.path.join(root_storage_dir, "config.yaml"),
        help=storage_help_long)

    parser.add_argument(
        '--storage',
        metavar="DIR",
        default=os.path.join(root_storage_dir, "storage"),
        help=storage_help_long)

    subparsers = parser.add_subparsers(help='sub-command help')

    log.add_parser(subparsers)
    view.add_parser(subparsers)
    daemon.add_parser(subparsers)
    passwordcli.add_parser(subparsers)

    args = parser.parse_args()

    storage_dir = os.path.expanduser(args.storage)
    if not os.path.exists(storage_dir):
        os.makedirs(storage_dir)
    if not os.path.isdir(storage_dir):
        raise RuntimeError(
            f'Expected --storage="{storage_dir}" to be a directory'
        )

    resolve_config_file(args)

    def under_storage(*path_segments):
        return os.path.join(storage_dir, *path_segments)

    args.under_storage = under_storage
    if not 'func' in args:
        parser.print_help()
        sys.exit(0)

    args.func(args)
