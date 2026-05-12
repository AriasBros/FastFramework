from fastframework.bootstrap.instance_service_provider import InstanceServiceProvider
from fastframework.config.base_config import BaseConfig
from fastframework.config.respository import ConfigRepository
from fastframework.container.utils import get_classes, get_modules
from fastframework.contracts.config.respository import ConfigRepositoryInterface


class ConfigRepositoryProvider(InstanceServiceProvider[ConfigRepositoryInterface]):
    @property
    def aliases(self) -> list[str | type] | None:
        return ["config"]

    def create(self) -> ConfigRepositoryInterface:
        repo = ConfigRepository()

        modules = get_modules("config")
        classes = get_classes(modules, "Config")

        for cls in classes:
            instance: BaseConfig = cls()
            repo.set(instance.config_key, instance.model_dump())

        return repo
