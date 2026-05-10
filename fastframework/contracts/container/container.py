from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any


class ContainerInterface(ABC):
    @abstractmethod
    def bind(
        self,
        abstract: str | type,
        concrete: type[Any] | Callable[..., Any],
    ) -> None:
        pass

    @abstractmethod
    def is_bound(self, abstract: str | type) -> bool:
        pass

    @abstractmethod
    def resolve(self, abstract: str | type) -> Any:
        pass

    @abstractmethod
    def resolved(self, abstract: str | type) -> bool:
        """Determine if the given abstract type has been resolved."""
        pass

    @abstractmethod
    def set_alias(self, abstract: str | type, alias: str | type) -> None:
        """Alias a type to a different one."""
        pass

    @abstractmethod
    def is_alias(self, alias: str | type) -> bool:
        """Determine if a given string/type is an alias."""
        pass

    @abstractmethod
    def flush(self) -> None:
        """Flush the container of all bindings and resolved instances."""
        pass
