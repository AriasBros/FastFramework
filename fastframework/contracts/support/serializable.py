from typing import Any


class SerializableInterface:
    __abstract__ = True

    def to_dict(
        self,
        nested: bool = False,
        hybrid_attributes: bool = False,
        exclude: list[str] | None = None,
    ) -> dict[str, Any]:
        return {}
