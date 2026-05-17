from typing import Type

from app.providers.app import AppServiceProvider

from pyrannic import (
    DatabaseServiceProvider,
    MiddlewaresServiceProvider,
    RoutersServiceProvider,
    ExceptionHandlersProvider,
    ServiceProvider,
)

providers: list[Type[ServiceProvider]] = [
    ExceptionHandlersProvider,
    AppServiceProvider,
    DatabaseServiceProvider,
    RoutersServiceProvider,
    MiddlewaresServiceProvider,
]
