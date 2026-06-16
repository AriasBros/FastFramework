import inspect
from contextlib import AsyncExitStack
from typing import Any, Callable, List, TypeVar

from fastapi.concurrency import run_in_threadpool
from fastapi.dependencies.utils import (
    SolvedDependency,
    get_dependant,
    solve_dependencies,
)
from fastapi.exceptions import ValidationException
from starlette.requests import Request

from pyrannic.contracts.application import ApplicationInterface


T = TypeVar("T")


# https://stackoverflow.com/a/78279023
# https://github.com/fastapi/fastapi/discussions/7720
async def resolve_dependant(
    command: Callable[..., Any],
    name: str | None = None,
    request: Request | None = None,
    security_scopes: list[str] | None = None,
    app: ApplicationInterface | None = None,
    **kwargs: Any,
) -> Any:
    """Given a callable, will solve its dependencies and run it."""

    async with AsyncExitStack() as cm:
        name = name or command.__name__
        path = request.url.path if request else f"command:{name}"

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
            name=name,
            path=path,
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
            result = await run_in_threadpool(
                dependant.call,
                **dependencies.values,
                **kwargs,
            )

        return result

    return None


def _should_raise_errors(errors: List[Any]) -> bool:
    if not errors or len(errors) == 0:
        return False

    if len(errors) > 1:
        return False

    return "kwargs" not in errors[0]["loc"]
