import json
import os
from kafka import KafkaProducer
from kafka.errors import KafkaError
from desafio.Services.Protocols import LogService


class KafkaLoggerService(LogService):
    def __init__(self) -> None:
        connection = os.environ.get("KAFKA_HOST") + ":" + os.environ.get("KAFKA_PORT")
        self.producer = KafkaProducer(bootstrap_servers=connection,
                                      value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode('utf-8'))
        super().__init__()
        
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
    
    def record(self, request, dados):
        loggerFormat = self.LoggerFormat(request, dados)
        try:
            self.producer.send('documento', loggerFormat.log)
        except KafkaError as ex:
            print("KafkaLoggerService::record()", ex)
        