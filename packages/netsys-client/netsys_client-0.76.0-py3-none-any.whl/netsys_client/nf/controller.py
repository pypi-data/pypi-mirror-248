from . import NFMethods
from mysql.connector import Error

class NFController(NFMethods):
    
    def __init__(self, data, token):

        self._data = data
        self._file_path = self.map_nf_path()
        self._token = token

    def execute(self):

        self._ini = self.generate_ini(self._data)
        self.write_ini(f'{self._file_path}/NFe.ini', self._ini)
        txt = f'NFe.CriarEnviarNFe("{self._file_path}/NFe.ini",1,1, , ,1)'
        self.write_txt(f'{self._file_path}\Entrada\ENT.txt', txt)
        txt = self.read_txt(f'{self._file_path}\Saida\ENT-resp.txt')
        try:
            self.send_to_db(txt, self._token)
        except Error as e:
            self.write_txt(f'{self._file_path}\log.txt', e)
        self.write_txt(f'{self._file_path}\Saida\ENT-resp.txt', '')

