import xmltodict
from desafio.services.protocols import TJRJService
from desafio.exceptions import NotFoundException


class MockTJRJSOAPService(TJRJService):
    def __init__(self, ACCESS_TOKEN_TJRJ):
        self.ACCESS_TOKEN = ACCESS_TOKEN_TJRJ

    def obterTramitacoes(self, id_tjrj):
        xml_data = ""

        if id_tjrj == 2:
            xml_data = '''
        <TRAMITACOES>
        <TRAMITACAO idtram="1">
        <data>01/01/2000</data>
        <doc>Texto falando sobre qual foi a tramitação</doc>
        </TRAMITACAO>
        <TRAMITACAO idtram="2">
        <data>02/01/2000</data>
        <doc>Texto falando sobre qual foi a tramitação</doc>
        </TRAMITACAO>
        </TRAMITACOES>
        '''
        elif id_tjrj == 3:
            xml_data = '''
        <TRAMITACOES>
        <TRAMITACAO idtram="1">
        <data>01/01/2020</data>
        <doc>Texto falando sobre qual foi a tramitação</doc>
        </TRAMITACAO>
        <TRAMITACAO idtram="2">
        <data>02/01/2000</data>
        <doc>Texto falando sobre qual foi a tramitação</doc>
        </TRAMITACAO>
        </TRAMITACOES>
        '''
        elif id_tjrj == 4:
            xml_data = '''
        <TRAMITACOES>
        <TRAMITACAO idtram="1">
        <data>01/01/1995</data>
        <doc>Texto falando sobre qual foi a tramitação</doc>
        </TRAMITACAO>
        <TRAMITACAO idtram="2">
        <data>02/01/2000</data>
        <doc>Texto falando sobre qual foi a tramitação</doc>
        </TRAMITACAO>
        </TRAMITACOES>
        '''
        elif id_tjrj == 5:
            xml_data = '''
        <TRAMITACOES>
        <TRAMITACAO idtram="1">
        <data>01/01/1980</data>
        <doc>Texto falando sobre qual foi a tramitação</doc>
        </TRAMITACAO>
        <TRAMITACAO idtram="2">
        <data>02/01/2000</data>
        <doc>Texto falando sobre qual foi a tramitação</doc>
        </TRAMITACAO>
        </TRAMITACOES>
        '''
        elif id_tjrj == 6:
            xml_data = '''
        <TRAMITACOES>
        <TRAMITACAO idtram="1">
        <data>01/01/1975</data>
        <doc>Texto falando sobre qual foi a tramitação</doc>
        </TRAMITACAO>
        <TRAMITACAO idtram="2">
        <data>02/01/2000</data>
        <doc>Texto falando sobre qual foi a tramitação</doc>
        </TRAMITACAO>
        </TRAMITACOES>
        '''

        if xml_data == "":
            raise NotFoundException("Tramitacoes nao encontradas no TJRJ")

        # converting xml to dictionary
        tramitacoes = xmltodict.parse(xml_data)

        return tramitacoes
