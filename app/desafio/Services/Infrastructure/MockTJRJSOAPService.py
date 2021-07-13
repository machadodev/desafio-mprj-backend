import xmltodict
from desafio.Services.Protocols import TJRJService


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
        
        return tramitacao