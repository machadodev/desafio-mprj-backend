from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_xml.parsers import XMLParser
from rest_framework_xml.renderers import XMLRenderer
from rest_framework.permissions import IsAuthenticated
from desafio.permissions import PermissionDocumento
# Cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from project_config.settings import CACHE_TTL_IN_SECONDS
from desafio.serializers import DocumentoSerializer
from desafio.exceptions import *
from desafio import usecases

class TramitacaoDocumentoAPIView(APIView):
    parser_classes = [XMLParser]
    renderer_classes = [XMLRenderer]
    permission_classes = (IsAuthenticated, PermissionDocumento)

    def validate(self, id_documento):
        serializer = DocumentoSerializer(data={"id": id_documento})
        
        if serializer.is_valid():
            return serializer.data            
        else:
            raise UnprocessableEntityException(errors=serializer.errors)        
        
    def handler(self, request, id_documento):
        validated_data = self.validate(id_documento)            
        return usecases.handler(request, validated_data)
    
    @method_decorator(cache_page(CACHE_TTL_IN_SECONDS))
    def get(self, request, id_documento, format=None):        
        response = None        
        try:            
            response = HttpResponse(self.handler(request, id_documento), content_type="text/xml")
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
