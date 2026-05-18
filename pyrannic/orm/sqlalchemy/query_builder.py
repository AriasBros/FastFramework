import math
from datetime import datetime
from logging import Logger
from typing import Annotated, Any, Self

from pyrannic.container.param_functions import Resolves
from pyrannic.contracts.database.manager import DatabaseManagerInterface
from pyrannic.contracts.orm.mixins.soft_deletes import SoftDeletesInterface
from pyrannic.contracts.orm.query_builder import QueryBuilderInterface
from pyrannic.contracts.orm.repository import T
from pyrannic.contracts.orm.scope import ScopeInterface
from pyrannic.orm.sqlalchemy.scopes.soft_deleting_scope import SoftDeletingScope
from pyrannic.support.datetime import get_current_utc_datetime
from pyrannic.support.reflection import get_generic_type
from sqlalchemy import (
    ColumnExpressionArgument,
    CompoundSelect,
    Delete,
    Select,
    UnaryExpression,
    delete,
    func,
    select,
)
from sqlalchemy.orm import InstrumentedAttribute


class QueryBuilder(QueryBuilderInterface[T]):
    __model__: type[T]
    __scopes__: list[ScopeInterface[T]] = []

    _scopes: list[ScopeInterface[T]] = []
    _query: Select[Any] | Delete | CompoundSelect[Any] | None = None
    _is_ordering: bool = False

    def __init__(
        self,
        manager: Annotated[DatabaseManagerInterface, Resolves()],
        logger: Annotated[Logger, Resolves()],
    ):
        if not hasattr(self, "__model__"):
            self.__model__ = get_generic_type(self)

        self._connection = manager.connection
        self._logger = logger

        self._scopes.append(SoftDeletingScope())
        self._scopes.extend(self.__scopes__)

    @property
    def model(self) -> type[T]:
        return self.__model__

    def select(self, model: type[T] | None = None) -> Self:
        self._query = select(model or self.model)
        return self

    def delete(self, model: type[T] | None = None) -> Self:
        self._query = delete(model or self.model)
        return self

    def order_by(
        self,
        *attributes: str | InstrumentedAttribute[Any] | UnaryExpression[Any],
    ) -> Self:
        assert self._query is not None

        if isinstance(self._query, (Select, CompoundSelect)):
            self._is_ordering = True
            self._query = self._query.order_by(*attributes)

        return self

    def limit(self, limit: int | None) -> Self:
        assert self._query is not None

        if limit is not None and limit > 0 and isinstance(self._query, Select):
            self._query = self._query.limit(limit)

        return self

    def offset(self, offset: int | None) -> Self:
        assert self._query is not None

        if offset is not None and offset > 0 and isinstance(self._query, Select):
            self._query = self._query.offset(offset)

        return self

    def where(self, *where_clause: ColumnExpressionArgument[Any]) -> Self:
        assert self._query is not None

        if isinstance(self._query, (Select, Delete)):
            self._query = self._query.where(*where_clause)

        return self

    def where_none(self, column_name: str) -> Self:
        return self.filter_by(**{column_name: None})

    def filter(self, *filters: ColumnExpressionArgument[Any] | None) -> Self:
        assert self._query is not None

        if isinstance(self._query, (Select, Delete)):
            filters = tuple(v for v in filters if v is not None)
            self._query = self._query.where(*filters)

        return self

    def filter_by(self, **kwargs: Any) -> Self:
        assert self._query is not None

        if isinstance(self._query, (Select, Delete)):
            self._query = self._query.filter_by(**kwargs)

        return self

    def group_by(
        self,
        *attributes: str | InstrumentedAttribute[Any] | UnaryExpression[Any],
    ) -> Self:
        assert self._query is not None

        if isinstance(self._query, (Select, CompoundSelect)):
            self._query = self._query.group_by(*attributes)

        return self

    def _reset_query(self) -> None:
        self._query = None
        self._is_ordering = False

    @property
    def _get_count_query(self) -> Select[Any]:
        assert isinstance(self._query, Select)

        return (
            self._query.with_only_columns(func.count(), maintain_column_froms=True)
            .order_by(None)
            .limit(None)
            .offset(None)
        )

    @staticmethod
    def _resolve_page(page: int | None = 1) -> int:
        if page is None or page <= 0:
            return 1

        return page

    @staticmethod
    def _resolve_last_page(last_page: int | None = None) -> int:
        if last_page is None or last_page <= 0:
            return 1

        return last_page

    def _before_query(self) -> None:
        assert self._query is not None
        self._apply_scopes()

    def _apply_scopes(self) -> Self:
        for scope in self._scopes:
            scope.apply(self)

        return self

    def _apply_pagination(
        self,
        total: int = 0,
        page: int = 1,
        per_page: int | None = None,
    ) -> tuple[int, int, int]:
        if not self._is_ordering:
            self.order_by(self.model.primary_key_column().asc())

        if per_page is None or per_page <= 0:
            per_page = max(total, 1)
            last_page = 1
            page = 1
        else:
            last_page = self._resolve_last_page(math.ceil(total / per_page))
            page = self._resolve_page(page)

            count = per_page
            offset = (page - 1) * per_page

            self.limit(count).offset(offset)

        return page, per_page, last_page

    def _prepare_destroy_model_if_needed(self, model: T | None) -> None:
        if model is not None:
            self.delete().where(
                self.model.primary_key_column() == model.primary_key_value
            )

    def _prepare_soft_deletes_model(
        self,
        model: T,
        deleted_at: datetime | None,
    ) -> bool:
        if isinstance(model, SoftDeletesInterface):
            model.set_deleted_at(deleted_at)
            return True

        return False

    def _remove_model(self, model: T) -> bool:
        return self._prepare_soft_deletes_model(model, get_current_utc_datetime())

    def _restore_model(self, model: T) -> bool:
        return self._prepare_soft_deletes_model(model, None)
