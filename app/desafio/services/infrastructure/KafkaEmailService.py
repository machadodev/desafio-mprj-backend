import json
import os
from kafka import KafkaProducer
from kafka.errors import KafkaError
from desafio.services.protocols import EmailService


class KafkaEmailService(EmailService):
    def __init__(self) -> None:
        connection = os.environ.get(
            "KAFKA_HOST") + ":" + os.environ.get("KAFKA_PORT")
        self.producer = KafkaProducer(
            bootstrap_servers=connection,
            value_serializer=lambda v: json.dumps(v, ensure_ascii=False).
            encode('utf-8'))
        super().__init__()

    def enviarEmail(self, usuario, conteudo):
        email_info = {
            "user": usuario,
            "data": conteudo
        }

        try:
            # self.producer.send('email', email_info)
            print("ENVIAR MENSAGEM KAFKA", email_info)
        except KafkaError as ex:
            print("KafkaEmailService::enviarEmail()", ex)
