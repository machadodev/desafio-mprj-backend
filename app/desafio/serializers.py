from rest_framework import serializers


# Caso julgue necessário criar algum serializer
class DocumentoSerializer(serializers.Serializer):
    numero = serializers.IntegerField(min_value=1)