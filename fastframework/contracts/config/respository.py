from abc import ABC, abstractmethod
from typing import Any

from fastframework.config.base_config import BaseConfig


class ConfigRepositoryInterface(ABC):
    @abstractmethod
    def has(self, name: str) -> bool:
        """Determine if the given configuration value exists."""
        pass

    @abstractmethod
    def get(self, name: str, default: Any | None = None) -> Any | None:
        """Get the specified configuration value."""
        pass

    @abstractmethod
    def all(self) -> dict[str, Any]:
        """Get all of the configuration items for the application."""
        pass

    @abstractmethod
    def set(self, name: str, value: Any) -> None:
        """Set a given configuration value."""
        pass

    @abstractmethod
    def set_all(self, items: dict[str, Any] | BaseConfig) -> None:
        """Set multiple configuration values."""
        pass

    @abstractmethod
    def string(self, name: str, default: str | None = None) -> str | None:
        """Get the specified configuration value as a string."""
        pass

    @abstractmethod
    def integer(self, name: str, default: int | None = None) -> int | None:
        """Get the specified configuration value as an integer."""
        pass

    @abstractmethod
    def float(self, name: str, default: float | None = None) -> float | None:
        """Get the specified configuration value as a float."""
        pass

    @abstractmethod
    def boolean(self, name: str, default: bool | None = None) -> bool | None:
        """Get the specified configuration value as a boolean."""
        pass
