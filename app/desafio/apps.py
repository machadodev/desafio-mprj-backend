from django.apps import AppConfig
#from app import project_config
from . import container
import sys
from . import usecases


class DesafioConfig(AppConfig):
    name = 'desafio'

    def ready(self):
        container.wire(modules=[usecases])
