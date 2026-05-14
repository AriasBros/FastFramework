from typing import Self

from sqlalchemy import CompoundSelect, Delete, Select, delete, select

from pyrannic.contracts.orm.repository import RepositoryInterface, T
from pyrannic.contracts.orm.traits.can_be_soft_deleted import CanBeSoftDeletedInterface


class Repository(RepositoryInterface[T]):
    __model__: type[T]
    _query: Select | CompoundSelect | Delete | None = None
    _is_ordering: bool = False

    def __init__(
        self,
        database_service: Annotated[DatabaseService, Depends()],
        logger: Annotated[Logger, Depends(get_logger)],
    ):
        self._session = database_service.session
        self._logger = logger

    def select(self, model: type[T] | None = None) -> Self:
        self._query = select(model or self.__model__)
        return self

    async def delete(self, model: type[T] | None = None) -> Self:
        self._query = delete(model or self.__model__)
        return self

    async def create(self, model: T) -> T:
        async with self._session() as session:
            try:
                session.add(obj)
                await session.commit()
                await session.refresh(obj)
                return obj
            except Exception as e:
                await session.rollback()
                self._logger.exception(f"Rolling Back. Error inserting object: {e}")
                raise

    async def update(self, model: T) -> T:
        pass

    async def destroy(self, model: T | None = None) -> None:
        pass

    async def remove(self, model: CanBeSoftDeletedInterface) -> T:
        pass

    def _reset_query(self) -> None:
        self._query = None
        self._is_ordering = False
