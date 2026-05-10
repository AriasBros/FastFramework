import os
from logging import Logger
from typing import Any, Type

from fastframework.bootstrap.manager import BootstrapManager
from fastframework.bootstrap.service_provider import ServiceProvider
from fastframework.container.container import Container
from fastframework.contracts.application import ApplicationInterface
from fastframework.contracts.container.container import ContainerInterface


class Application(ApplicationInterface):
    def __init__(
        self,
        logger: Logger,
        *service_providers: Type[ServiceProvider],
        version: str = "0.1.0",
        **kwargs: Any,
    ) -> None:
        bootstrap_manager = BootstrapManager(logger, *service_providers)

        super().__init__(
            title=os.environ.get("APP_NAME", "FastFramework Application"),
            version=os.environ.get("APP_VERSION", version),
            lifespan=bootstrap_manager.lifespan,
            **kwargs,
        )

        bootstrap_manager.run(self)

    @property
    def container(self) -> ContainerInterface:
        if not hasattr(self.state, "ioc_container"):
            setattr(self.state, "ioc_container", Container(app=self))

        return getattr(self.state, "ioc_container")
