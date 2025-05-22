# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
 run external program
 args:  ['program_pat', 'arg1', 'arg2', ...]
"""
# pylint: disable=too-many-arguments,too-many-positional-arguments
import subprocess


def run_prog(pargs: list[str],
             input_str: str | None = None,
             stdout: int = subprocess.PIPE,
             stderr: int = subprocess.PIPE,
             test: bool = False,
             verb: bool = False) -> tuple[int, str, str]:
    """
    Run external program using subprocess.

    Returns:
        tuple(retc: int, stdout: str, stderrr: str)
    """
    if not pargs:
        return (0, '', '')

    if test:
        cmdline = ' '.join(pargs)
        if verb:
            print(f'{cmdline}')
        return (0, '', '')

    bstring = None
    if input_str:
        bstring = bytearray(input_str, 'utf-8')

    ret = subprocess.run(pargs, input=bstring,
                         stdout=stdout, stderr=stderr, check=False)

    retc = ret.returncode
    output = ''
    errors = ''

    if ret.stdout:
        output = str(ret.stdout, 'utf-8', errors='ignore')

    if ret.stderr:
        errors = str(ret.stderr, 'utf-8', errors='ignore')

    return (retc, output, errors)
