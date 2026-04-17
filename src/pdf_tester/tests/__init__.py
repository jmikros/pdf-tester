# src/pdf_tester/tests/__init__.py
"""
Auto-discovery of all test modules.
New test_*.py files are automatically registered.
"""

import pkgutil
import importlib

# Automatically import all test modules
for _, module_name, _ in pkgutil.iter_modules(__path__):
    if not module_name.startswith("_"):
        try:
            importlib.import_module(f".{module_name}", __package__)
        except Exception as e:
            import warnings
            warnings.warn(f"Failed to load test module '{module_name}': {e}")