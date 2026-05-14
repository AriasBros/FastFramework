from typing import Any

from pydantic_settings import BaseSettings

from pyrannic.contracts.config.config import ConfigInterface


class Configuration(ConfigInterface, BaseSettings):
    def __init__(self) -> None:
        super().__init__(_case_sensitive=False, _env_prefix=self.env_prefix)

    @property
    def config_key(self) -> str:
        return self.__class__.__name__.replace("Config", "").lower()

    @property
    def env_prefix(self) -> str:
        return f"{self.config_key.upper()}_"

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump()
