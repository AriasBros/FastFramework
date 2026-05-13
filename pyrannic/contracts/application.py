from abc import ABC, abstractmethod

from fastapi import FastAPI

from pyrannic.contracts.container.container import ContainerInterface


class ApplicationInterface(ABC, FastAPI):
    @property
    @abstractmethod
    def container(self) -> ContainerInterface:
        pass
