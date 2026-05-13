from abc import ABC, abstractmethod
from typing import Any

from annotated_types import T


class ConfigRepositoryInterface(ABC):
    @abstractmethod
    def has(self, name: str) -> bool:
        """Determine if the given configuration value exists."""
        pass

    @abstractmethod
    def get(self, name: str, default: Any | None = None) -> object | None:
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
    def string(self, name: str, default: str = "") -> str:
        """Get the specified configuration value as a string."""
        pass

    @abstractmethod
    def integer(self, name: str, default: int = 0) -> int:
        """Get the specified configuration value as an integer."""
        pass

    @abstractmethod
    def float(self, name: str, default: float = 0.0) -> float:
        """Get the specified configuration value as a float."""
        pass

    @abstractmethod
    def boolean(self, name: str, default: bool = False) -> bool:
        """Get the specified configuration value as a boolean."""
        pass

    @abstractmethod
    def array(self, name: str, default: list[T]) -> list[T]:
        """Get the specified configuration value as a list."""
        pass
