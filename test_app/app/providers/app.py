from fastframework.bootstrap.service_provider import ServiceProvider

from app.services.foo import FooService, FooServiceInterface


class AppServiceProvider(ServiceProvider):
    __bindings__ = {
        FooServiceInterface: FooService,
    }
