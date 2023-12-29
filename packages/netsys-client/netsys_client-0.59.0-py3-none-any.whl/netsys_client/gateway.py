from . import ConfController, PrintController, Response, NFController
import json

class Gateway:

    _erros = []

    def __init__(self):

        self._response = Response()

    def change_config(self):
        
        self._message = {'token': self._token}
        self._response.send_message(json.dumps(self._message))
        self._message = self._response.get_message()
        self._conf = ConfController(json.loads(self._message))
        self._conf.execute()

    def search_printers(self):

        self._print = PrintController()
        self._message = self._print.get_printer_list(self._token)
        self._response.send_message(json.dumps(self._message))

    def print_cupom_fiscal(self):

        self._message = {'token': self._token}
        self._response.send_message(json.dumps(self._message))
        self._message = self._response.get_message()
        self._print = PrintController()
        printer = ConfController().get_parameter('printer')
        self._print.setPrinter(printer)
        self._print.print_data(json.loads(self._message))

    def emitir_nota_fiscal(self):

        self._message = {'token': self._token}
        self._response.send_message(json.dumps(self._message))
        self._message = self._response.get_message()
        data: dict = json.loads(self._message)
        ini = data.get('ini')
        cupom = data.get('cupom')
        self._nf = NFController(ini)
        self._nf.execute()
        self._print = PrintController()
        self._print.print_data(cupom)
    
    def set_erro(self, erro):

        self._erros.append(erro)

    def set_token(self, token):

        self._token = token