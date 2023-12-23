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
from cloudmesh.common.Benchmark import Benchmark

from cloudmesh.configuration.Config import Location
from shutil import copyfile



@pytest.mark.incremental
class TestConfig:

    def test_location(self):
        HEADING()
        Benchmark.Start()
        a = Location()
        print(a.get())
        assert ".cloudmesh" in a.get()

        b = Location()
        b.set("a")
        Benchmark.Stop()

        print(a.get(), a)
        print(b.get(), b)

        assert a.get() == "a"
        assert b.get() == "a"

    def test_equal(self):
        HEADING()
        Benchmark.Start()
        location = Location()
        Benchmark.Stop()
        assert location == "a"

    def test_environment(self):
        HEADING()
        Benchmark.Start()
        location = Location()
        location.environment("DOESNOTEXIST")
        Benchmark.Stop()
        print(location.get())
        assert location is None

    def test_environment(self):
        HEADING()
        os.environ["USE_THIS"] = "use_this"
        Benchmark.Start()
        location = Location()
        location.environment("USE_THIS")
        assert location.get() == "use_this"
        print(location.get())
        Benchmark.Stop()
        del os.environ['USE_THIS']

    def test_environment_os(self):
        HEADING()
        os.environ["USE_THIS"] = "use_this"
        Benchmark.Start()
        location = Location(directory="~/.cloudmesh")
        location.environment("USE_THIS")
        assert location.get() == "use_this"
        print(location.get())
        Benchmark.Stop()
        del os.environ['USE_THIS']

    def test_key(self):
        HEADING()
        Benchmark.Start()
        location = Location()
        assert location.key == "CLOUDMESH_CONFIG_DIR"
        Benchmark.Stop()


    def test_StopWatch(self):
        StopWatch.benchmark(sysinfo=False)
