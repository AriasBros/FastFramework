from collections.abc import Callable
from contextlib import AsyncExitStack
import inspect
from types import FunctionType
from typing import Any, Awaitable, TypeVar, cast

from fastapi import Request
from fastapi.concurrency import run_in_threadpool
from fastapi.exceptions import RequestValidationError
from fastapi.types import DependencyCacheKey

from pyrannic.container.contextual_binding_builder import ContextualBindingBuilder
from pyrannic.contracts.application import ApplicationInterface
from pyrannic.contracts.container.container import ContainerInterface
from pyrannic.contracts.container.contextual_binding_builder import (
    ContextualBindingBuilderInterface,
)
from pyrannic.support.reflection import is_interface

from fastapi.dependencies.utils import (
    get_dependant,
    solve_dependencies,
    SolvedDependency,
)
from fastapi.dependencies.models import Dependant

T = TypeVar("T")


class Binding:
    def __init__(
        self,
        concrete: Callable[..., Any],
        shared: bool = False,
    ) -> None:
        self.concrete = concrete
        self.shared = shared


class Container(ContainerInterface):
    _app: ApplicationInterface
    _bindings: dict[str, Binding]
    _instances: dict[str, Any]
    _aliases: dict[str, str | type]
    _scoped_instances: list[str]
    _contextual: dict[str, dict[str, Binding]]
    _build_stack: list[str]
    _dependency_cache: dict[DependencyCacheKey, Any]

    def __init__(self, app: ApplicationInterface):
        self._app = app
        self._bindings = {}
        self._instances = {}
        self._scoped_instances = []
        self._aliases = {}
        self._contextual = {}
        self._build_stack = []
        self._dependency_cache = {}

    def _abstract_to_str(self, abstract: str | type) -> str:
        if isinstance(abstract, str):
            return abstract
        else:
            return f"{abstract.__qualname__}:{inspect.getfile(abstract)}"

    def bind(
        self,
        abstract: str | type,
        concrete: type[Any] | Callable[..., Any],
        shared: bool = False,
    ) -> None:
        abstract = self._abstract_to_str(abstract)
        self._drop_stale_instances(abstract)

        if inspect.isclass(concrete):
            concrete = self._get_closure(concrete)

        if not isinstance(concrete, FunctionType):
            raise RequestValidationError("Concrete must be a class or a callable")

        self._bindings[abstract] = Binding(concrete, shared)

    def bind_if(
        self,
        abstract: str | type,
        concrete: type[Any] | Callable[..., Any],
        shared: bool = False,
    ) -> None:
        if not self.is_bound(abstract):
            self.bind(abstract, concrete, shared)

    def scoped(
        self,
        abstract: str | type,
        concrete: type[Any] | Callable[..., Any],
    ) -> None:
        self._scoped_instances.append(self._abstract_to_str(abstract))
        self.singleton(abstract, concrete)

    def scoped_if(
        self,
        abstract: str | type,
        concrete: type[Any] | Callable[..., Any],
    ) -> None:
        if not self.is_bound(abstract):
            self.scoped(abstract, concrete)

    def singleton(
        self,
        abstract: str | type,
        concrete: type[Any] | Callable[..., Any],
    ) -> None:
        self.bind(abstract, concrete, True)

    def singleton_if(
        self,
        abstract: str | type,
        concrete: type[Any] | Callable[..., Any],
    ) -> None:
        if not self.is_bound(abstract):
            self.singleton(abstract, concrete)

    def instance(self, abstract: str | type[T], instance: T | None = None) -> T:
        if instance is None:
            abstract = self.get_alias(abstract)
            instance = self._instances.get(abstract)

            if not instance:
                raise ValueError(f"No instance found for {abstract}")

            return instance
        else:
            abstract = self._abstract_to_str(abstract)
            self._drop_stale_instances(abstract)
            self._instances[abstract] = instance

            return instance

    def add_contextual_binding(
        self,
        concrete: str,
        abstract: str | type,
        implementation: type | Callable[..., Any],
    ) -> None:
        abstract_key = self._abstract_to_str(abstract)

        if concrete not in self._contextual:
            self._contextual[concrete] = {}

        if inspect.isclass(implementation):
            implementation = self._get_closure(implementation)

        self._contextual[concrete][abstract_key] = Binding(implementation)

    def when(self, concrete: type | list[type]) -> ContextualBindingBuilderInterface:
        concretes = [concrete] if not isinstance(concrete, list) else concrete
        concrete_keys = [self._abstract_to_str(c) for c in concretes]

        return ContextualBindingBuilder(self, concrete_keys)

    def is_bound(self, abstract: str | type) -> bool:
        abstract = self._abstract_to_str(abstract)
        return abstract in self._bindings or self.is_alias(abstract)

    async def resolve(
        self,
        abstract: str | type[T],
        request: Request | None = None,
    ) -> T:
        binding_key = self.get_alias(abstract)
        concrete = self._get_contextual_concrete(abstract)

        self._build_stack.append(binding_key)

        try:
            if not concrete and binding_key in self._instances:
                return self._instances[binding_key]

            if not concrete:
                concrete = self._get_concrete(abstract)

            instance = await concrete(self._app, request)

            if self._is_shared(binding_key, abstract):
                self._instances[binding_key] = instance

            return instance
        finally:
            self._build_stack.pop()

    def _is_shared(self, binding_key: str, abstract: str | type[T]) -> bool:
        binding_key = self._abstract_to_str(abstract)

        if binding_key in self._instances:
            return True

        if binding_key in self._bindings and self._bindings[binding_key].shared:
            return True

        binding_type = self._get_binding_type(abstract)

        if binding_type == "scoped" and binding_key not in self._scoped_instances:
            self._scoped_instances.append(binding_key)

        return True if binding_type in ("singleton", "scoped") else False

    def _get_binding_type(self, abstract: str | type[T]) -> str | None:
        if isinstance(abstract, str):
            return None

        binding_type = getattr(abstract, "__pyrannic_binding_type__", None)

        return binding_type

    def _get_contextual_concrete(
        self,
        abstract: str | type,
    ) -> Callable[..., Any] | None:
        binding_key = self._abstract_to_str(abstract)
        last_concrete = self._build_stack[-1] if self._build_stack else None

        if last_concrete and last_concrete in self._contextual:
            contextual_bindings = self._contextual[last_concrete]
            if binding_key in contextual_bindings:
                return contextual_bindings[binding_key].concrete

        return None

    def _get_concrete(self, abstract: str | type[T]) -> Callable[..., Any]:
        concrete: Callable[..., Any]
        binding_key = self._abstract_to_str(abstract)

        if binding_key not in self._bindings:
            if isinstance(abstract, str):
                raise RequestValidationError(f"No binding found for key {abstract}")
            elif is_interface(abstract):
                raise RequestValidationError(
                    f"No binding found for interface {abstract.__name__}"
                )
            else:
                concrete = self._get_closure(abstract)
        else:
            concrete = self._bindings[binding_key].concrete

        return concrete

    async def call(self, callback: type[T] | Callable[..., Any]) -> T:
        return await self._resolve(callback, self._app)

    def resolved(self, abstract: str | type[T]) -> bool:
        abstract = self.get_alias(abstract)
        return abstract in self._instances

    def set_alias(self, abstract: str | type, alias: str | type) -> None:
        abstract = self._abstract_to_str(abstract)
        alias = self._abstract_to_str(alias)

        if alias == abstract:
            raise ValueError(f"{abstract} cannot be aliased to itself.")

        self._aliases[alias] = abstract

    def is_alias(self, alias: str | type) -> bool:
        alias = self._abstract_to_str(alias)
        return alias in self._aliases

    def get_alias(self, abstract: str | type) -> str:
        abstract = self._abstract_to_str(abstract)

        return (
            self.get_alias(self._aliases[abstract])
            if self.is_alias(abstract)
            else abstract
        )

    def flush(self) -> None:
        self._bindings.clear()
        self._instances.clear()
        self._aliases.clear()
        self._scoped_instances.clear()
        self._dependency_cache.clear()

    def forget_scoped_instances(self) -> None:
        """Clear all of the scoped instances from the container."""
        for abstract in self._scoped_instances:
            if abstract in self._instances:
                del self._instances[abstract]

    def _drop_stale_instances(self, abstract: str) -> None:
        """Drop all of the stale instances and aliases."""
        if abstract in self._instances:
            del self._instances[abstract]

        if abstract in self._aliases:
            del self._aliases[abstract]

    def _get_closure(
        self, concrete: type[T]
    ) -> Callable[[ApplicationInterface, Request], Awaitable[T]]:
        async def closure(app: ApplicationInterface, request: Request) -> T:
            return await self._resolve(concrete, app, request)

        return closure

    async def _solve_dependencies(
        self,
        request: Request,
        dependant: Dependant,
    ) -> SolvedDependency:
        return await solve_dependencies(
            request=request,
            dependant=dependant,
            embed_body_fields=False,
            dependency_cache=self._dependency_cache,
            # TODO: Remove async_exit_stack, no longer used.
            async_exit_stack=cast(AsyncExitStack, None),
        )

    async def _resolve(
        self,
        callback: type[T] | Callable[..., Any],
        app: ApplicationInterface,
        request: Request | None = None,
        **kwargs: Any,
    ) -> T:
        dependant = get_dependant(path="/", call=callback, scope="function")

        if not request:
            async with AsyncExitStack() as context_manager:
                dependencies = await self._solve_dependencies(
                    self._fallback_request(app, context_manager),
                    dependant,
                )

                return await self._resolve_dependant(
                    dependant,
                    dependencies,
                    **kwargs,
                )
        else:
            dependencies = await self._solve_dependencies(request, dependant)
            return await self._resolve_dependant(dependant, dependencies, **kwargs)

    async def _resolve_dependant(
        self,
        dependant: Dependant,
        dependencies: SolvedDependency,
        **kwargs: Any,
    ) -> Any:
        assert dependant.call  # For types

        if inspect.iscoroutinefunction(dependant.call):
            result = await dependant.call(**dependencies.values, **kwargs)
        else:
            result = await run_in_threadpool(
                dependant.call,
                **dependencies.values,
                **kwargs,
            )

        return result

    def _fallback_request(
        self, app: ApplicationInterface, context_manager: AsyncExitStack
    ) -> Request:
        """Generate a fallback request to be used when no request is available in the context of resolution."""
        return Request(
            {
                "app": app,
                "type": "http",
                "method": "GET",
                "path": "/",
                "headers": [],
                "query_string": b"",
                "fastapi_inner_astack": context_manager,
                "fastapi_function_astack": context_manager,
            }
        )
