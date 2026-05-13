from typing import Any, Optional

from pydantic import Field

from fastframework import Resource, ResourceCollection
from fastframework.http.resources.collection import DataType
from fastframework.pagination.meta import PaginationMeta


class Foo(Resource):
    name: str = Field(description="The name of the resource")
    description: Optional[str] = Field(
        default=None, description="A brief description of the resource"
    )


class FooCollection(ResourceCollection[Foo]):
    __resource_cls__ = Foo
    meta: PaginationMeta

    # NOTE: Needed to avoid Pydantic's validation error when initializing with a list of resources.
    def __init__(self, items: DataType[Foo], /, **kwargs: Any) -> None:
        super().__init__(items, **kwargs)
