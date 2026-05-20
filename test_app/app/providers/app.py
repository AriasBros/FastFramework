from app.services.foo import FooService, FooServiceInterface

from pyrannic import ServiceProvider


class AppServiceProvider(ServiceProvider):
    __bindings__ = {
        FooServiceInterface: FooService,
    }
