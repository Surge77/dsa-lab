"""
Pytest configuration.

Two jobs:

1. Put the repository root on sys.path, so `python -m pytest` works from a clean
   checkout with no install step and no PYTHONPATH fiddling — which matters for a
   study repo you come back to after months away.

2. Honour DSA_DRILL_SUBSTITUTE, which lets `drill.py --check` run a topic's real
   test file against *your* implementation instead of the reference one.
"""

import importlib.util
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
SUBSTITUTE_ENV = "DSA_DRILL_SUBSTITUTE"

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def _install_substitute(spec: str) -> None:
    """
    Register a file as though it were an existing module.

    `spec` is "dotted.module.name=/path/to/attempt.py". Pre-loading it into
    sys.modules means a test that does `from Linear.stack import Stack` gets the
    drill attempt, with no change to the test file itself.
    """
    module_name, _, path_text = spec.partition("=")
    module_name, path = module_name.strip(), Path(path_text.strip())

    if not module_name or not path.exists():
        raise RuntimeError(f"{SUBSTITUTE_ENV} is malformed or points at a missing file: {spec!r}")

    module_spec = importlib.util.spec_from_file_location(module_name, path)
    if module_spec is None or module_spec.loader is None:
        raise RuntimeError(f"cannot load {path} as {module_name}")

    module = importlib.util.module_from_spec(module_spec)
    # Registering before exec_module lets the attempt import itself if it must.
    sys.modules[module_name] = module
    module_spec.loader.exec_module(module)


_substitute = os.environ.get(SUBSTITUTE_ENV)
if _substitute:
    _install_substitute(_substitute)
