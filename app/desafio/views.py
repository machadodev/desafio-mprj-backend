from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
#from rest_framework_xml.renderers import XMLRenderer
from desafio.serializers import DocumentoSerializer
from desafio.exceptions import *

class TramitacaoDocumentoAPIView(APIView):
    # renderer_classes = [XMLRenderer]
    
    def get_object(self, id_documento):
        try:
            return (id_documento, "test")
        except Exception:
            raise NotFoundException(message="Document not found")
        
    def validate(self, id_documento):
        serializer = DocumentoSerializer(data={"id": id_documento})
        
        if serializer.is_valid():
            return serializer.data            
        else:
            raise UnprocessableEntityException(errors=serializer.errors)        
        
    def handler(self, id_documento):
        valid_data = self.validate(id_documento)
        return Response(valid_data)
                 

    def get(self, request, id_documento, format=None):        
        response = None        
        try:
            response = self.handler(id_documento)
        except UnprocessableEntityException as ex:
            response = Response(ex.errors, status=ex.code)
        except NotFoundException as ex:
            response = Response(ex.message, status=ex.code)
        except Exception as ex:
            ex = InternalServerException()
            response = Response(ex.message, status=ex.code)
        finally:
            return response
