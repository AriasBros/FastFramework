from pyrannic.contracts.application import ApplicationInterface
from pyrannic.contracts.container.container import ContainerInterface
from pyrannic.support.facades.facade import Facade


class App(Facade[ApplicationInterface]):
    @classmethod
    def _get_facade_accessor(cls) -> str:
        return "app"

    @classmethod
    def container(cls) -> ContainerInterface:
        return cls.call("container")
