from dependency_injector import containers, providers
from infrastructure.settings import Settings

class Container(containers.DeclarativeContainer):
    config: Settings = providers.Configuration()