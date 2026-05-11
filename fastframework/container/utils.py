import importlib
from collections.abc import Callable
from glob import glob
from inspect import getmembers, isfunction
from os import path
from types import ModuleType
from typing import Any


def get_modules(package_path: str) -> list[str]:
    """Returns a list of full paths of the modules in a given package."""

    pattern = "**/*.py"
    files = [f for f in glob(path.join(package_path, pattern), recursive=True)]

    return files


def import_modules(package_path: str):
    """Imports a list of modules in a given package."""

    modules = get_modules(package_path)

    for module in modules:
        module_path = module.replace("\\", "/").replace("/", ".").replace(".py", "")
        module = importlib.import_module(module_path)

        yield module_path, module


def _get_attr(module: ModuleType, attr_name: str, default: Any = None) -> Any:
    try:
        return getattr(module, attr_name, default)
    except AttributeError:
        return default


def get_attr(module: str, attr_name: str, default: Any = None) -> Any:
    """Imports and returns the specified attribute from the given module."""

    module = module.replace("\\", "/").replace("/", ".").replace(".py", "")
    imported_module = importlib.import_module(module)

    return _get_attr(imported_module, attr_name, default)


def get_attrs(modules: list[str], attr_name: str) -> list[Any]:
    """Imports and returns a list of attrs with the given name from the specified modules."""

    attrs: list[Any] = []

    for module in modules:
        attr = get_attr(module, attr_name)

        if attr is not None:
            attrs.append(attr)

    return attrs


def get_class(
    module: ModuleType,
    *,
    module_path: str | None = None,
    class_name: str | None = None,
    class_suffix: str = "",
) -> Any:
    """Returns the specified class from the given module."""

    if module_path is not None:
        class_name = module_path.split(".")[-1].capitalize() + class_suffix
    elif class_name is None:
        raise ValueError("Either module_path or class_name must be provided")

    return _get_attr(module, class_name)


def get_classes(modules: list[str], class_suffix: str = "") -> list[type]:
    """Imports and returns a list of classes with the given name from the specified modules."""

    classes: list[type] = []

    for module in modules:
        module = module.replace("\\", "/").replace("/", ".").replace(".py", "")
        imported_module = importlib.import_module(module)

        class_ = get_class(
            imported_module,
            module_path=module,
            class_suffix=class_suffix,
        )

        if class_ is not None:
            classes.append(class_)

    return classes


def get_functions(
    module: ModuleType,
    predicate: Callable[[str], bool] | None = None,
) -> list[tuple[str, Any]]:
    return getmembers(
        module,
        lambda member: (
            isfunction(member) and (predicate(member.__name__) if predicate else True)
        ),
    )
