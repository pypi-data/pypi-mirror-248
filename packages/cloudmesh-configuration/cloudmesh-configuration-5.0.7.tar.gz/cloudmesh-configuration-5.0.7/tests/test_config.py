###############################################################
# pytest -v --capture=no tests/test_config.py
# pytest -v  tests/test_config.py
# pytest -v --capture=no  tests/test_config..py::Test_config::<METHODNAME>
###############################################################
import os
import textwrap
from pathlib import Path
from pprint import pprint

import oyaml as yaml
import pytest
from cloudmesh.common.StopWatch import StopWatch
from cloudmesh.common.util import HEADING
from cloudmesh.common.util import path_expand
from cloudmesh.common.StopWatch import StopWatch
from cloudmesh.configuration.Config import Config
from shutil import copyfile


@pytest.mark.incremental
class TestConfig:


    def test_create_backup(self):
        path = Path("~/.cloudmesh/cloudmesh.yaml")
        if path.is_file():
            backup = Path("~/.cloudmesh/cloudmesh.yaml-pytest")
            copyfile(path, backup)
            os.remove(path)
            assert not path.is_file()
            assert backup.is_file()


    def config_n_load(self, n):
        config = [None] * n
        StopWatch.start("test_config_load n={n}".format(**locals()))
        for i in range(1, n):
            config[i] = Config()
            pprint (config[i])
        StopWatch.stop("test_config_load n={n}".format(**locals()))

    def test_config(self):
        print ()
        for n in range(1, 10):
            self.config_n_load(n)
            n_1 = StopWatch.get("test_config_load n=1")
            n_n = StopWatch.get("test_config_load n={n}".format(**locals()))
            print (n, n_1 >= n_n, n_1, n_n, n_1 - n_n)

        n_1 = StopWatch.get("test_config_load n=1")
        n_n = StopWatch.get("test_config_load n=9")


    def test_search(self):
        config = Config()

        StopWatch.start("search")
        r = config.search("cloudmesh.cloud.*.cm.active", True)
        StopWatch.stop("search")
        pprint (r)

    def test_dict(self):
        HEADING()
        config = Config()
        StopWatch.start("dict")
        result = config.dict()
        StopWatch.stop("dict")
        pprint(result)
        print(config)
        print(type(config.data))

        assert config is not None

    def test_config_subscriptable(self):
        HEADING()
        config = Config()
        StopWatch.start("config_subscriptable")
        data = config["cloudmesh"]["data"]["mongo"]
        StopWatch.stop("config_subscriptable")
        assert data is not None

    def test_dictreplace(self):
        HEADING()
        config = Config()
        spec = textwrap.dedent("""
        cloudmesh:
          profile:
            name: Gregor
          unordered:
            name: "{cloudmesh.other.name}.postfix"
          other:
            name: "{cloudmesh.profile.name}"
        
        """)

        print(spec)

        # spec = spec.replace("{", "{{")
        # spec = spec.replace("}", "}}")

        # print(spec)
        StopWatch.start("dictreplace")
        result = config.spec_replace(spec)
        StopWatch.stop("dictreplace")
        print(result)
        data = yaml.load(result, Loader=yaml.SafeLoader)
        pprint(data)

        assert data["cloudmesh"]["unordered"]["name"] == "Gregor.postfix"
        assert data["cloudmesh"]["other"]["name"] == "Gregor"

    def test_configreplace(self):
        HEADING()
        config = Config()
        pprint(config["cloudmesh"]["profile"])

    def test_if_yaml_file_exists(self):
        config = Config()
        config.create()
        filename = path_expand("~/.cloudmesh/cloudmesh.yaml")
        assert os.path.isfile(Path(filename))

    def test_set(self):
        StopWatch.start("set")
        config = Config()
        config["cloudmesh.test.nested"] = "Gregor"
        StopWatch.stop("set")
        print(config["cloudmesh.test.nested"])
        assert config["cloudmesh.test.nested"] == "Gregor"

    ''' THIS TEST DOES FAIL
    def test_del(self):
        del config["cloudmesh.test.nested"]

        assert config["cloudmesh.test.nested"] != "Gregor"
    '''
    def test_restore_backup(self):
        backup = Path("~/.cloudmesh/cloudmesh.yaml-pytest")
        if backup.is_file():
            path = Path("~/.cloudmesh/cloudmesh.yaml")
            os.remove(backup)
            copyfile(path, backup)


    def test_getitem(self):
        config = Config()
        key = "cloudmesh.version"
        StopWatch.start(f"config[{key}]")
        value = config[key]
        StopWatch.stop(f"config[{key}]")
        assert  value is not None

    def test_get(self):
        config = Config()
        key = "cloudmesh.version"
        StopWatch.start(f"get({key})")
        value = config[key]
        StopWatch.stop(f"get({key})")
        assert  value is not None

    def test_doesnotexist_get(self):
        config = Config()

        key = "cloudmesh.doesnotexist"
        StopWatch.start(f"not exists get({key})")
        value = config.get(key, default="Hallo")
        StopWatch.stop(f"not exists get({key})")

        assert value == "Hallo"

    def test_doesnotexist_getitem(self):
        config = Config()
        key = "cloudmesh.doesnotexist"
        StopWatch.start(f"not exists [{key}]")
        try:
            value = config[key]
            keyerror = False
        except KeyError:
            keyerror = True
        StopWatch.stop(f"not exists [{key}]")

        assert keyerror


    def test_StopWatch(self):
        StopWatch.benchmark(sysinfo=False)
