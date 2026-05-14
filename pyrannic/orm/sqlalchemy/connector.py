from typing import Any

from pyrannic.contracts.database.connector import ConnectorInterface
from pyrannic.contracts.database.migration import MigrationInterface


class SqlAlchemyConnector(ConnectorInterface):
    async def connection(self) -> Any:
        pass

    async def disconnect(self) -> None:
        pass

    async def migrate(
        self,
        migrations: list[type[MigrationInterface]] | None = None,
    ) -> None:
        print(migrations)
        pass
