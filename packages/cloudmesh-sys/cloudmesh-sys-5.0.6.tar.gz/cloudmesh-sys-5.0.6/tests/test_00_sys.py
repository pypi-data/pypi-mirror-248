###############################################################
# pytest -v --capture=no tests/test_00_sys.py
# pytest -v  tests/test_00_sys.py
###############################################################

import pytest

from cloudmesh.common.Benchmark import Benchmark
from cloudmesh.common.Shell import Shell
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.util import HEADING
from cloudmesh.common.variables import Variables

Benchmark.debug()

variables = Variables()

cloud = 'local'


@pytest.mark.incremental
class Test_Sys:

    def test_cms_help(self):
        HEADING()

        Benchmark.Start()
        result = Shell.execute("cms help", shell=True)
        Benchmark.Stop()
        VERBOSE(result)
        assert 'sys' in result

    def test_benchmark(self):
        Benchmark.print(sysinfo=True, csv=True, tag=cloud)
