from django.contrib.auth.models import Permission
from django.contrib import admin
from .models import Documento

admin.site.register(Permission)
admin.site.register(Documento)