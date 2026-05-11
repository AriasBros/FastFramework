from contextlib import asynccontextmanager
from logging import Logger
from typing import AsyncGenerator, Type

from dotenv import load_dotenv

from fastframework.bootstrap.service_provider import ServiceProvider
from fastframework.contracts.application import ApplicationInterface
from fastframework.dependency_injection.resolvers import resolve_dependant


class BootstrapManager:
    _service_providers_classes: tuple[Type[ServiceProvider], ...]
    _service_providers_instances: list[ServiceProvider]
    _starting = False

    def __init__(
        self, logger: Logger, *service_providers: Type[ServiceProvider]
    ) -> None:
        self._logger = logger
        self._service_providers_classes = service_providers
        self._service_providers_instances = []
        load_dotenv()

    def run(self, app: ApplicationInterface) -> None:
        self._starting = True
        self._logger.info("🕒 Initializing application...")

        for ProviderClass in self._service_providers_classes:
            provider = ProviderClass(app, self._logger)
            name = ProviderClass.__name__

            try:
                self._service_providers_instances.append(provider)
                self._register_provider(provider)
                self._logger.info(f"✅ Registered {name}")
            except Exception as e:
                self._provider_exec_failed(provider, "register", e)

    @asynccontextmanager
    async def lifespan(self, app: ApplicationInterface) -> AsyncGenerator[None, None]:
        self._logger.info("🚀 Starting up application...")

        await self._walk_providers(app, "initialize", "Initialized")
        await self._walk_providers(app, "boot", "Booted")
        self._starting = False

        yield

        await self._walk_providers(app, "shutdown", "Shutdown", should_reverse=True)

        self._logger.info("✅ Resources released and application shutdown complete")

    async def _walk_providers(
        self,
        app: ApplicationInterface,
        method_name: str,
        info_message: str,
        should_reverse: bool = False,
    ) -> None:
        providers = (
            self._service_providers_instances[::-1]
            if should_reverse
            else self._service_providers_instances
        )

        for provider in providers:
            try:
                name = provider.__class__.__name__
                method = getattr(provider, method_name, None)

                if method is not None:
                    await resolve_dependant(method, name=name, app=app)
                    self._logger.info(f"✅ {info_message} {name}")
            except Exception as e:
                self._provider_exec_failed(provider, method_name, e)

    def _provider_exec_failed(
        self,
        provider: ServiceProvider,
        method_name: str,
        exception: Exception,
    ):
        name = provider.__class__.__name__

        if self._starting and provider.is_critical:
            self._logger.critical(
                f"❌  {name} failed to {method_name}, cannot start app"
            )
            raise provider.exception(f"{name} failed to {method_name}") from exception
        else:
            self._logger.warning(
                f"⚠️  {name} failed to {method_name} properly: {exception}"
            )

            if self._starting:
                provider.failed(method_name)

    def _register_provider(self, provider: ServiceProvider):
        for abstract, concrete in provider.__bindings__.items():
            provider.app.container.bind(abstract, concrete)

        provider.register()
