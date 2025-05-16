"""
Serial Bump Tests

Please set PYTHONPATH=../src/dns_tools
"""
from .run_prog import run_prog
from .new_env import get_new_env


ENV = get_new_env()


def _check_result(stdout: str, target: str) -> bool:
    """
    Confirm that "New Serial" = target
    Return True if correct
    """
    if not stdout:
        return False
    rows = stdout.splitlines()
    for row in rows:
        row = row.strip()
        if row.startswith('New Serial = '):
            words = row.split('=')
            if len(words) == 2:
                serial = words[1].strip()
                if serial == target:
                    return True
    return False


class TestSerialBump:
    """
    Hash test class
    """
    def _init_test(self):
        """
        Initialize with fresh config / zone files
        """
        pargs = ['./tools/test-init']
        (rc, _stdout, _stderr) = run_prog(pargs, env=ENV)
        assert rc == 0

    def test_serial_1(self):
        """
        Check serial-1
        """
        pargs = ['dns-serial-bump.py']
        pargs += ['--check', 'tools/serial-check-1.zone']
        (rc, stdout, _stderr) = run_prog(pargs, env=ENV)
        assert rc == 0
        assert _check_result(stdout, '2025051600')

    def test_serial_2(self):
        """
        Check serial-2
        """
        pargs = ['dns-serial-bump.py']
        pargs += ['--check', 'tools/serial-check-2.zone']
        (rc, stdout, _stderr) = run_prog(pargs, env=ENV)
        assert rc == 0
        assert _check_result(stdout, '2025051600')

    def test_serial_3(self):
        """
        Check serial-3
        """
        pargs = ['dns-serial-bump.py']
        pargs += ['--check', 'tools/serial-check-3.zone']
        (rc, stdout, _stderr) = run_prog(pargs, env=ENV)
        assert rc == 0
        assert _check_result(stdout, '2025051700')
