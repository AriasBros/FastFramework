from abc import ABC, abstractmethod


class MigrationInterface(ABC):
    @abstractmethod
    async def up(self) -> None:
        pass

    @abstractmethod
    async def down(self) -> None:
        pass
