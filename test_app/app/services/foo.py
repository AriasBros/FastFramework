from abc import ABC, abstractmethod


class FooServiceInterface(ABC):
    @abstractmethod
    def get_app_name(self) -> str:
        pass


class FooService(FooServiceInterface):
    def __init__(self):
        self.app_name = "FastApp"

    def get_app_name(self) -> str:
        return self.app_name
