import json
from enum import Enum
from dependency_injector.wiring import inject, Provide
from desafio.containers import Container
from desafio.helper import hashString
from desafio.Services.Protocols import CacheService, DatabaseService, LogService, TJRJService, EmailService

from desafio.models import Documento,UsuarioObservers
from django.contrib.auth.models import User

class ObterTramitacoesUseCase:
    
    # Construtor
    # Dependencies injection
    def __init__(self, 
                 databaseService : DatabaseService, 
                 TJRJService : TJRJService):
        self.databaseService = databaseService
        self.TJRJService = TJRJService

    class Action(Enum):
        NO_ACTION = 1
        UPDATED = 2
        CREATED = 3
        
    # Esta função atualiza ou cria uma tripla: (id_documento, id_tjrj, hash_tramitacao)
    # Dessa forma sempre que é feito uma requisição de tramitações, é feito um hash
    # Isso permite saber se desde o último acesso o arquivo mudou.
    def atualizaHashTramitacoesBanco(self, numero_documento, id_tjrj, tramitacoes):
                
        hash = hashString(json.dumps(tramitacoes, ensure_ascii=False))
        
        obj, criado = Documento.objects.get_or_create(
            id_doc=numero_documento,
            id_tjrj=id_tjrj,
            defaults={ "hash_tramitacao" : hash}
        )
        
        action = self.Action.NO_ACTION
        
        if criado:
            action = self.Action.CREATED
        elif obj.hash_tramitacao != hash:
            action = self.Action.UPDATED
                    
        return action
    
    # Traz as tramitações em JSON
    def obterTramitacoesTJRJ(self, id_tjrj):
        return self.TJRJService.obterTramitacoes(id_tjrj)
    
    # Se escreve para mudanças no documento
    # Agora toda mudança que tiver em id_tjrj
    # o usuario_id será notificado por e-mail
    def solicitaNoticacoesDeMudancas(self, usuario_id, id_tjrj):
        usuario = User.objects.get(id=usuario_id)
        
        UsuarioObservers.objects.update_or_create(
            usuario=usuario,
            id_tjrj=id_tjrj,
            defaults={}
        )

    # Consulta o DB externo para trazer a id do TJRJ associada
    # ao numero_documento, busca as tramitações e atualiza o hash
    def obterTramitacoes(self, request, numero_documento):

        dados_documento = self.databaseService.obterDocumento(numero_documento)  
        
        usuario_id = request.user.id
        id_tjrj = dados_documento['id_tjrj']    
        
        tramitacoes = self.obterTramitacoesTJRJ(id_tjrj)        
        
        self.atualizaHashTramitacoesBanco(numero_documento, id_tjrj, tramitacoes)
        
        self.solicitaNoticacoesDeMudancas(usuario_id, id_tjrj)
        
        return tramitacoes

# DECORATOR
# Essa classe serve para estender as funcionalidades da classe original
# Nela faremos logs do request e das tramitações
class ObterTramitacoesUseCaseLoggerDecorator(ObterTramitacoesUseCase):
    def __init__(self, 
                 databaseService : DatabaseService, 
                 TJRJService : TJRJService,
                 logService : LogService):
        super().__init__(databaseService, TJRJService)
        self.databaseService = databaseService
        self.TJRJService = TJRJService
        self.logService = logService        

    def obterTramitacoes(self, request, numero_documento):          
        tramitacoes = super().obterTramitacoes(request, numero_documento)
             
        # iv - make log
        self.logService.record(request, tramitacoes)
        
        return tramitacoes

# DECORATOR
# Essa classe serve para estender as funcionalidades da classe original
# Nela faremos a configuração do CACHE para verificar se devemos devolver
# uma informaçaõ que está salva em memória ou devemos prosseguir a consulta
# nos serviços externos
class ObterTramitacoesUseCaseCacheDecorator(ObterTramitacoesUseCaseLoggerDecorator):
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
    
    def obterTramitacoes(self, request, numero_documento):
        tramitacoes = self.cacheService.get(numero_documento)
                
        if tramitacoes is None:           
            tramitacoes = super().obterTramitacoes(request, numero_documento)
            self.cacheService.set(numero_documento, tramitacoes)
        
        return tramitacoes

@inject
def handler(request, 
            numero_documento,
            database_service : DatabaseService = Provide[Container.database_service],
            tjrj_service : TJRJService = Provide[Container.tjrj_service],
            log_service : LogService = Provide[Container.log_service],
            cache_service : CacheService = Provide[Container.cache_service]):
    instance = ObterTramitacoesUseCaseCacheDecorator(database_service, tjrj_service, log_service, cache_service)
    
    return instance.obterTramitacoes(request, numero_documento)

@inject
def handlerScheduled(
            database_service : DatabaseService = Provide[Container.database_service],
            tjrj_service : TJRJService = Provide[Container.tjrj_service],
            cache_service : CacheService = Provide[Container.cache_service],
            email_service: EmailService = Provide[Container.email_service]):
    
    instance = ObterTramitacoesUseCase(database_service, tjrj_service)
    
    tramitacoesObservadas = Documento.objects.distinct("id_tjrj")
    
    for tramitacao in tramitacoesObservadas:
        tramitacoes = instance.obterTramitacoesTJRJ(tramitacao.id_tjrj)
        
        action = instance.atualizaHashTramitacoesBanco(numero_documento=tramitacao.id_doc,id_tjrj=tramitacao.id_tjrj, tramitacoes=tramitacoes)
        
        if action == ObterTramitacoesUseCase.Action.UPDATED:
            
            # Se o documento mudou, invalidar o cache para próxima requisição de usuário
            # acessar o serviço do SOAP
            cache_service.delete(tramitacao.id_doc)
            
            # Retorna todos os usuarios que fizeram alguma consulta a esse documento
            # Esses usuários são os interessados nas mudanças desse documento
            usuariosObservers = UsuarioObservers.objects.filter(id_tjrj=tramitacao.id_tjrj)
            
            # # Disparar um email para cada um dos usuarios interessados avisando da mudança
            # # O primeiro que acessar vai gerar um novo cache no servidor
            # # e os próximos já vão acessar a versão nova em cache            
            for interessado in usuariosObservers:
                email_service.enviarEmail(interessado.usuario, {
                    "mensagem": "O conteúdo que você consultou mudou!"
                })