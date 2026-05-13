from typing import Type

from app.providers.app import AppServiceProvider

from pyrannic.bootstrap.service_provider import ServiceProvider
from pyrannic.http.providers import (
    MiddlewaresServiceProvider,
    RoutersServiceProvider,
)

providers: list[Type[ServiceProvider]] = [
    AppServiceProvider,
    RoutersServiceProvider,
    MiddlewaresServiceProvider,
]
