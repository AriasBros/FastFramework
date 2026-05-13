from abc import ABC, abstractmethod
from typing import Any, Self

from pydantic import BaseModel

from fastframework.contracts.support.serializable import SerializableInterface


class BaseResource(BaseModel):
    @classmethod
    def _attrs(cls, model: SerializableInterface) -> dict[str, Any]:
        return model.to_dict(hybrid_attributes=True)

    @classmethod
    def _relationships(cls, model: SerializableInterface) -> dict[str, Any]:
        return {}


class ResourceInterface(ABC, BaseResource, SerializableInterface):
    @classmethod
    @abstractmethod
    def from_model(
        cls,
        model: SerializableInterface,
        with_relationships: bool | list[str] = True,
    ) -> Self | None:
        pass

    @classmethod
    @abstractmethod
    def model_to_dict(cls, model: SerializableInterface) -> dict[str, Any]:
        pass
