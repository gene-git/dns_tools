"""
 run_prog.py

 Run program return status and stdout and stderr

"""
# pylint: disable=subprocess-run-check
from typing import (Any)
import subprocess


def run_prog(pargs: list[str], env: dict[str, str] | None
             ) -> tuple[int, str, str]:
    """
    run external program using subprocess
        pargs = [cmd, arg1, arg2, ... ]
    """
    retc = 0
    output = ''
    errors = ''

    run_args: dict[str, Any] = {
            'stdout': subprocess.PIPE,
            'stderr': subprocess.PIPE,
            'text': True,
            'check': False,
            }
    if env:
        run_args['env'] = env

    if pargs and pargs != []:
        try:
            ret = subprocess.run(pargs, **run_args)
            retc = ret.returncode
            output = ret.stdout
            errors = ret.stderr

        except subprocess.CalledProcessError:
            retc = -1
            errors = f'Error running: {pargs}'

        except FileNotFoundError:
            retc = -1
            errors = f'Error: file not found {pargs[0]}'

    return (retc, output, errors)
