"""
Serial Bump Tests
"""
from typing import Any
from datetime import datetime
from pyconcurrent import run_prog
import pytest


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


def _today():
    """ date for serial """
    return datetime.today().date().strftime("%Y%m%d")


class TestSerialBump:
    """
    Hash test class
    """
    @pytest.fixture(scope="class")
    @classmethod
    def common(cls) -> dict[str, Any]:
        data: dict[str, str] = {'appdir': "../../src/dns_tools/apps"}
        return data

    def _init_test(self, common: dict[str, Any]):
        """
        Initialize with fresh config / zone files
        """
        pargs = ['./tools/test-init']
        (rc, _stdout, _stderr) = run_prog(pargs)
        assert rc == 0

    def test_serial_1(self, common: dict[str, Any]):
        """
        Check serial-1
        """
        appdir = common['appdir']
        pargs = [f'{appdir}/dns-serial-bump.py']
        pargs += ['--check', 'tools/serial-check-1.zone']
        (rc, stdout, _stderr) = run_prog(pargs)
        assert rc == 0

        target = _today() + '00'
        assert _check_result(stdout, target)

    def test_serial_2(self, common: dict[str, Any]):
        """
        Check serial-2
        """
        appdir = common['appdir']
        pargs = [f'{appdir}/dns-serial-bump.py']
        pargs += ['--check', 'tools/serial-check-2.zone']
        (rc, stdout, _stderr) = run_prog(pargs)
        assert rc == 0
        target = _today() + '00'
        assert _check_result(stdout, target)

    def test_serial_3(self, common: dict[str, Any]):
        """
        Check serial-3
        """
        appdir = common['appdir']
        pargs = [f'{appdir}/dns-serial-bump.py']
        pargs += ['--check', 'tools/serial-check-3.zone']
        (rc, stdout, _stderr) = run_prog(pargs)
        assert rc == 0
        target = _today() + '00'
        assert _check_result(stdout, target)
