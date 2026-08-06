"""Test bootstrap.

Registers lightweight stand-in package modules for
``custom_components`` and ``custom_components.purc_tariff`` so that
``purc_client.py`` (and its relative imports of ``const``/``exceptions``)
can be imported without executing ``custom_components/purc_tariff/__init__.py``,
which requires the ``homeassistant`` package to be installed.
"""

import sys
import types
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
COMPONENTS_DIR = ROOT_DIR / "custom_components"
INTEGRATION_DIR = COMPONENTS_DIR / "purc_tariff"

if "custom_components" not in sys.modules:
    stub = types.ModuleType("custom_components")
    stub.__path__ = [str(COMPONENTS_DIR)]
    sys.modules["custom_components"] = stub

if "custom_components.purc_tariff" not in sys.modules:
    stub = types.ModuleType("custom_components.purc_tariff")
    stub.__path__ = [str(INTEGRATION_DIR)]
    sys.modules["custom_components.purc_tariff"] = stub
