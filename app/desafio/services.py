# Contratos
from django.core.cache import cache
import xmltodict, json

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
    def get(self, key):
        pass
    def set(self, key, value, ttl):
        pass
    def delete(self, key):
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
        xml_data = '''
        <TRAMITACOES>
        <TRAMITACAO idtram="1">
        <data>01/01/1999</data>
        <doc>Texto falando sobre qual foi a tramitação, transcrições de ata, etc etc</doc>
        </TRAMITACAO>
        <TRAMITACAO idtram="2">
        <data>02/01/2000</data>
        <doc>Texto falando sobre qual foi a tramitação, transcrições de ata, etc etc</doc>
        </TRAMITACAO>
        </TRAMITACOES>
        '''
        
        #converting xml to dictionary
        tramitacao = xmltodict.parse(xml_data)
        # converting to json and returning
       # tramitacao = json.dumps(tramitacao, ensure_ascii=False)
        
        return tramitacao

# 
class KafkaLoggerService(LogService):
    class LoggerFormat:
        def __init__(self, request, documento_tramitacao):
            
            json_data = json.dumps(documento_tramitacao, ensure_ascii=False)  
            
            self.log = {
                "user_id": request.user.id,
                "scheme": request.scheme,
                "path": request.path,
                "method": request.method,
                "user_agent": request.headers['User-Agent'],
                "data": json.loads(json_data)
            }
            
            self.log = json.dumps(self.log, ensure_ascii=False)  
    
    def record(self, request, dados):
        loggerFormat = self.LoggerFormat(request, dados)
        print("LOGGER KAFKA:")
        print("Log info:", loggerFormat.log)

class RedisCacheService:    
    def get(self, key):
        #return cache.get(key, None)
        return None
    
    def set(self, key, value, ttl):
        pass
    def delete(self, key):
        pass