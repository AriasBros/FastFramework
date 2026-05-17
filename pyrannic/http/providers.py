from fastapi import APIRouter

from pyrannic.bootstrap.service_provider import ServiceProvider
from pyrannic.container.utils import (
    get_attrs,
    get_class,
    get_functions,
    get_modules,
    import_modules,
)
from pyrannic.http.exceptions.exception import handle_exception
from pyrannic.http.exceptions.resource_not_found import (
    ResourceNotFoundException,
    handle_resource_not_found_exception,
)
from pyrannic.http.exceptions.unprocessable_entity import (
    UnprocessableEntityException,
    handle_unprocessable_entity_exception,
)


class RoutersServiceProvider(ServiceProvider):
    def register(self):
        modules = get_modules("app/http/routers")
        routers: list[APIRouter] = get_attrs(modules, "router")

        for router in routers:
            self.app.include_router(router)


class MiddlewaresServiceProvider(ServiceProvider):
    def register(self):
        for module_path, module in import_modules("app/http/middlewares"):
            middleware = get_class(
                module,
                module_path=module_path,
                class_suffix="Middleware",
            )

            if middleware:
                self.app.add_middleware(middleware)
            else:
                for _, middleware in get_functions(
                    module,
                    lambda name: not name.startswith("_"),
                ):
                    self.app.middleware("http")(middleware)


class ExceptionHandlersProvider(ServiceProvider):
    def register(self):
        self.app.add_exception_handler(
            UnprocessableEntityException, handle_unprocessable_entity_exception
        )
        self.app.add_exception_handler(
            ResourceNotFoundException, handle_resource_not_found_exception
        )
        self.app.add_exception_handler(Exception, handle_exception)
