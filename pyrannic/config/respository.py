from typing import Any

from annotated_types import T

from pyrannic.support.collections.dot_dict import get, has, set
from pyrannic.contracts.config.respository import ConfigRepositoryInterface


class ConfigRepository(ConfigRepositoryInterface):
    _items: dict[str, Any] = {}

    def __init__(self, items: dict[str, Any] = dict()) -> None:
        self._items = items

    def __getattr__(self, name: str, default: Any = None) -> Any:
        return get(self._items, name, default)

    def __hasattr__(self, name: str) -> bool:
        return has(self._items, name)

    def has(self, name: str) -> bool:
        return has(self._items, name)

    def get(self, name: str, default: Any | None = None) -> Any | None:
        return get(self._items, name, default)

    def all(self) -> dict[str, Any]:
        return dict(self._items)

    def set(self, name: str, value: Any) -> None:
        set(self._items, name, value)

    def optional_string(self, name: str, default: str | None = None) -> str | None:
        value = self.get(name, default)
        return str(value) if value is not None else default

    def string(self, name: str, default: str = "") -> str:
        return self.optional_string(name, default) or default

    def integer(self, name: str, default: int = 0) -> int:
        value = self.get(name, default)

        try:
            return int(value) if value is not None else default
        except (ValueError, TypeError):
            return default

    def float(self, name: str, default: float = 0.0) -> float:
        value = self.get(name, default)

        try:
            return float(value) if value is not None else default
        except (ValueError, TypeError):
            return default

    def boolean(self, name: str, default: bool = False) -> bool:
        value = self.get(name, default)

        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ["true", "1", "yes"]
        if isinstance(value, (int, float)):
            return value != 0

        return default

    def array(self, name: str, default: list[T]) -> list[T]:
        value = self.get(name, default)
        return list(value) if value is not None else default
