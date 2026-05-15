from typing import Any, Sequence, TypeAlias, TypeVar, Union

from pydantic import BaseModel

from pyrannic.contracts.http.resources.collection import (
    ResourceCollectionInterface,
)
from pyrannic.contracts.http.resources.resource import ResourceInterface
from pyrannic.contracts.pagination.paginator import PaginatorInterface
from pyrannic.contracts.support.serializable import SerializableInterface
from pyrannic.pagination.meta import PaginationMeta

ResourceType = TypeVar("ResourceType", covariant=True, bound=ResourceInterface)

DataType: TypeAlias = Union[
    Sequence[ResourceType],
    Sequence[SerializableInterface],
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
