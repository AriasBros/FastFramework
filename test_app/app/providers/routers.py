from fastframework.bootstrap.service_provider import ServiceProvider

from app.http.controllers.system import router as system_router


class RoutersProvider(ServiceProvider):
    def register(self):
        self.app.include_router(system_router)
