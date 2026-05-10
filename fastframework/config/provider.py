from fastframework.bootstrap.app_state_service_provider import AppStateServiceProvider
from fastframework.config.base_config import BaseConfig
from fastframework.config.respository import ConfigRepository
from fastframework.container.utils import get_classes, get_modules


class ConfigRepositoryProvider(AppStateServiceProvider[ConfigRepository]):
    def create(self) -> ConfigRepository:
        repo = ConfigRepository()

        modules = get_modules("config")
        classes = get_classes(modules, "Config")

        for cls in classes:
            instance: BaseConfig = cls()
            repo.set_all(instance)

        return repo
