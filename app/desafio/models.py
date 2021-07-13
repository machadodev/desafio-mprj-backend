from django.db import models


# Caso precise criar algum modelo para sua aplicação

class Documento(models.Model):
    id_doc = models.IntegerField()
    id_tjrj = models.IntegerField()
    hash_tramitacao = models.CharField(max_length=32)
