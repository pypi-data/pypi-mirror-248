from . import NFMethods

class NFController(NFMethods):
    
    def __init__(self, data):

        self._data = data
        self._file_path = self.map_nf_path()

    def execute(self):

        self._ini = self.generate_ini(self._data)
        self.write_ini(f'{self._file_path}/NFe.ini', self._ini)
        self.write_ini(f'{self._file_path}/NFe.ini', self._ini)
        txt = f'NFe.CriarEnviarNFe("{self._file_path}/NFe.ini",1,1, , ,1)'
        self.write_txt(f'{self._file_path}/ENT.txt', txt)

