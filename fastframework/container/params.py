from collections.abc import Callable
import inspect
from typing import Any, Literal

from fastapi.params import Depends

from fastframework.contracts.http.request import RequestInterface


class Resolves(Depends):
    def __init__(
        self,
        dependency: str | type | Callable[..., Any] | None = None,
        use_cache: bool = True,
        scope: Literal["function", "request"] | None = None,
    ):
        if isinstance(dependency, str) or inspect.isclass(dependency):
            dependency = self._get_dependency(dependency)

        super().__init__(dependency=dependency, use_cache=use_cache, scope=scope)

    def _get_dependency(self, abstract: str | type) -> Callable[..., Any]:
        async def dependency(request: RequestInterface) -> Any:
            return await request.app.container.resolve(abstract)

        return dependency
