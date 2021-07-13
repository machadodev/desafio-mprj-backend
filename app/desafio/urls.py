from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from desafio import views

urlpatterns = [
    path("<numero_documento>", views.TramitacaoDocumentoAPIView.as_view(),name="tramitacao_documento"),
]

urlpatterns = format_suffix_patterns(urlpatterns)