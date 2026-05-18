from typing import Any

from pyrannic.contracts.orm.repository import RepositoryInterface, T
from pyrannic.contracts.pagination.paginator import PaginatorInterface
from pyrannic.orm.sqlalchemy.query_builder import QueryBuilder
from pyrannic.pagination.paginator import Paginator


class Repository(QueryBuilder[T], RepositoryInterface[T]):
    def create(self, model: T) -> T:
        with self._connection() as session:
            try:
                session.add(model)
                session.commit()
                session.refresh(model)
                return model
            except Exception as e:
                session.rollback()
                self._logger.exception(f"Rolling Back. Error inserting model: {e}")
                raise

    def update(self, model: T) -> T:
        with self._connection() as session:
            try:
                session.merge(model)
                session.commit()
                return model
            except Exception as e:
                session.rollback()
                self._logger.exception(f"Rolling Back. Error updating model: {e}")
                raise

    def destroy(self, model: T | None = None) -> None:
        self._prepare_destroy_model_if_needed(model)

        assert self._query is not None

        # TODO - Apply Scopes before executing the delete query

        with self._connection() as session:
            try:
                session.execute(self._query)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
            finally:
                self._reset_query()

    def remove(self, model: T) -> T:
        return self.update(model) if self._remove_model(model) else model

    def restore(self, model: T) -> T:
        return self.update(model) if self._restore_model(model) else model

    def count(self) -> int:
        self._before_query()
        return self._count(reset_query=False)

    def first(self) -> T | None:
        self._before_query()

        model = None

        with self._connection() as session:
            model = (session.scalars(self._query)).first()

        self._reset_query()

        return model

    def get(self) -> list[T]:
        self._before_query()
        return self._get()

    def find_by_id(self, value: Any) -> T | None:
        return self.select().where(self.__model__.primary_key_column() == value).first()

    def paginate(
        self,
        page: int = 1,
        per_page: int | None = None,
        **kwargs: Any,
    ) -> PaginatorInterface[T, Any]:
        self._before_query()

        total = self._count(reset_query=False)
        page, per_page, last_page = self._apply_pagination(total, page, per_page)
        items = self._get()

        return Paginator(items, page, per_page, total, last_page, **kwargs)

    def _get(self) -> list[T]:
        models = None

        with self._connection() as session:
            models = (session.scalars(self._query)).all()

        self._reset_query()

        return models or []

    def _count(self, reset_query: bool = True) -> int:
        count = 0

        with self._connection() as session:
            count = session.execute(self._get_count_query).scalar()

        if reset_query:
            self._reset_query()

        return count
