from rest_framework import serializers


# Caso julgue necessário criar algum serializer
class DocumentoSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=1)