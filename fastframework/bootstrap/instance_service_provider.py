from abc import abstractmethod
from typing import Generic, TypeVar, get_args

from fastframework.bootstrap.service_provider import ServiceProvider

ServiceType = TypeVar("ServiceType")


class InstanceServiceProvider(ServiceProvider, Generic[ServiceType]):
    @property
    def has_dependencies(self) -> bool:
        return False

    @property
    def abstract(self) -> str | type:
        return get_args(type(self).__orig_bases__[0])[0]  # type: ignore

    @property
    def aliases(self) -> list[str | type] | None:
        return None

    @abstractmethod
    def create(self) -> ServiceType:
        pass

    def register(self):
        if not self.has_dependencies:
            self._set_instance(self.create())

    async def boot(self):
        if self.has_dependencies:
            self._set_instance(await self.app.container.call(self.create))

    def _set_instance(self, instance: ServiceType):
        abstract = self.abstract
        aliases = self.aliases

        self.app.container.instance(abstract, instance)

        if aliases:
            for alias in aliases:
                self.app.container.set_alias(abstract, alias)
