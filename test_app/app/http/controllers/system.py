from typing import Annotated

from fastapi import APIRouter
from fastframework.container import Resolves

from app.services.foo import FooServiceInterface

router = APIRouter(tags=["System"])


@router.get(
    "/status",
    summary="Status Endpoint",
    description="Endpoint to check the status of the application.",
)
async def status(service: Annotated[FooServiceInterface, Resolves()]) -> dict[str, str]:
    """
    Endpoint to get the status of the application.

    Returns:
        A dictionary with the status of the application.
    """

    return {"app_name": service.get_app_name()}
