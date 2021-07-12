from rest_framework.views import APIView
from rest_framework.response import Response
from desafio.serializers import DocumentoSerializer
from rest_framework_xml.renderers import XMLRenderer

class TramitacaoDocumentoAPIView(APIView):
    renderer_classes = [XMLRenderer]
    
    def get(self, request, id_documento, format=None):
        documentos = None
        serializer = DocumentoSerializer(documentos, many=True)
        return Response(serializer.data)
