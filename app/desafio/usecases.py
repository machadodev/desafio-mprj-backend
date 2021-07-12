from dependency_injector.wiring import inject, Provide
from .containers import Container
from .services import *

class ObterTramitacaoDocumentoUseCase:  
    # Dependencies injection
    def __init__(self, 
                 databaseService : DatabaseService, 
                 TJRJService : TJRJService,
                 cacheService: CacheService,
                 logService : LogService):
        self.databaseService = databaseService
        self.TJRJService = TJRJService
        self.cacheService = cacheService
        self.logService = logService
    
    def obterTramitacaoDocumento(self, request, documento):
        tramitacao = None
        
        self.logService.record(request, "TESTE LOGGER")
                
        # ii
        dados_documento = self.databaseService.findDocumento(documento)       
        
        # iii
        tramitacao = self.TJRJService.findTramitacao(dados_documento)
        
        # iv
        self.logService.record(request, tramitacao)
        
        return tramitacao

        

@inject
def handler(request, 
            doc,
            database_service : DatabaseService = Provide[Container.database_service],
            tjrj_service : TJRJService = Provide[Container.tjrj_service],
            log_service : LogService = Provide[Container.log_service],
            cache_service: CacheService= Provide[Container.cache_service]):
  
    usecase = ObterTramitacaoDocumentoUseCase(database_service, tjrj_service, cache_service, log_service)
    
    return usecase.obterTramitacaoDocumento(request, doc)
