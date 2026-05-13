from pyrannic.bootstrap.instance_service_provider import InstanceServiceProvider
from pyrannic.config.base_config import BaseConfig
from pyrannic.config.respository import ConfigRepository
from pyrannic.container.utils import get_classes, get_modules
from pyrannic.contracts.config.respository import ConfigRepositoryInterface


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
