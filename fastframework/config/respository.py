from typing import Any

from fastframework.collections.dot_dict import has, get, set
from fastframework.contracts.config.respository import ConfigRepositoryInterface


class ConfigRepository(ConfigRepositoryInterface):
    _items: dict[str, Any] = {}

    def __init__(self, items: dict[str, Any] = dict()) -> None:
        self._items = items

    def __getattr__(self, name: str, default: Any | None = None) -> Any | None:
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

    def string(self, name: str, default: str | None = None) -> str | None:
        value = self.get(name, default)
        return str(value) if value is not None else default

    def integer(self, name: str, default: int | None = None) -> int | None:
        value = self.get(name, default)

        try:
            return int(value) if value is not None else default
        except (ValueError, TypeError):
            return default

    def float(self, name: str, default: float | None = None) -> float | None:
        value = self.get(name, default)

        try:
            return float(value) if value is not None else default
        except (ValueError, TypeError):
            return default

    def boolean(self, name: str, default: bool | None = None) -> bool | None:
        value = self.get(name, default)

        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ["true", "1", "yes"]
        if isinstance(value, (int, float)):
            return value != 0

        return default
