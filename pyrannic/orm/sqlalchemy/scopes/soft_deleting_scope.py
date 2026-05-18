from pyrannic.contracts.orm.mixins.soft_deletes import SoftDeletesInterface
from pyrannic.contracts.orm.query_builder import QueryBuilderInterface, T
from pyrannic.contracts.orm.scope import ScopeInterface


class SoftDeletingScope(ScopeInterface[T]):
    """
    A scope that automatically excludes soft-deleted records from query results.
    This scope can be applied to repositories that manage models implementing the SoftDeletesInterface.
    """

    def apply(self, repository: QueryBuilderInterface[T]) -> None:
        if issubclass(repository.model, SoftDeletesInterface):
            repository.where_none(repository.model.deleted_at_column())
