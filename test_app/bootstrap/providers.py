from typing import Type

from app.providers.app import AppServiceProvider

from pyrannic import (
    DatabaseServiceProvider,
    MiddlewaresServiceProvider,
    RoutersServiceProvider,
    ServiceProvider,
)

providers: list[Type[ServiceProvider]] = [
    AppServiceProvider,
    DatabaseServiceProvider,
    RoutersServiceProvider,
    MiddlewaresServiceProvider,
]
