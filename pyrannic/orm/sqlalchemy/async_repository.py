from logging import Logger
from typing import Annotated, Any, Self

from sqlalchemy import CompoundSelect, Delete, Select, delete, select

from pyrannic.container.param_functions import Resolves
from pyrannic.contracts.database.manager import DatabaseManagerInterface
from pyrannic.contracts.orm.async_repository import RepositoryInterface, T


class Repository(RepositoryInterface[T]):
    __model__: type[T]
    _query: Select[Any] | CompoundSelect[Any] | Delete | None = None
    _is_ordering: bool = False

    def __init__(
        self,
        manager: Annotated[DatabaseManagerInterface, Resolves()],
        logger: Annotated[Logger, Resolves()],
    ):
        self._connection = manager.connection
        self._logger = logger

    def select(self, model: type[T] | None = None) -> Self:
        self._query = select(model or self.__model__)
        return self

    def delete(self, model: type[T] | None = None) -> Self:
        self._query = delete(model or self.__model__)
        return self

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

    """

    async def update(self, model: T) -> T:
        pass

    async def destroy(self, model: T | None = None) -> None:
        pass

    async def remove(self, model: CanBeSoftDeletedInterface) -> T:
        pass
    
    """

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

    def _reset_query(self) -> None:
        self._query = None
        self._is_ordering = False
