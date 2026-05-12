from fastframework.support.facades.facade import Facade


class Config(Facade):
    @classmethod
    def _get_facade_accessor(cls) -> str:
        return "config"
