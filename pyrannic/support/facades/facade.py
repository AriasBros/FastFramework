from typing import Any, Generic

from annotated_types import T

from pyrannic.contracts.application import ApplicationInterface


class FacadeMetaclass(type):
    def __getattr__(cls, key: str) -> Any:
        instance = cls._get_facade_root()
        return getattr(instance, key)


class Facade(Generic[T], metaclass=FacadeMetaclass):
    _app: ApplicationInterface | None = None
    """The application instance being facaded."""

    @classmethod
    def call(cls, name: str, *args: Any, **kwargs: Any) -> Any:
        instance = cls._get_facade_root()
        return getattr(instance, name)(*args, **kwargs)

    @classmethod
    def _get_facade_root(cls) -> T:
        return cls._resolve_facade_instance(cls._get_facade_accessor())

    @classmethod
    def _get_facade_accessor(cls) -> str:
        raise NotImplementedError(
            "Facade subclasses must implement the _get_facade_accessor method."
        )

    @classmethod
    def _resolve_facade_instance(cls, name: str) -> T:
        assert cls._app is not None, "Facade application instance has not been set."
        return cls._app.container.instance(name)

    @classmethod
    def set_facade_application(cls, app: ApplicationInterface) -> None:
        cls._app = app
