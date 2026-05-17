from abc import ABC, abstractmethod
from typing import Any, Generic, Self, TypeVar

from pyrannic.contracts.orm.model import ModelInterface
from pyrannic.contracts.orm.traits.can_be_soft_deleted import CanBeSoftDeletedInterface
from pyrannic.contracts.pagination.paginator import PaginatorInterface

T = TypeVar("T", bound=ModelInterface)


class BaseRepositoryInterface(ABC, Generic[T]):
    @abstractmethod
    def select(self, model: type[T] | None = None) -> Self:
        """Initialize a select query for the model."""
        pass

    @abstractmethod
    def delete(self, model: type[T] | None = None) -> Self:
        """Initialize a delete query for the model."""
        pass

    @abstractmethod
    def order_by(self, *attributes: Any) -> Self:
        """Set the order for the current query."""
        pass

    @abstractmethod
    def limit(self, limit: int | None) -> Self:
        """Set the limit for the current query."""
        pass

    @abstractmethod
    def offset(self, offset: int | None) -> Self:
        """Set the offset for the current query."""
        pass

    @abstractmethod
    def where(self, *where_clause: Any) -> Self:
        """Add where conditions to the current query."""
        pass

    @abstractmethod
    def filter(self, *filters: Any | None) -> Self:
        """Add filtering conditions to the current query."""
        pass

    @abstractmethod
    def filter_by(self, **kwargs: Any) -> Self:
        """Add filtering conditions to the current query."""
        pass

    @abstractmethod
    def group_by(self, *attributes: Any) -> Self:
        pass


class RepositoryInterface(BaseRepositoryInterface[T]):
    @abstractmethod
    def create(self, model: T) -> T:
        """Insert a new record into the database."""
        pass

    @abstractmethod
    def update(self, model: T) -> T:
        """Update an existing record in the database."""
        pass

    @abstractmethod
    def destroy(self, model: T | None = None) -> None:
        """Permanently delete the records matching the current query."""
        pass

    @abstractmethod
    def remove(self, model: T) -> T:
        """
        Soft delete the models by setting the deleted_at timestamp.
        The model must implement the CanBeSoftDeletedInterface mixin for this to work.
        """
        pass

    @abstractmethod
    def count(self, reset_query: bool = True) -> int:
        """Count the number of records matching the current query."""
        pass

    @abstractmethod
    def first(self) -> T | None:
        """Retrieve the first record of the model."""
        pass

    @abstractmethod
    def get(self) -> list[T]:
        """Retrieve all records matching the current query."""
        pass

    @abstractmethod
    def find_by_id(self, value: Any) -> T | None:
        """Find a record by its primary key."""
        pass

    @abstractmethod
    def paginate(
        self,
        page: int = 1,
        per_page: int | None = None,
        **kwargs: Any,
    ) -> PaginatorInterface[T, Any]:
        """Paginate the results of the current query."""
        pass
