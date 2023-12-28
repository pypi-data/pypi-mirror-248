import os
import configparser

class NFMethods:

    def map_nf_path(self):

        user_path = os.path.expanduser('~')

        return f'{user_path}/NFe.ini'
    
    def generate_ini(self, data: dict):

        ini = configparser.ConfigParser()

        for section, values in data.items():
            ini.add_section(section)
            for key, value in values.items():
                ini.set(section, key, str(value))
        
        return ini

    def write_ini(self, file_path, ini: configparser.ConfigParser):

        with open(file_path, 'w') as file:
                
            ini.write(file)
