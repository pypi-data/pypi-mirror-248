import re
import shutil
import sys
from os import mkdir
from os.path import isfile, realpath, exists, dirname
from pathlib import Path
from shutil import copyfile

import munch
import oyaml as yaml
from cloudmesh.common.FlatDict import FlatDict
from cloudmesh.common.console import Console
from cloudmesh.common.dotdict import dotdict
from cloudmesh.common.util import backup_name
from cloudmesh.common.util import path_expand
from cloudmesh.common.variables import Variables
from cloudmesh.configuration.Config import Config

"""
This clas is similar to Config, but does not contain a shared state for the location where to find it.
It also does not mask secrets.
cat was removed
"""


# see also https://github.com/cloudmesh/client/blob/main/cloudmesh_client/cloud/register.py


class Configuration(object):
    """Configuration management class for Cloudmesh.

        This class allows you to manage and interact with the Cloudmesh configuration file (`cloudmesh.yaml`).
        It provides methods to load, save, and manipulate the configuration.

        Args:
            path (str): Path to the Cloudmesh configuration file (`cloudmesh.yaml`).
                        Default is `~/.cloudmesh/cloudmesh.yaml`.
        """

    def __init__(self, path='~/.cloudmesh/cloudmesh.yaml'):
        """Initialize the Config class.

        Args:
            path (str): A local file path to the Cloudmesh YAML config with a root element `cloudmesh`.
                        Default: `~/.cloudmesh/cloudmesh.yaml`.
        """
        self.path = path

        self.load(path=self.path)

    def set_debug_defaults(self):
        """Set default values for debug-related configurations if not already present."""
        for name in ["trace", "debug"]:
            if name not in self.variable_database:
                self.variable_database[name] = str(False)

    def default(self):
        """Retrieve the default configurations.

        Returns:
            dotdict: A dotdict representing the default configurations.
        """
        try:
            return dotdict(self.data["cloudmesh"]["default"])
        except:
            return None

    def load(self, path=None):
        """Load the Cloudmesh configuration file.

         Args:
             path (str): Path to the Cloudmesh configuration file (`cloudmesh.yaml`).
         """

        # VERBOSE("Load config")
        self.filename = Path(path_expand(path))

        self.config_folder = dirname(self.path)

        self.create(path=path)

        with open(self.path, "r") as stream:
            content = stream.read()
            # content = path_expand(content)
            content = self.spec_replace(content)
            self.data = yaml.load(content, Loader=yaml.SafeLoader)

        # print (self.data["cloudmesh"].keys())

        # self.data is loaded as nested OrderedDict, can not use set or get
        # methods directly

        if self.data is None:
            raise EnvironmentError(
                "Failed to load configuration file cloudmesh.yaml, "
                "please check the path and file locally")

        #
        # populate default variables
        #

        self.variable_database = Variables(filename="~/.cloudmesh/variable.dat")

        self.set_debug_defaults()

        try:
            default = self.default()
            if default is not None:
                for name in self.default():
                    if name not in self.variable_database:
                        self.variable_database[name] = default[name]
                if "cloud" in default:
                    self.cloud = default["cloud"]
                else:
                    self.cloud = None

        except Exception as e:
            print (e)



    def create(self, path=None):
        """creates the cloudmesh.yaml file in the specified location. The
        default is

            ~/.cloudmesh/cloudmesh.yaml

        If the file does not exist, it is initialized with a default. You still
        need to edit the file.

        Args:
            path (str): Path to the Cloudmesh configuration file (`cloudmesh.yaml`).
        """
        self.path = Path(path_expand(path))

        self.config_folder = dirname(self.path)

        if not exists(self.config_folder):
            mkdir(self.config_folder)

        if not isfile(self.path):
            source = Path(dirname(realpath(__file__)) + "/etc/cloudmesh.yaml")

            copyfile(source.resolve(), self.path)

            # read defaults
            self.__init__()

            defaults = self["cloudmesh.default"]

            # pprint(defaults)

            d = Variables()
            if defaults is not None:
                print("# Set default from yaml file:")

            for key in defaults:
                value = defaults[key]
                print("set {key}={value}".format(**locals()))
                d[key] = defaults[key]

    def save(self, path=None, backup=True):
        """Save the configuration to the Cloudmesh configuration file.

        Args:
            path (str): Path to the Cloudmesh configuration file (`cloudmesh.yaml`).
            backup (bool): If True, create a backup of the existing configuration file before saving.

        Note: not tested

        saves th dic into the file. It also creates a backup if set to true The
        backup filename  appends a .bak.NO where number is a number that is not
        yet used in the backup directory.
        """
        path = path_expand(path or self.location.config())
        if backup:
            destination = backup_name(path)
            shutil.copyfile(path, destination)
        yaml_file = self.data.copy()
        with open(self.path, "w") as stream:
            yaml.safe_dump(yaml_file, stream, default_flow_style=False)

    def spec_replace(self, spec):
        """Replace placeholders in the specification with actual values.

        Args:
            spec (str): The specification string.

        Returns:
            str: The specification with placeholders replaced.

        TODO: BUG: possible bug redundant char \{ in escape
                    may be relevant for python 2 may behave differnet in
                    differnt python versions, has to be checked. a unit test
                    should be created to just check the \{ issue
        """

        variables = re.findall(r"\{\w.+\}", spec)

        for i in range(0, len(variables)):
            data = yaml.load(spec, Loader=yaml.SafeLoader)

            m = munch.DefaultMunch.fromDict(data)

            for variable in variables:
                text = variable
                variable = variable[1:-1]
                try:
                    value = eval("m.{variable}".format(**locals()))
                    if "{" not in value:
                        spec = spec.replace(text, value)
                except:
                    value = variable
        return spec

    def dict(self):
        """Get the configuration as a dictionary.

        Returns:
            dict: The configuration dictionary.
        """
        return self.data

    def __str__(self):
        """Get a string representation of the configuration.

        Returns:
            str: The string representation of the configuration.
        """
        return self.cat_dict(self.data)

    def get(self, key, default=None):
        """A helper function for reading values from the config without
        a chain of `get()` calls.

        Usage:
            mongo_conn = conf.get('db.mongo.MONGO_CONNECTION_STRING')
            default_db = conf.get('default.db')
            az_credentials = conf.get('data.service.azure.credentials')

        Args:
            default
            key (str): A string representing the value's path in the config.
        """
        try:
            return self.__getitem__(key)
        except KeyError:
            if default is None:
                path = self.path
                Console.warning(
                    "The key '{key}' could not be found in the yaml file '{path}'".format(
                        **locals()))
                # sys.exit(1)
                raise KeyError(key)
            return default
        except Exception as e:
            print(e)
            sys.exit(1)

    def __setitem__(self, key, value):
        """Set the value for a specific key in the configuration.

        Args:
            key (str): The key for which to set the value.
            value: The value to set for the specified key.
        """
        self.set(key, value)

    def set(self, key, value):
        """A helper function for setting the default cloud in the config without
        a chain of `set()` calls.

        Usage:
            mongo_conn = conf.set('db.mongo.MONGO_CONNECTION_STRING',
                         "https://localhost:3232")

        Args:
            key (str): The key for which to set the value.
            value: The value to set for the specified key.
        """

        if value.lower() in ['true', 'false']:
            value = value.lower() == 'true'
        try:
            if "." in key:
                keys = key.split(".")
                #
                # create parents
                #
                parents = keys[:-1]
                location = self.data
                for parent in parents:
                    if parent not in location:
                        location[parent] = {}
                    location = location[parent]
                #
                # create entry
                #
                location[keys[len(keys) - 1]] = value
            else:
                self.data[key] = value

        except KeyError:
            path = self.path
            Console.error(
                "The key '{key}' could not be found in the yaml file '{path}'".format(
                    **locals()))
            sys.exit(1)
        except Exception as e:
            print(e)
            sys.exit(1)

        yaml_file = self.data.copy()
        with open(self.path, "w") as stream:
            yaml.safe_dump(yaml_file, stream, default_flow_style=False)

    def __getitem__(self, item):
        """gets an item form the dict. The key is . separated
        use it as follows get("a.b.c")

        Args:
            item (str): The item for which to retrieve the value.

        Returns:
            Any: The value for the specified item.
        """
        try:
            if "." in item:
                keys = item.split(".")
            else:
                return self.data[item]
            element = self.data[keys[0]]
            for key in keys[1:]:
                element = element[key]
        except KeyError:
            path = self.path
            Console.warning(
                "The key '{item}' could not be found in the yaml file '{path}'".format(
                    **locals()))
            raise KeyError(item)
            # sys.exit(1)
        except Exception as e:
            print(e)
            sys.exit(1)
        # if element.lower() in ['true', 'false']:
        #    element = element.lower() == 'true'
        return element

    def __delitem__(self, item):
        """Delete a specific item from the configuration.

        Args:
            item (str): The item to delete from the configuration.

        BUG: THIS DOES NOT WORK

            gets an item form the dict. The key is . separated
            use it as follows get("a.b.c")
        """
        try:
            if "." in item:
                keys = item.split(".")
            else:
                return self.data[item]
            element = self.data
            print(keys)
            for key in keys:
                element = element[key]
            del element
        except KeyError:
            path = self.path
            Console.error(
                "The key '{item}' could not be found in the yaml file '{path}'".format(
                    **locals()))
            sys.exit(1)
        except Exception as e:
            print(e)
            sys.exit(1)

    def search(self, key, value=None):
        """Search for items in the configuration based on a key and optional value.

        Args:
              key (str): The key to search for.
              value: The value to match (optional).

        Returns:
              dict: A dictionary containing the search results.

        Example:
              search("cloudmesh.cloud.*.cm.active", True)
        """
        flat = FlatDict(self.data, sep=".")
        result = flat.search(key, value)
        return result

    def edit(self, attribute):
        """Edit the dict specified by the attribute and fills out all TBD values.

        Args:
            attribute (string)

        Returns:

        """

        Console.ok("Filling out: {attribute}".format(attribute=attribute))

        try:
            config = Config()
            values = config[attribute]

            print("Editing the values for {attribute}"
                  .format(attribute=attribute))

            print("Current Values:")

            print(yaml.dump(values, indent=2))

            for key in values:
                if values[key] == "TBD":
                    result = input("Please enter new value for {key}: "
                                   .format(**locals()))
                    values[key] = result

            config.save()
        except Exception as e:
            print(e)
            Console.error(f"could not find the attribute '{attribute}' in the yaml file.")

    """
    @staticmethod
    def cat_dict(d,
                 mask_secrets=True,
                 attributes=None,
                 color=None):
        kluge = yaml.dump(d,
                          default_flow_style=False, indent=2)
        content = kluge.splitlines()

        return Config.cat_lines(content, mask_secrets=mask_secrets)
    """

    def cat_dict(self, d):
        """Get a string representation of a dictionary.

        Args:
            d (dict): The dictionary to represent as a string.

        Returns:
            str: A string representation of the dictionary.
        """
        kluge = yaml.dump(d,
                          default_flow_style=False, indent=2)
        content = kluge.splitlines()

        return self.cat_lines(content)

    def cat_lines(self, content):
        """Get a string representation of lines.

        Args:
            content (list): The list of lines to represent as a string.

        Returns:
            str: A string representation of the lines.
        """
        lines = '\n'.join(content)
        return lines

    def cat(self):
        """Get a string representation of the configuration.

         Returns:
             str: A string representation of the configuration.
         """

        _path = path_expand(self.path)
        with open(_path) as f:
            content = f.read().splitlines()
        return self.cat_lines(content)
