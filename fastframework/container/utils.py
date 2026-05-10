import importlib
from glob import glob
from os import path


def get_modules(package_path: str) -> list[str]:
    """Returns a list of full paths of the modules in a given package."""

    pattern = "**/*.py"
    files = [f for f in glob(path.join(package_path, pattern), recursive=True)]

    return files


def get_classes(modules: list[str], class_suffix: str = "") -> list[type]:
    """Imports and returns a list of classes with the given name from the specified modules."""

    classes: list[type] = []

    for module in modules:
        module = module.replace("\\", "/").replace("/", ".").replace(".py", "")
        class_module = importlib.import_module(module)
        class_name = module.split(".")[-1].capitalize() + class_suffix
        classes.append(getattr(class_module, class_name))

    return classes
