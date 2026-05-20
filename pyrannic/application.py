from typing import Any

from pyrannic.bootstrap.manager import BootstrapManager
from pyrannic.bootstrap.service_provider import ServiceProvider
from pyrannic.config.provider import ConfigRepositoryProvider
from pyrannic.container.container import Container
from pyrannic.contracts.application import ApplicationInterface
from pyrannic.contracts.container.container import ContainerInterface
from pyrannic.logging.provider import LoggingServiceProvider
from pyrannic.support.facades.config import Config


class Application(ApplicationInterface):
    _critical_service_providers: list[type[ServiceProvider]] = [
        ConfigRepositoryProvider,
        LoggingServiceProvider,
    ]

    def __init__(
        self,
        *,
        debug: bool = False,
        version: str = "0.1.0",
        title: str | None = None,
        **kwargs: Any,
    ) -> None:
        bootstrap_manager = BootstrapManager().start_critical_services(
            self,
            self._critical_service_providers,
        )

        app_name = Config.string("app.name", title or "Pyrannic Application")

        super().__init__(
            title=app_name,
            debug=Config.boolean("app.debug", debug),
            version=Config.string("app.version", version),
            lifespan=bootstrap_manager.lifespan,
            **kwargs,
        )

        bootstrap_manager.run(self)

    @property
    def container(self) -> ContainerInterface:
        if not hasattr(self, "_container"):
            self._container = Container(self)

        return self._container
