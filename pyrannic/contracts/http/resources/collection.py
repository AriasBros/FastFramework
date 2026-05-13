from typing import Generic, TypeVar

from pyrannic.contracts.http.resources.resource import ResourceInterface

DataType = TypeVar("DataType", covariant=True, bound=ResourceInterface)


class ResourceCollectionInterface(Generic[DataType]):
    pass
