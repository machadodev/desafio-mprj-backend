import json
from enum import Enum
from django.contrib.auth.models import User
from dependency_injector.wiring import inject, Provide
from desafio.models import Documento, UsuarioObservers
from desafio.containers import Container
from desafio.helper import hashString


class ObterTramitacoesUseCase:
    class Action(Enum):
        NO_ACTION = 1
        UPDATED = 2
        CREATED = 3
    # Esta função atualiza ou cria
    # uma tripla: (id_documento, id_tjrj, hash_tramitacao)
    # Dessa forma sempre que é feito uma requisição de
    # tramitações, é feito um hash
    # Isso permite saber se desde o último acesso o arquivo mudou.

    def atualizaHashTramitacoesBanco(self, numero_documento, id_tjrj,
                                     tramitacoes):
        hash = hashString(json.dumps(tramitacoes, ensure_ascii=False))
        obj, criado = Documento.objects.get_or_create(
            id_doc=numero_documento,
            id_tjrj=id_tjrj,
            defaults={"hash_tramitacao": hash}
        )

        action = self.Action.NO_ACTION

        if criado:
            action = self.Action.CREATED
        elif obj.hash_tramitacao != hash:
            action = self.Action.UPDATED

        return action

    # Traz as tramitações em JSON
    @inject
    def obterTramitacoesTJRJ(self,
                             id_tjrj,
                             tjrj_service=Provide[Container.tjrj_service]):
        return tjrj_service.obterTramitacoes(id_tjrj)

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
    @inject
    def obterTramitacoes(self,
                         request,
                         numero_documento,
                         database_service=Provide[Container.database_service]):

        dados_documento = database_service.obterDocumento(numero_documento)

        usuario_id = request.user.id
        id_tjrj = dados_documento['id_tjrj']

        tramitacoes = self.obterTramitacoesTJRJ(id_tjrj)

        self.atualizaHashTramitacoesBanco(
            numero_documento, id_tjrj, tramitacoes)

        self.solicitaNoticacoesDeMudancas(usuario_id, id_tjrj)

        return tramitacoes

# DECORATOR
# Essa classe serve para estender as funcionalidades da classe original
# Nela faremos a configuração do CACHE para verificar se devemos devolver
# uma informaçaõ que está salva em memória ou devemos prosseguir a consulta
# nos serviços externos


class ObterTramitacoesUseCaseCacheDecorator(
    ObterTramitacoesUseCase
):
    @inject
    def obterTramitacoes(self,
                         request,
                         numero_documento,
                         cache_service=Provide[Container.cache_service]):

        tramitacoes = cache_service.get(numero_documento)

        if tramitacoes is None:
            tramitacoes = super().obterTramitacoes(request, numero_documento)
            cache_service.set(numero_documento, tramitacoes)

        return tramitacoes

# DECORATOR
# Essa classe serve para estender as funcionalidades da classe original
# Nela faremos logs do request e das tramitações


class ObterTramitacoesUseCaseLoggerDecorator(
        ObterTramitacoesUseCaseCacheDecorator
):
    @inject
    def obterTramitacoes(self,
                         request,
                         numero_documento,
                         log_service=Provide[Container.log_service]):

        tramitacoes = super().obterTramitacoes(request, numero_documento)

        # iv - make log
        log_service.record(request, tramitacoes)

        return tramitacoes


def handler(request, numero_documento):
    instance = ObterTramitacoesUseCaseLoggerDecorator()

    return instance.obterTramitacoes(request, numero_documento)


@inject
def handlerScheduled(
        cache_service=Provide[Container.cache_service],
        email_service=Provide[Container.email_service]):

    instance = ObterTramitacoesUseCase()

    tramitacoesObservadas = Documento.objects.distinct("id_tjrj")

    for tramitacao in tramitacoesObservadas:
        tramitacoes = instance.obterTramitacoesTJRJ(tramitacao.id_tjrj)

        action = instance.atualizaHashTramitacoesBanco(
            numero_documento=tramitacao.id_doc,
            id_tjrj=tramitacao.id_tjrj,
            tramitacoes=tramitacoes)

        if action == ObterTramitacoesUseCase.Action.UPDATED:

            # Se o documento mudou, invalidar o cache para
            # próxima requisição de usuário
            # acessar o serviço do SOAP
            cache_service.delete(tramitacao.id_doc)

            # Retorna todos os usuarios que fizeram alguma
            # consulta a esse documento
            # # Esses usuários são os interessados nas mudanças desse documento
            usuariosObservers = UsuarioObservers.objects.filter(
                id_tjrj=tramitacao.id_tjrj)

            # # Disparar um email para cada um dos usuarios
            # interessados avisando da mudança
            # # O primeiro que acessar vai gerar um novo cache no servidor
            # # e os próximos já vão acessar a versão nova em cache
            for interessado in usuariosObservers:
                email_service.enviarEmail(interessado.usuario, {
                    "mensagem": "O conteúdo que você consultou mudou!"
                })
