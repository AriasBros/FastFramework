from abc import ABC, abstractmethod
from typing import Any, Generic, Self, TypeVar

from pyrannic.contracts.orm.model import ModelInterface

T = TypeVar("T", bound=ModelInterface)


class QueryBuilderInterface(ABC, Generic[T]):
    @property
    @abstractmethod
    def model(self) -> type[T]:
        """Return the model type associated with this query builder."""
        pass

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
    def where_none(self, column_name: str) -> Self:
        """Add a where condition to check if the column is None."""
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
        """Add group by conditions to the current query."""
        pass
