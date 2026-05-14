from abc import ABC, abstractmethod
from typing import Any

from pyrannic.contracts.database.migration import MigrationInterface


class ConnectorInterface(ABC):
    @abstractmethod
    async def connection(self) -> Any:
        """
        Establishes a connection to the database.
        """
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """
        Closes the connection to the database.
        """
        pass

    @abstractmethod
    async def migrate(
        self,
        migrations: list[type[MigrationInterface]] | None = None,
    ) -> None:
        """
        Runs the provided migrations against the database.
        """
        pass
