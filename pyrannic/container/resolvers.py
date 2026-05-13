import asyncio
import inspect
from contextlib import AsyncExitStack
from typing import Any, Callable, List, Optional, Type, TypeVar

from fastapi import FastAPI
from fastapi.dependencies.utils import (
    SolvedDependency,
    get_dependant,
    solve_dependencies,
)
from fastapi.exceptions import ValidationException
from starlette.requests import Request

T = TypeVar("T")


async def resolve(
    class_type: Type[T],
    request: Request | None = None,
    security_scopes: Optional[List[str]] = None,
    app: FastAPI | None = None,
) -> T:
    return await resolve_dependant(
        class_type,
        class_type.__name__,
        request,
        security_scopes=security_scopes,
        app=app,
    )


# TODO
async def resolve_provider(
    provider_class: Type[T],
    request: Request,
    security_scopes: Optional[List[str]] = None,
) -> T:
    provider = await resolve(provider_class, request, security_scopes=security_scopes)

    if hasattr(provider, "boot") and callable(getattr(provider, "boot")):
        result = provider.boot()

        if asyncio.iscoroutine(result):
            await result

    return provider


# https://stackoverflow.com/a/78279023
# https://github.com/fastapi/fastapi/discussions/7720
async def resolve_dependant(
    command: Callable[..., Any],
    name: str | None = None,
    request: Request | None = None,
    security_scopes: Optional[List[str]] = None,
    app: FastAPI | None = None,
    **kwargs: Any,
) -> Any:
    """Given a callable, will solve its dependencies and run it."""

    async with AsyncExitStack() as cm:
        request = request or Request(
            {
                "app": app,
                "type": "http",
                "method": "GET",
                "path": "/",
                "headers": [],
                "query_string": b"",
                "fastapi_astack": cm,  # To support older FastAPI versions
                "fastapi_inner_astack": cm,
                "fastapi_function_astack": cm,
            }
        )

        dependant = get_dependant(
            path=f"command:{name or command.__name__}",
            call=command,
            own_oauth_scopes=security_scopes,
        )

        dependencies: SolvedDependency = await solve_dependencies(
            request=request,
            dependant=dependant,
            async_exit_stack=cm,
            dependency_overrides_provider=request.app,
            embed_body_fields=True,
        )

        if _should_raise_errors(dependencies.errors):
            raise ValidationException(dependencies.errors)

        if not dependant.call:
            raise ValueError("Could not find a callable to run")

        if inspect.iscoroutinefunction(dependant.call):
            result = await dependant.call(**dependencies.values, **kwargs)
        else:
            result = dependant.call(**dependencies.values, **kwargs)

        return result

    return None


def _should_raise_errors(errors: List[Any]) -> bool:
    if not errors or len(errors) == 0:
        return False

    if len(errors) > 1:
        return False

    return "kwargs" not in errors[0]["loc"]
