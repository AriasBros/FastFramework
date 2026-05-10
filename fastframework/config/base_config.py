from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    def __init__(self) -> None:
        super().__init__(_case_sensitive=False, _env_prefix=self.env_prefix)

    @property
    def env_prefix(self) -> str:
        return f"{self.__class__.__name__.replace('Config', '').upper()}_"
