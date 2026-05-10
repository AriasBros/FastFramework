from abc import abstractmethod
from typing import Generic, TypeVar

from fastframework.bootstrap.service_provider import ServiceProvider
from fastframework.dependency_injection.resolvers import resolve_dependant

ServiceType = TypeVar("ServiceType")


class AppStateServiceProvider(ServiceProvider, Generic[ServiceType]):
    _service: ServiceType

    @property
    def service(self) -> ServiceType:
        return self._service

    @property
    def has_dependencies(self) -> bool:
        return False

    @property
    def state_key(self) -> str:
        return ServiceType.__name__

    @abstractmethod
    def create(self) -> ServiceType:
        pass

    def register(self):
        if not self.has_dependencies:
            self._service = self.create()
            setattr(self.app.state, self.state_key, self._service)

    async def boot(self):
        if self.has_dependencies:
            self._service = await resolve_dependant(
                self.create,
                name=self.state_key,
                app=self.app,
            )

            setattr(self.app.state, self.state_key, self._service)

    def failed(self, stage_name: str):
        setattr(self.app.state, self.state_key, None)
