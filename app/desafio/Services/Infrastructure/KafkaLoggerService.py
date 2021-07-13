import json
from desafio.Services.Protocols import LogService


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