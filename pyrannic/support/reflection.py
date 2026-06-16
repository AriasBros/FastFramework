from abc import ABC
from inspect import isclass
from types import get_original_bases
from typing import get_args


def is_interface(cls: object) -> bool:
    return isclass(cls) and ABC in cls.__bases__


def get_generic_type(instance_or_class: object | type, generic_index: int = 0) -> type:
    classes = get_original_bases(type(instance_or_class))
    args = get_args(classes[generic_index])
    size = len(args)

    if size == 0:
        raise ValueError(
            f"Generic type not found for {instance_or_class.__class__.__name__} at index {generic_index}"  # type: ignore
        )

    return args[0]
