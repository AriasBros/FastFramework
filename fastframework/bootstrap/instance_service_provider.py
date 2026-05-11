from abc import abstractmethod
from typing import Generic, TypeVar

from fastframework.bootstrap.service_provider import ServiceProvider

ServiceType = TypeVar("ServiceType")


class InstanceServiceProvider(ServiceProvider, Generic[ServiceType]):
    @property
    def has_dependencies(self) -> bool:
        return False

    @property
    def abstract(self) -> str | type:
        return ServiceType.__class__

    @abstractmethod
    def create(self) -> ServiceType:
        pass

    def register(self):
        if not self.has_dependencies:
            instance = self.create()
            self.app.container.instance(self.abstract, instance)

    async def boot(self):
        if self.has_dependencies:
            instance = await self.app.container.call(self.create)
            self.app.container.instance(self.abstract, instance)
