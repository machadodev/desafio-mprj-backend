from dependency_injector.wiring import inject, Provide

from .containers import Container
from .services import *

class ObterTramitacaoDocumentoUseCase:  
    # Dependencies injection
    def __init__(self, 
                 databaseService : DatabaseService, 
                 TJRJService : TJRJService,
                 logService : LogService):
        self.databaseService = databaseService
        self.TJRJService = TJRJService
        self.logService = logService
    
    def obterTramitacaoDocumento(self, request, documento):
        tramitacao = None
                
        # ii
        dados_documento = self.databaseService.findDocumento(documento)       
        
        # iii
        tramitacao = self.TJRJService.findTramitacao(dados_documento)
        
        # iv
        #self.logService.record(request, tramitacao)
        
        return tramitacao


@inject
def handler(request, 
            doc,
            database_service : DatabaseService = Provide[Container.database_service],
            tjrj_service : TJRJService = Provide[Container.tjrj_service],
            log_service : LogService = Provide[Container.log_service]):
    
    usecase = ObterTramitacaoDocumentoUseCase(database_service, tjrj_service, log_service)
    
    return usecase.obterTramitacaoDocumento(request, doc)
