from typing import Annotated, TypeVar

from pyrannic.container.decorators import scoped as scoped
from pyrannic.container.decorators import singleton as singleton
from pyrannic.container.param_functions import Resolves
from pyrannic.contracts.application import ApplicationInterface
from pyrannic.contracts.container.container import ContainerInterface

T = TypeVar("T")

Resolve = Annotated[T, Resolves()]
Container = Resolve[ContainerInterface]
App = Resolve[ApplicationInterface]
