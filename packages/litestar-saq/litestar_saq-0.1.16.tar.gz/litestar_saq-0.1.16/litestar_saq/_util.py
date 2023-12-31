from __future__ import annotations

import importlib.util
import sys
from functools import lru_cache
from importlib import import_module
from pathlib import Path
from typing import TYPE_CHECKING, Any

__all__ = ["import_string", "module_to_os_path"]


if TYPE_CHECKING:
    from types import ModuleType


@lru_cache
def module_to_os_path(dotted_path: str) -> Path:
    """Find Module to OS Path.

    Return path to the base directory of the project or the module
    specified by `dotted_path`.

    Ensures that pkgutil returns a valid source file loader.
    """
    src = importlib.util.find_spec(dotted_path)
    if src is None:
        msg = f"Couldn't find the path for {dotted_path}"
        raise TypeError(msg)
    return Path(str(src.origin).removesuffix("/__init__.py"))  # type: ignore[unreachable]


def import_string(dotted_path: str) -> Any:
    """Dotted Path Import.

    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.

    Args:
        dotted_path (str): The path of the module to import.

    Raises:
        ImportError: Could not import the module.

    Returns:
        object: The imported object.
    """
    try:
        module_path, class_name = dotted_path.rsplit(".", 1)
    except ValueError as e:
        msg = f"{dotted_path} doesn't look like a module path"
        raise ImportError(msg) from e

    try:
        return _cached_import(module_path, class_name)
    except AttributeError as e:
        msg = f"Module '{module_path}' does not define a '{class_name}' attribute/class"
        raise ImportError(msg) from e


def _is_loaded(module: ModuleType | None) -> bool:
    spec = getattr(module, "__spec__", None)
    initializing = getattr(spec, "_initializing", False)
    return bool(module and spec and not initializing)


def _cached_import(module_path: str, class_name: str) -> Any:
    """Import and cache a class from a module.

    Args:
        module_path (str): dotted path to module.
        class_name (str): Class or function name.

    Returns:
        object: The imported class or function
    """
    # Check whether module is loaded and fully initialized.
    module = sys.modules.get(module_path)
    if not _is_loaded(module):
        module = import_module(module_path)
    return getattr(module, class_name)
