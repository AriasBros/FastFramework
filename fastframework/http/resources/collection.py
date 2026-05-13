from typing import Any, TypeAlias, TypeVar, Union

from pydantic import BaseModel

from fastframework.contracts.http.resources.collection import (
    ResourceCollectionInterface,
)
from fastframework.contracts.http.resources.resource import ResourceInterface
from fastframework.contracts.pagination.paginator import PaginatorInterface
from fastframework.contracts.support.serializable import SerializableInterface
from fastframework.pagination.meta import PaginationMeta

ResourceType = TypeVar("ResourceType", covariant=True, bound=ResourceInterface)

DataType: TypeAlias = Union[
    list[ResourceType],
    list[SerializableInterface],
    PaginatorInterface[SerializableInterface, PaginationMeta],
]


class _ResourceCollection(ResourceCollectionInterface[ResourceType]):
    __resource_cls__: type[ResourceType]
    __meta_cls__: type[PaginationMeta] = PaginationMeta

    data: list[ResourceType]


class _PydanticCollection(BaseModel, _ResourceCollection[ResourceType]):
    def __init__(
        self,
        data: DataType[ResourceType],
        with_relationships: bool | list[str] = True,
        **kwargs: Any,
    ):
        assert self.__resource_cls__ is not None, (
            "Resource class must be set before initializing ResourceCollection"
        )

        if isinstance(data, PaginatorInterface):
            super().__init__(
                data=[
                    self.__resource_cls__.from_model(model, with_relationships)
                    for model in data.items
                ],
                meta=data.meta(self.__meta_cls__),
            )
        elif len(data) == 0 or isinstance(data[0], dict):
            super().__init__(data=data or [], **kwargs)
        else:
            super().__init__(
                data=[
                    self.__resource_cls__.from_model(model, with_relationships)
                    for model in data
                ],
                **kwargs,
            )


class ResourceCollection(_PydanticCollection[ResourceType]):
    def __init__(self, items: DataType[ResourceType], /, **kwargs: Any) -> None:
        kwargs["data"] = items
        super().__init__(**kwargs)
