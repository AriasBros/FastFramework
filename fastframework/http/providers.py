from fastapi import APIRouter

from fastframework.bootstrap.service_provider import ServiceProvider
from fastframework.container.utils import (
    get_attrs,
    get_class,
    get_functions,
    get_modules,
    import_modules,
)


class RoutersServiceProvider(ServiceProvider):
    def register(self):
        modules = get_modules("app/http/controllers")
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
