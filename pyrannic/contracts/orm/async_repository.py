from abc import abstractmethod
from typing import Any

from pyrannic.contracts.orm.repository import BaseRepositoryInterface, T
from pyrannic.contracts.pagination.paginator import PaginatorInterface


class RepositoryInterface(BaseRepositoryInterface[T]):
    @abstractmethod
    async def create(self, model: T) -> T:
        """Insert a new record into the database."""
        pass

    @abstractmethod
    async def update(self, model: T) -> T:
        """Update an existing record in the database."""
        pass

    @abstractmethod
    async def destroy(self, model: T | None = None) -> None:
        """Permanently delete the records matching the current query."""
        pass

    @abstractmethod
    async def remove(self, model: T) -> T:
        """
        Soft delete the models by setting the deleted_at timestamp.
        The model must implement the CanBeSoftDeletedInterface mixin for this to work.
        """
        pass

    @abstractmethod
    async def count(self, reset_query: bool = True) -> int:
        """Count the number of records matching the current query."""
        pass

    @abstractmethod
    async def first(self) -> T | None:
        """Retrieve the first record of the model."""
        pass

    @abstractmethod
    async def get(self) -> list[T]:
        """Retrieve all records matching the current query."""
        pass

    @abstractmethod
    async def find_by_id(self, value: Any) -> T | None:
        """Find a record by its primary key."""
        pass

    @abstractmethod
    async def paginate(
        self,
        page: int = 1,
        per_page: int | None = None,
        **kwargs: Any,
    ) -> PaginatorInterface[T, Any]:
        """Paginate the results of the current query."""
        pass
