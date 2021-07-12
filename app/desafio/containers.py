from dependency_injector import containers, providers
from .services import DatabaseService
from .services import TJRJService
from .services import LogService
from .services import CacheService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()  
    database_service : DatabaseService = providers.Singleton(DatabaseService)
    tjrj_service : TJRJService = providers.Singleton(TJRJService)
    log_service : LogService = providers.Singleton(LogService)
    cache_service : CacheService = providers.Singleton(CacheService)

