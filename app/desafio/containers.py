import os
from dependency_injector import containers, providers
from desafio.Services.Protocols import DatabaseService, CacheService, LogService, TJRJService
from desafio.Services.Infrastructure import RedisCacheService, KafkaLoggerService, MockTJRJSOAPService, MockExternalDatabaseService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    cache_service : CacheService = providers.Factory(RedisCacheService, int(os.environ.get("CACHE_TTL_IN_SECONDS", default=10)))    
    tjrj_service : TJRJService = providers.Factory(MockTJRJSOAPService, os.environ.get("ACCESS_TOKEN_TJRJ", default=''))
    log_service : LogService = providers.Singleton(KafkaLoggerService)
    database_service : DatabaseService = providers.Factory(MockExternalDatabaseService)
