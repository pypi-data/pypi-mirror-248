###############################################################
# pytest -v --capture=no tests/test_progress.py
# pytest -v  tests/test_progress.py
# pytest -v --capture=no  tests/test_progress.py::Test_cmsd::<METHODNAME>
# pytest -v --capture=no  tests/test_progress.py::TestCmsd::test_vm_list_json
###############################################################
import pytest
from cloudmesh.common.StopWatch import StopWatch
from cloudmesh.common.Shell import Shell
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.util import HEADING
from cloudmesh.common.util import readfile
from cloudmesh.common.Benchmark import Benchmark

Benchmark.debug()


@pytest.mark.incremental
class TestProgress:

    def test_progress_0(self):
        HEADING()
        result = Shell.run("cms progress 0")
        print(result)
        assert "progress=0" in result

    def test_progress_50(self):
        HEADING()
        result = Shell.run("cms progress 50")
        print(result)
        assert "progress=50" in result

    def test_progress_now(self):
        HEADING()
        result = Shell.run("cms progress 50 --now")
        print(result)
        assert "progress=50" in result
        assert "time='" in result

    def test_progress_status(self):
        HEADING()
        result = Shell.run("cms progress 50 --status=undefined")
        print(result)
        assert "progress=50" in result
        assert "status=undefined" in result

    def test_progress_values(self):
        HEADING()
        result = Shell.run("cms progress 50 a=10 b=text c=\"{d:1}\"")
        print(result)
        assert "progress=50" in result

    def test_progress_banner(self):
        HEADING()
        result = Shell.run("cms progress 50 a=10 b=text c=\"{d:1}\" --banner")
        print(result)
        assert "progress=50" in result
