from rest_framework import serializers


# Caso julgue necessário criar algum serializer
class DocumentoSerializer(serializers.Serializer):
    id = serializers.IntegerField(label='ID', read_only=True)