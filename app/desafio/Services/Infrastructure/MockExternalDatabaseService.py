from desafio.Services.Protocols import DatabaseService


# Aqui entram os detalhes do banco externo:
# HOST, PORT, USER e PASSWORD
class MockExternalDatabaseService(DatabaseService):    
    def findDocumento(self, dados):
        dados_documento = { "id": dados["id"], "id_tjrj": 2 }
        return dados_documento
