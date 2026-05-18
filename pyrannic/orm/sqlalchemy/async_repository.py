from typing import Any

from pyrannic.contracts.orm.async_repository import RepositoryInterface, T
from pyrannic.contracts.pagination.paginator import PaginatorInterface
from pyrannic.orm.sqlalchemy.query_builder import QueryBuilder
from pyrannic.pagination.paginator import Paginator


class AsyncRepository(QueryBuilder[T], RepositoryInterface[T]):
    async def create(self, model: T) -> T:
        async with self._connection() as session:
            try:
                session.add(model)
                await session.commit()
                await session.refresh(model)
                return model
            except Exception as e:
                await session.rollback()
                self._logger.exception(f"Rolling Back. Error inserting object: {e}")
                raise

    async def update(self, model: T) -> T:
        async with self._connection() as session:
            try:
                await session.merge(model)
                await session.commit()
                return model
            except Exception as e:
                await session.rollback()
                self._logger.exception(f"Rolling Back. Error updating model: {e}")
                raise

    async def destroy(self, model: T | None = None) -> None:
        self._prepare_destroy_model_if_needed(model)

        assert self._query is not None

        async with self._connection() as session:
            try:
                await session.execute(self._query)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                self._reset_query()

    async def remove(self, model: T) -> T:
        return (await self.update(model)) if self._remove_model(model) else model

    async def restore(self, model: T) -> T:
        return (await self.update(model)) if self._restore_model(model) else model

    async def count(self, reset_query: bool = True) -> int:
        assert self._query is not None

        count = 0

        async with self._connection() as session:
            count = (await session.execute(self._get_count_query)).scalar()

        if reset_query:
            self._reset_query()

        return count

    async def first(self) -> T | None:
        assert self._query is not None

        model = None

        async with self._connection() as session:
            model = (await session.scalars(self._query)).first()

        self._reset_query()

        return model

    async def get(self) -> list[T]:
        assert self._query is not None

        models = None

        async with self._connection() as session:
            models = (await session.scalars(self._query)).all()

        self._reset_query()

        return models or []

    async def find_by_id(self, value: Any) -> T | None:
        return await (
            self.select().where(self.__model__.primary_key_column() == value).first()
        )

    async def paginate(
        self,
        page: int = 1,
        per_page: int | None = None,
        **kwargs: Any,
    ) -> PaginatorInterface[T, Any]:
        assert self._query is not None

        total = await self.count(reset_query=False)
        page, per_page, last_page = self._apply_pagination(total, page, per_page)
        items = await self.get()

        return Paginator(items, page, per_page, total, last_page, **kwargs)
