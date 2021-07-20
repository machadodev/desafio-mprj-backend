from desafio.usecase import ObterTramitacoesUseCase
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from desafio.permissions import PermissionDocumento
from desafio.serializers import DocumentoSerializer
from desafio.exceptions import (
    UnprocessableEntityException,
    NotFoundException,
    InternalServerException)


class TramitacaoDocumentoAPIView(APIView):
    permission_classes = (IsAuthenticated, PermissionDocumento)

    def validate(self, numero_documento):
        serializer = DocumentoSerializer(data={"numero": numero_documento})

        if serializer.is_valid():
            return serializer.data['numero']
        else:
            raise UnprocessableEntityException(errors=serializer.errors)

    def handler(self, request, numero_documento):
        numero_documento_validado = self.validate(numero_documento)
        return ObterTramitacoesUseCase.handler(request,
                                               numero_documento_validado)

    def get(self, request, numero_documento, format=None):
        response = None
        try:
            documento_tramitacao = self.handler(request, numero_documento)
            response = Response(documento_tramitacao)
        except UnprocessableEntityException as ex:
            response = Response(ex.errors, status=ex.code)
        except NotFoundException as ex:
            response = Response(ex.message, status=ex.code)
        except Exception as ex:
            print("EXCEPTION:", ex)
            ex = InternalServerException()
            response = Response(ex.message, status=ex.code)
        finally:
            return response
