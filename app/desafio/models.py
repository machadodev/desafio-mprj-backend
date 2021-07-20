from django.db import models
from django.contrib.auth.models import User


# Caso precise criar algum modelo para sua aplicação

class Documento(models.Model):
    id_doc = models.IntegerField()
    id_tjrj = models.IntegerField()
    hash_tramitacao = models.CharField(max_length=32)


class UsuarioObservers(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    id_tjrj = models.IntegerField()
