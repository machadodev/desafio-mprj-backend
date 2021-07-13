from django.apps import AppConfig
from . import container
from .UseCase import ObterTramitacaoDocumentoUseCase


class DesafioConfig(AppConfig):
    name = 'desafio'

    def ready(self):
        container.wire(modules=[ObterTramitacaoDocumentoUseCase])
        from .tasks import start
        start()
