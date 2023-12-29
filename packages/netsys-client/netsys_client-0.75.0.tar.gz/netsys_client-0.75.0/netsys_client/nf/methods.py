import os
import configparser
import mysql.connector

class NFMethods:

    def map_nf_path(self):

        user_path = os.path.expanduser('~')

        return f'{user_path}'
    
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

    def write_txt(self, file_path, txt):

        with open(file_path, 'w') as file:
            file.write(txt)

    def read_txt(self, file_path):

        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def send_to_db(self, txt, token):

        con = mysql.connector.connect(user = 'netsys', host = 'localhost', database = 'netsys_db', password = 'Gtq62fp@')
        cursor = con.cursor()
        cursor.execute(f"insert into ctblognf (error, token) values ('teste', {token})")
        con.commit()