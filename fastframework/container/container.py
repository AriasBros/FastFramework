from collections.abc import Callable
from inspect import isclass
from types import FunctionType
from typing import Any

from fastframework.contracts.application import ApplicationInterface
from fastframework.contracts.container.container import ContainerInterface
from fastframework.dependency_injection.resolvers import resolve


class Container(ContainerInterface):
    _bindings: dict[str | type, Callable[..., Any]]
    _instances: dict[str | type, object]
    _aliases: dict[str | type, str | type]

    def __init__(self, app: ApplicationInterface):
        self._app = app
        self._bindings = {}
        self._instances = {}
        self._aliases = {}

    def bind(
        self,
        abstract: str | type,
        concrete: type[Any] | Callable[..., Any],
    ) -> None:
        self._dropStaleInstances(abstract)

        if isclass(concrete):
            concrete = self._get_closure(abstract, concrete)

        if not isinstance(concrete, FunctionType):
            raise ValueError("Concrete must be a class or a callable")

        self._bindings[abstract] = concrete

    def is_bound(self, abstract: str | type) -> bool:
        abstract = self.get_alias(abstract)
        return abstract in self._bindings

    async def resolve(self, abstract: str | type) -> Any:
        abstract = self.get_alias(abstract)

        if abstract in self._instances:
            return self._instances[abstract]

        if abstract not in self._bindings:
            raise ValueError(f"No binding found for {abstract}")

        concrete: Callable[..., Any] = self._bindings[abstract]
        instance: Any = await concrete(self._app)

        self._instances[abstract] = instance

        return instance

    def resolved(self, abstract: str | type) -> bool:
        abstract = self.get_alias(abstract)
        return abstract in self._instances

    def set_alias(self, abstract: str | type, alias: str | type) -> None:
        if alias == abstract:
            raise ValueError(f"{abstract} cannot be aliased to itself.")

        self._aliases[alias] = abstract

    def is_alias(self, alias: str | type) -> bool:
        return alias in self._aliases

    def get_alias(self, abstract: str | type) -> str | type:
        return (
            self.get_alias(self._aliases[abstract])
            if self.is_alias(abstract)
            else abstract
        )

    def flush(self) -> None:
        self._bindings.clear()
        self._instances.clear()
        self._aliases.clear()

    def _dropStaleInstances(self, abstract: str | type) -> None:
        """Drop all of the stale instances and aliases."""
        if abstract in self._instances:
            del self._instances[abstract]

        if abstract in self._aliases:
            del self._aliases[abstract]

    def _get_closure(
        self,
        abstract: str | type,
        concrete: type[Any],
    ) -> Callable[..., Any]:
        async def closure(app: ApplicationInterface) -> Any:
            return await resolve(concrete, app=app)

        return closure
