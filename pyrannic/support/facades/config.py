from typing import Any

from annotated_types import T

from pyrannic.contracts.config.respository import ConfigRepositoryInterface
from pyrannic.support.facades.facade import Facade


class Config(Facade[ConfigRepositoryInterface]):
    @classmethod
    def _get_facade_accessor(cls) -> str:
        return "config"

    @classmethod
    def get(cls, name: str, default: Any | None = None) -> object | None:
        """Get the specified configuration value."""
        return cls.call("get", name, default)

    @classmethod
    def string(cls, name: str, default: str = "") -> str:
        """Get the specified configuration value as a string."""
        return cls.call("string", name, default)

    @classmethod
    def integer(cls, name: str, default: int = 0) -> int:
        """Get the specified configuration value as an integer."""
        return cls.call("integer", name, default)

    @classmethod
    def float(cls, name: str, default: float = 0.0) -> float:
        """Get the specified configuration value as a float."""
        return cls.call("float", name, default)

    @classmethod
    def boolean(cls, name: str, default: bool = False) -> bool:
        """Get the specified configuration value as a boolean."""
        return cls.call("boolean", name, default)

    @classmethod
    def array(cls, name: str, default: list[T] = []) -> list[T]:
        """Get the specified configuration value as a list."""
        return cls.call("array", name, default)

    @classmethod
    def optional_string(cls, name: str, default: str | None = None) -> str | None:
        """Get the specified configuration value as a string."""
        return cls.call("optional_string", name, default)

    @classmethod
    def optional_integer(cls, name: str, default: int | None = None) -> int | None:
        """Get the specified configuration value as an integer."""
        return cls.call("optional_integer", name, default)

    @classmethod
    def optional_float(cls, name: str, default: float | None = None) -> float | None:
        """Get the specified configuration value as a float."""
        return cls.call("optional_float", name, default)

    @classmethod
    def optional_boolean(cls, name: str, default: bool | None = None) -> bool | None:
        """Get the specified configuration value as a boolean."""
        return cls.call("optional_boolean", name, default)

    @classmethod
    def optional_array(
        cls,
        name: str,
        default: list[T] | None = None,
    ) -> list[T] | None:
        """Get the specified configuration value as a list."""
        return cls.call("optional_array", name, default)
