from typing import Any, Optional

from pydantic import Field

from pyrannic import Resource, ResourceCollection
from pyrannic.http.resources.collection import DataType


class Hero(Resource):
    id: str = Field(coerce_numbers_to_str=True)
    name: str = Field(
        description="The name of the hero, e.g., 'Superman', 'Batman'.",
    )

    description: Optional[str] = Field(
        default=None,
        description="The description of the hero, e.g., 'The Man of Steel', 'The Dark Knight'.",
    )


class HeroesCollection(ResourceCollection[Hero]):
    __resource_cls__ = Hero
    # meta: PaginationMeta

    # NOTE: Needed to avoid Pydantic's validation error when initializing with a list of resources.
    def __init__(self, items: DataType[Hero], /, **kwargs: Any) -> None:
        super().__init__(items, **kwargs)
