from desafio.Services.Protocols import DatabaseService
from desafio.exceptions import NotFoundException

# Aqui entram os detalhes do banco externo:
# HOST, PORT, USER e PASSWORD
class MockExternalDatabaseService(DatabaseService):    
    def obterDocumento(self, numero_documento):
        
        id_tjrj = 1
        
        if numero_documento == 1:
            id_tjrj = 2
        elif numero_documento == 2:
            id_tjrj = 3
        elif numero_documento == 3:
            id_tjrj = 4
        elif numero_documento == 4:
            id_tjrj = 5
        else:
            raise NotFoundException("Documento nao encontrado do banco de dados externo.")

        dados_documento = { "id_tjrj": id_tjrj }
        
        return dados_documento
