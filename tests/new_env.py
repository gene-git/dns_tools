"""
Hash Tests

Please set PYTHONPATH.
"""
from typing import (Dict)
import os


def get_new_env() -> Dict[str, str]:
    """
    Update PATH to include PYTHONPATH

    Ensures the source version of tools are used
    """
    env = os.environ.copy()
    python_path = env.get('PYTHONPATH')
    if python_path:
        env['PATH'] = python_path + ':' + env['PATH']
    return env
