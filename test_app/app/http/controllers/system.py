from typing import Annotated

from app.services.foo import FooServiceInterface
from fastapi import APIRouter

from pyrannic import Config, Paginator, Resolves
from test_app.app.http.resources.foo import Foo, FooCollection

router = APIRouter(tags=["System"])


@router.get(
    "/status",
    summary="Status Endpoint",
    description="Endpoint to check the status of the application.",
)
async def status(service: Annotated[FooServiceInterface, Resolves()]) -> dict[str, str]:
    return {"app_name": Config.get("app.name"), "status": "ok"}


@router.get(
    "/status2",
    summary="Status Endpoint",
    description="Endpoint to check the status of the application.",
)
async def status2() -> FooCollection:
    items = Paginator(
        [
            Foo(name="status", description="The application is running smoothly."),
            Foo(
                name="uptime",
                description="The application has been running for 24 hours.",
            ),
        ]
    )

    return FooCollection(items)
