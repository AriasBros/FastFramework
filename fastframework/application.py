import logging
from logging import Logger
from typing import Any

from fastframework.bootstrap.manager import BootstrapManager
from fastframework.bootstrap.service_provider import ServiceProvider
from fastframework.config.env import read_bool, read_str
from fastframework.config.provider import ConfigRepositoryProvider
from fastframework.container.container import Container
from fastframework.container.utils import get_attr
from fastframework.contracts.application import ApplicationInterface
from fastframework.contracts.container.container import ContainerInterface


class Application(ApplicationInterface):
    _critical_service_providers = [
        ConfigRepositoryProvider,
        # LoggingServiceProvider,
    ]

    _container: ContainerInterface

    def __init__(
        self,
        *service_providers: type[ServiceProvider],
        version: str = "0.1.0",
        logger: Logger | None = None,
        **kwargs: Any,
    ) -> None:
        self._container = Container(app=self)
        self._register_critical_services()
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
        return self._container

    def _register_critical_services(self):
        """Register critical services like config, logging, etc. that may be needed during the bootstrapping process."""
        for provider_class in self._critical_service_providers:
            provider_class(app=self).register()

    def _get_logger(self, app_name: str, logger: Logger | None) -> Logger:
        if logger is not None:
            return logger

        # TODO - We need to load the config repository before the bootstrap manager.

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
