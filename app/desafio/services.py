class DatabaseService:
    def findDocumento(self, dados):
        dados_documento = { "id": dados["id"], "id_tjrj": 2 }
        return dados_documento

class TJRJService:
    def findTramitacao(self, dados):
        tramitacao = '''
        <TRAMITACOES>
        <TRAMITACAO idtram="1">
        <data>01/01/1999</data>
        <doc>Texto falando sobre qual foi a tramitação, transcrições de ata, etc etc</doc>
        </TRAMITACAO>
        <TRAMITACAO idtram="2">
        <data>02/01/1999</data>
        <doc>Texto falando sobre qual foi a tramitação, transcrições de ata, etc etc</doc>
        </TRAMITACAO>
        </TRAMITACOES>
        '''    
        return tramitacao
    
class LogService:    
    def record(self, request, dados):
        print("Logger Service:")
        print("Request:", request)
        print("Dados:", dados)


class CacheService:
        pass
