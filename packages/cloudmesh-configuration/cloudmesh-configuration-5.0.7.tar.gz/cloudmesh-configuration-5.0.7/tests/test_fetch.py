###############################################################
# pytest -v --capture=no tests/1_local/test_fetch.py
# pytest -v  tests/1_local/test_fetch.py
# pytest -v --capture=no  tests/1_local/test_fetch..py::Test_fetch::<METHODNAME>
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
        path = Path("~/.cloudmesh/pytest-test.yaml")
        config = Config()
        config.fetch(destination=path)
        assert not path.is_file()
