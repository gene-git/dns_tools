"""
Tests:
    - Hash
    - Moving to production
    - DNS server restart
"""
from typing import Any
from subprocess import CalledProcessError
import pytest

from pyconcurrent import run_prog



@pytest.fixture(scope='session', autouse=True)
def setup_cleanup():
    """
    Setup before tests run
    Clean up after tests completed
    """
    pargs = ['./tools/test-init']
    (rc, _stdout, stderr) = run_prog(pargs)     # , env=ENV)
    if rc != 0:
        raise CalledProcessError(-1, pargs, stderr)
    yield

    pargs = ['./tools/test-clean']
    (rc, _stdout, _stderr) = run_prog(pargs)        # , env=ENV)
    if rc != 0:
        raise CalledProcessError(-1, pargs, stderr)


class TestTool:
    """
    Hash test class
    """
    @pytest.fixture(scope="class")
    @classmethod
    def common(cls) -> dict[str, Any]:
        data: dict[str, str] = {'appdir': "../../src/dns_tools/apps"}
        return data

    def test_make_keys(self, common: dict[str, Any]):
        """
        Generate ksk and zsk
        """
        appdir = common['appdir']
        pargs = [f'{appdir}/dns-tool.py']
        pargs += ['--gen-ksk-curr', '--gen-zsk-curr']
        (rc, stdout, _stderr) = run_prog(pargs)     # , env=ENV)
        assert rc == 0
        assert 'Success: all done' in stdout

    def test_sign(self, common: dict[str, Any]):
        """
        Roll keys phase 1
        """
        appdir = common['appdir']
        pargs = [f'{appdir}/dns-tool.py']
        pargs += ['--sign']
        (rc, stdout, _stderr) = run_prog(pargs)     # , env=ENV)
        assert rc == 0
        assert 'Success: all done' in stdout

    def test_serial_bump(self, common: dict[str, Any]):
        """
        Roll keys phase 1
        """
        appdir = common['appdir']
        pargs = [f'{appdir}/dns-tool.py']
        pargs += ['--serial-bump']
        (rc, stdout, _stderr) = run_prog(pargs)     # , env=ENV)
        assert rc == 0
        assert 'Success: all done' in stdout

    def test_serial_bump_sign(self, common: dict[str, Any]):
        """
        Roll keys phase 1
        """
        appdir = common['appdir']
        pargs = [f'{appdir}/dns-tool.py']
        pargs += ['--serial-bump', '--sign']
        (rc, stdout, _stderr) = run_prog(pargs)     # , env=ENV)
        assert rc == 0
        assert 'Success: all done' in stdout

    def test_roll_1(self, common: dict[str, Any]):
        """
        Roll keys phase 1
        """
        appdir = common['appdir']
        pargs = [f'{appdir}/dns-tool.py']
        pargs += ['--zsk-roll-1']
        (rc, stdout, _stderr) = run_prog(pargs)     # , env=ENV)
        assert rc == 0
        assert 'Success: all done' in stdout

    def test_roll_2(self, common: dict[str, Any]):
        """
        Roll keys phase 2
        """
        appdir = common['appdir']
        pargs = [f'{appdir}/dns-tool.py']
        pargs += ['--zsk-roll-2']
        (rc, stdout, _stderr) = run_prog(pargs)     # , env=ENV)
        assert rc == 0
        assert 'Success: all done' in stdout

    def test_to_production(self, common: dict[str, Any]):
        """
        push to production
        """
        appdir = common['appdir']
        pargs = [f'{appdir}/dns-prod-push.py']
        pargs += ['--to-production']
        (rc, stdout, _stderr) = run_prog(pargs)     # , env=ENV)
        assert rc == 0
        assert 'Success: all done' in stdout

    def test_restart_dns_servers(self, common: dict[str, Any]):
        """
        Restart DNS servers
        """
        appdir = common['appdir']
        pargs = [f'{appdir}/dns-prod-push.py']
        pargs += ['--dns-restart']
        (rc, stdout, _stderr) = run_prog(pargs)     # , env=ENV)
        assert rc == 0
        assert 'Success: all done' in stdout
