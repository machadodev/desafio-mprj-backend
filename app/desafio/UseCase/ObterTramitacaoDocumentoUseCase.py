from dependency_injector.wiring import inject, Provide
from desafio.containers import Container
from desafio.helper import hashString
from desafio.Services.Protocols import CacheService, DatabaseService, LogService, TJRJService

class ObterTramitacaoDocumentoUseCase:  
    # Dependencies injection
    def __init__(self, 
                 databaseService : DatabaseService, 
                 TJRJService : TJRJService):
        self.databaseService = databaseService
        self.TJRJService = TJRJService
    
    def obterTramitacaoDocumento(self, documento):
        tramitacao = None
                
        # ii
        dados_documento = self.databaseService.findDocumento(documento)       
        
        # iii
        tramitacao = self.TJRJService.findTramitacao(dados_documento)

        return tramitacao

class ObterTramitacaoDocumentoUseCaseLoggerDecorator(ObterTramitacaoDocumentoUseCase):
    def __init__(self, 
                 databaseService : DatabaseService, 
                 TJRJService : TJRJService,
                 logService : LogService):
        super().__init__(databaseService, TJRJService)
        self.databaseService = databaseService
        self.TJRJService = TJRJService
        self.logService = logService        

    def obterTramitacaoDocumento(self, request, documento):
        tramitacao = super().obterTramitacaoDocumento(documento)
        
        # iv - make log
        self.logService.record(request, tramitacao)
        
        return tramitacao

class ObterTramitacaoDocumentoUseCaseCacheDecorator(ObterTramitacaoDocumentoUseCaseLoggerDecorator):
    def __init__(self, 
                 databaseService : DatabaseService, 
                 TJRJService : TJRJService,
                 logService : LogService,
                 cacheService : CacheService):
        super().__init__(databaseService, TJRJService, logService)
        self.databaseService = databaseService
        self.TJRJService = TJRJService
        self.logService = logService
        self.cacheService = cacheService        
    
    def obterTramitacaoDocumento(self, request, documento):        
        tramitacao = self.cacheService.get(documento)
        
        if tramitacao is None:           
            tramitacao = super().obterTramitacaoDocumento(request, documento)
            self.cacheService.set(documento, tramitacao)
        
        return tramitacao

@inject
def handler(request, 
            documento,
            database_service : DatabaseService = Provide[Container.database_service],
            tjrj_service : TJRJService = Provide[Container.tjrj_service],
            log_service : LogService = Provide[Container.log_service],
            cache_service : CacheService = Provide[Container.cache_service]):
    
    instance = ObterTramitacaoDocumentoUseCaseCacheDecorator(database_service, tjrj_service, log_service, cache_service)
    
    return instance.obterTramitacaoDocumento(request, documento)   

@inject
def handlerScheduled(
            database_service : DatabaseService = Provide[Container.database_service],
            tjrj_service : TJRJService = Provide[Container.tjrj_service],
            cache_service : CacheService = Provide[Container.cache_service]):
    
    TramitacoesObservadas = [{ "id": 1, "hash": '777c6d651d8f956c519dcec7ff2457e1' }]
    
    for tramitacao in TramitacoesObservadas:
        usecase = ObterTramitacaoDocumentoUseCase(database_service, tjrj_service)
        documento_tramitacao = usecase.obterTramitacaoDocumento(tramitacao)
        
        hash_documento_tramitacao = hashString(documento_tramitacao)
        
        if tramitacao['hash'] != hash_documento_tramitacao:            
            print("Documento atualizado:", documento_tramitacao)           
        else:
            print("Documento nao teve alteracoes")