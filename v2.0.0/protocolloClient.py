from socket import *


class Client:

    def __init__(self, host, port):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.host = host
        self.port = port
        self.connect()

    def connect(self):
        connected = False
        while not connected:
            try:
                self.socket.connect((self.host, self.port))
                connected = True
                print("Connesso con il server")
            except:
                pass

    def receive(self):

        sep = b'\n'  # separator : separatore per identificare la fine di una sequenza di bit
        data_id = ''  # data id : identifica il tipo di dati che verrano ricevuti
        bytes_len = ''  # bytes lenght : lunghezza della sequenza di byte che verrà ricevuta
        bytes_sequence = ''  # bytes sequence : sequenza di byte da ricevere
        byte = b''

        # finchè il byte ricevuto nel ciclo precedente è diverso da sep ("\n") continua ad aggiungere il byte alla variabile a patto che sia diverso da "\n"

        while byte != sep:
            byte = self.socket.recv(1)
            if byte != sep:
                data_id += byte.decode()
        byte = ''
        while byte != sep:
            byte = self.socket.recv(1)
            if byte != sep:
                bytes_len += byte.decode()
        byte = ''
        while byte != sep:
            byte = self.socket.recv(1)
            if byte != sep:
                bytes_sequence += byte.decode()
        lista = [data_id, bytes_len, bytes_sequence]
        return lista

    def send(self, msg, data_id):

        bytes_len = len(msg)
        stringa = data_id + "\n" + str(bytes_len) + "\n" + msg + "\n"
        stringa = stringa.encode()
        self.socket.send(stringa)
