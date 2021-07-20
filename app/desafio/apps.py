from django.apps import AppConfig
from . import container


class DesafioConfig(AppConfig):
    name = 'desafio'

    def ready(self):
        from .usecase import ObterTramitacoesUseCase
        container.wire(modules=[ObterTramitacoesUseCase])
        from .tasks import start
        start()
