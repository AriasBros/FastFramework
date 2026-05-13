from typing import Generic, TypeVar

from fastframework.contracts.http.resources.resource import ResourceInterface

DataType = TypeVar("DataType", covariant=True, bound=ResourceInterface)


class ResourceCollectionInterface(Generic[DataType]):
    pass
