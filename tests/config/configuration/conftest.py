import pytest

from tests.config.configuration.foo import Foo
from tests.config.configuration.foo_config import FooConfig


@pytest.fixture(scope="module")
def foo() -> Foo:
    return Foo()


@pytest.fixture(scope="module")
def foo_config() -> FooConfig:
    return FooConfig()
