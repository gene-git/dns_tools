"""
Tests:
    - Hash
    - Moving to production
    - DNS server restart

Please set PYTHONPATH=../src/dns_tools
"""
from subprocess import CalledProcessError
import pytest

from .run_prog import run_prog
from .new_env import get_new_env

ENV = get_new_env()


@pytest.fixture(scope='session', autouse=True)
def setup_cleanup():
    """
    Setup before tests run
    Clean up after tests completed
    """
    pargs = ['./tools/test-init']
    (rc, _stdout, stderr) = run_prog(pargs, env=ENV)
    if rc != 0:
        raise CalledProcessError(-1, pargs, stderr)
    yield

    pargs = ['./tools/test-clean']
    (rc, _stdout, _stderr) = run_prog(pargs, env=ENV)
    if rc != 0:
        raise CalledProcessError(-1, pargs, stderr)


class TestTool:
    """
    Hash test class
    """
    def test_make_keys(self):
        """
        Generate ksk and zsk
        """
        pargs = ['dns-tool.py']
        pargs += ['--gen-ksk-curr', '--gen-zsk-curr']
        (rc, stdout, _stderr) = run_prog(pargs, env=ENV)
        assert rc == 0
        assert 'Success: all done' in stdout

    def test_sign(self):
        """
        Roll keys phase 1
        """
        pargs = ['dns-tool.py']
        pargs += ['--sign']
        (rc, stdout, _stderr) = run_prog(pargs, env=ENV)
        assert rc == 0
        assert 'Success: all done' in stdout

    def test_roll_1(self):
        """
        Roll keys phase 1
        """
        pargs = ['dns-tool.py']
        pargs += ['--zsk-roll-1']
        (rc, stdout, _stderr) = run_prog(pargs, env=ENV)
        assert rc == 0
        assert 'Success: all done' in stdout

    def test_roll_2(self):
        """
        Roll keys phase 2
        """
        pargs = ['dns-tool.py']
        pargs += ['--zsk-roll-2']
        (rc, stdout, _stderr) = run_prog(pargs, env=ENV)
        assert rc == 0
        assert 'Success: all done' in stdout

    def test_to_production(self):
        """
        push to production
        """
        pargs = ['dns-prod-push.py']
        pargs += ['--to-production']
        (rc, stdout, _stderr) = run_prog(pargs, env=ENV)
        assert rc == 0
        assert 'Success: all done' in stdout

    def test_restart_dns_servers(self):
        """
        Restart DNS servers
        """
        pargs = ['dns-prod-push.py']
        pargs += ['--dns-restart']
        (rc, stdout, _stderr) = run_prog(pargs, env=ENV)
        assert rc == 0
        assert 'Success: all done' in stdout
