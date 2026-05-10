from logging import Logger
import logging
from typing import Any

from fastframework.bootstrap.manager import BootstrapManager
from fastframework.bootstrap.service_provider import ServiceProvider
from fastframework.config.env import read_bool, read_str
from fastframework.container.container import Container
from fastframework.container.utils import get_attr
from fastframework.contracts.application import ApplicationInterface
from fastframework.contracts.container.container import ContainerInterface


class Application(ApplicationInterface):
    def __init__(
        self,
        *service_providers: type[ServiceProvider],
        version: str = "0.1.0",
        logger: Logger | None = None,
        **kwargs: Any,
    ) -> None:
        app_name = read_str("APP_NAME", "FastFramework Application")

        bootstrap_manager = BootstrapManager(
            self._get_logger(app_name, logger),
            *self._get_service_providers(*service_providers),
        )

        super().__init__(
            title=app_name,
            debug=read_bool("APP_DEBUG"),
            version=read_str("APP_VERSION", version),
            lifespan=bootstrap_manager.lifespan,
            **kwargs,
        )

        bootstrap_manager.run(self)

    @property
    def container(self) -> ContainerInterface:
        if not hasattr(self.state, "ioc_container"):
            setattr(self.state, "ioc_container", Container(app=self))

        return getattr(self.state, "ioc_container")

    def _get_logger(self, app_name: str, logger: Logger | None) -> Logger:
        if logger is not None:
            return logger

        # TODO

        default_logger = Logger(app_name)
        default_logger.setLevel(logging.DEBUG)
        default_logger.addHandler(logging.StreamHandler())

        return default_logger

    def _get_service_providers(
        self, *service_providers: type[ServiceProvider]
    ) -> tuple[type[ServiceProvider], ...]:
        if len(service_providers) > 0:
            return service_providers

        return get_attr("bootstrap.providers", "providers", ())
