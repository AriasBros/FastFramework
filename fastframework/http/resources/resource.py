from typing import Any, Self

from pydantic import PrivateAttr

from fastframework.contracts.http.resources.resource import ResourceInterface
from fastframework.contracts.support.serializable import SerializableInterface


class Resource(ResourceInterface):
    _with_relationships: bool | list[str] = PrivateAttr(default=True)

    @classmethod
    def from_model(
        cls,
        model: SerializableInterface,
        with_relationships: bool | list[str] = True,
    ) -> Self | None:
        cls._with_relationships = with_relationships
        return cls.model_validate(cls.model_to_dict(model)) if model else None

    @classmethod
    def model_to_dict(cls, model: SerializableInterface) -> dict[str, Any]:
        return {
            **cls._attrs(model),
            **cls.__relationships(model),
        }

    @classmethod
    def __relationships(cls, model: SerializableInterface) -> dict[str, Any]:
        relationships: dict[str, dict[str, Any]] = cls._relationships(model)

        if isinstance(cls._with_relationships, list):
            return {
                k: v for k, v in relationships.items() if k in cls._with_relationships
            }
        elif cls._with_relationships:
            return relationships

        return {}

    def to_dict(
        self,
        nested: bool = False,
        hybrid_attributes: bool = False,
        exclude: list[str] | None = None,
    ) -> dict[str, Any]:
        return self.model_dump(exclude=set(exclude) if exclude else set())
