from pydantic import Field

from pyrannic.config.configuration import Configuration


class Foo(Configuration):
    name: str = Field(default="Pyrannic")
    env: str = Field(default="production")
    debug: bool = Field(default=False)
