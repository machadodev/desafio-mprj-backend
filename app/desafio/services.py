# Contratos

class DatabaseService:
    def findDocumento(self, dados):
        pass

class TJRJService:
    def findTramitacao(self, dados):
        pass
    
class LogService:    
    def record(self, request, dados):
        pass

class CacheService:
        pass

# =========================================

# Implementações

# Aqui entram os detalhes do banco externo: 
# HOST, PORT, USER e PASSWORD
class MockExternalDatabaseService(DatabaseService):
    def findDocumento(self, dados):
        dados_documento = { "id": dados["id"], "id_tjrj": 2 }
        return dados_documento

# Aqui entram os detalhes do banco externo: 
# HOST, PORT, USER e PASSWORD
class MockTJRJSOAPService(TJRJService):
    def __init__(self, ACCESS_TOKEN_TJRJ):
        self.ACCESS_TOKEN = ACCESS_TOKEN_TJRJ
        
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

# 
class KafkaLoggerService(LogService):
    def record(self, request, dados):
        print("Logger Service Kafka:")
        print("Producing data:", dados)

class RedisService(CacheService):
    pass
