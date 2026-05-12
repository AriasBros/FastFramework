from typing import Type

from fastframework.bootstrap.service_provider import ServiceProvider
from fastframework.http.providers import (
    RoutersServiceProvider,
    MiddlewaresServiceProvider,
)

from app.providers.app import AppServiceProvider

providers: list[Type[ServiceProvider]] = [
    AppServiceProvider,
    RoutersServiceProvider,
    MiddlewaresServiceProvider,
]
