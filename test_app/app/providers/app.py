from app.services.foo import FooService, FooServiceInterface

from pyrannic.bootstrap.service_provider import ServiceProvider


class AppServiceProvider(ServiceProvider):
    __bindings__ = {
        FooServiceInterface: FooService,
    }
