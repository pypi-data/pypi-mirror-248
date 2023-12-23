###############################################################
# npytest -v --capture=no  tests/test_catalog.py::Test_data.test_001_help
# pytest -v --capture=no  tests/test_catalog.py
# pytest -v tests/test_catalog.py
###############################################################

import os
import pytest
from cloudmesh.common.Shell import Shell
from cloudmesh.common.util import HEADING
#from cloudmesh.data.create import ascii_file
#from cloudmesh.data.create import random_file


@pytest.mark.incremental
class Test_catalog(object):

    def setup(self):
        self.size = "1GB"

    def test_001_help(self):
        HEADING()
        r = Shell.run("cms catalog")
        print(r)
        assert "Usage:" in r
        assert "catalog copy" in r
        assert "ERROR: Could not execute the command." in r

    def test_001_start(self):
        HEADING()
        r = Shell.run("cms catalog start")
        r = Shell.run("cms catalog info")
        assert "True" in r
        r = Shell.run("curl localhost:8001")
        assert "running" in r

    def test_002_info(self):
        HEADING()
        r = Shell.run("cms catalog info")
        assert "True" in r
        r = Shell.run("curl localhost:8001")
        assert "running" in r

    def test_003_stop(self):
        HEADING()
        r = Shell.run("cms catalog stop")
        r = Shell.run("cms catalog info")
        assert "'pid': None" in r
        r = Shell.run("curl localhost:8001")
        assert "running" not in r


class rest:

    def test_002_create_database(self):
        HEADING()
        # here you create a test directory with data
        raise None


    def test_005_load(self):
        HEADING()
        # here you load all data from a directory
        raise NotImplementedError

    def test_006_query(self):
        HEADING()
        # here you query all data from a directory
        raise NotImplementedError

    def test_007_start(self):
        HEADING()
        # here you create the stop test of the server
        raise NotImplementedError

    # other tests

    def test_100_cleanup(self):
        HEADING()
        # here you do the cleanup
        raise NotImplementedError
