import os
from dependency_injector import containers, providers
from .services import *


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    database_service : DatabaseService = providers.Singleton(MockExternalDatabaseService)
    tjrj_service : TJRJService = providers.Singleton(MockTJRJSOAPService, os.environ.get("ACCESS_TOKEN_TJRJ", default=''))
    log_service : LogService = providers.Factory(KafkaLoggerService)
    cache_service : CacheService = providers.Singleton(RedisService)
