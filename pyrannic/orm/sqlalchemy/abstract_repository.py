from logging import Logger
import math
from typing import Annotated, Any, Generic, Self

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

from pyrannic.container.param_functions import Resolves
from pyrannic.contracts.database.manager import DatabaseManagerInterface
from pyrannic.contracts.orm.repository import T
from pyrannic.contracts.orm.traits.can_be_soft_deleted import CanBeSoftDeletedInterface
from pyrannic.support.datetime import get_current_utc_datetime
from pyrannic.support.reflection import get_generic_type


class AbstractRepository(Generic[T]):
    __model__: type[T]
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

    def select(self, model: type[T] | None = None) -> Self:
        self._query = select(model or self.__model__)
        return self

    def delete(self, model: type[T] | None = None) -> Self:
        self._query = delete(model or self.__model__)
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

    def _apply_pagination(
        self,
        total: int = 0,
        page: int = 1,
        per_page: int | None = None,
    ) -> tuple[int, int, int]:
        if not self._is_ordering:
            self.order_by(self.__model__.primary_key_column().asc())

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
                self.__model__.primary_key_column() == model.primary_key_value
            )

    def _remove_model(self, model: T) -> bool:
        if isinstance(model, CanBeSoftDeletedInterface):
            model.set_deleted_at(get_current_utc_datetime())
            return True

        return False
