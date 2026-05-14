from abc import ABC, abstractmethod
from typing import Generic, Self, TypeVar

from pyrannic.contracts.orm.model import ModelInterface
from pyrannic.contracts.orm.traits.can_be_soft_deleted import CanBeSoftDeletedInterface

T = TypeVar("T", bound=ModelInterface)


class RepositoryInterface(ABC, Generic[T]):
    @abstractmethod
    def select(self, model: type[T] | None = None) -> Self:
        """Initialize a select query for the model."""
        pass

    @abstractmethod
    async def delete(self, model: type[T] | None = None) -> Self:
        """Initialize a delete query for the model."""
        pass

    @abstractmethod
    async def create(self, model: T) -> T:
        pass

    @abstractmethod
    async def update(self, model: T) -> T:
        pass

    @abstractmethod
    async def destroy(self, model: T | None = None) -> None:
        """Permanently delete the records matching the current query."""
        pass

    @abstractmethod
    async def remove(self, model: CanBeSoftDeletedInterface) -> T:
        """Soft delete the models by setting the deleted_at timestamp."""
        pass
