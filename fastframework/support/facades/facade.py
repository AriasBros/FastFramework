from typing import Any

from fastframework.contracts.application import ApplicationInterface


class FacadeMetaclass(type):
    def __getattr__(cls, key: str) -> Any:
        instance = cls._get_facade_root()
        return getattr(instance, key)


class Facade(metaclass=FacadeMetaclass):
    _app: ApplicationInterface | None = None
    """The application instance being facaded."""

    _cached: bool = True
    """Indicates if the resolved instance should be cached."""

    _resolved_instances: dict[str, Any] = {}
    """The resolved object instances."""

    @classmethod
    def _get_facade_root(cls) -> Any:
        return cls._resolve_facade_instance(cls._get_facade_accessor())

    @classmethod
    def _get_facade_accessor(cls) -> str:
        raise NotImplementedError(
            "Facade subclasses must implement the _get_facade_accessor method."
        )

    @classmethod
    def _resolve_facade_instance(cls, name: str) -> Any:
        if name in cls._resolved_instances:
            return cls._resolved_instances[name]

        if cls._app is not None:
            instance = cls._app.container.instance(name)

            if cls._cached:
                cls._resolved_instances[name] = instance

            return instance

    @classmethod
    def set_facade_application(cls, app: ApplicationInterface) -> None:
        cls._app = app
