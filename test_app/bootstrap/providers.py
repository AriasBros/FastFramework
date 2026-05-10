from typing import Type

from fastframework.bootstrap.service_provider import ServiceProvider

from app.providers.app import AppServiceProvider
from app.providers.routers import RoutersProvider

providers: list[Type[ServiceProvider]] = [
    AppServiceProvider,
    RoutersProvider,
]
