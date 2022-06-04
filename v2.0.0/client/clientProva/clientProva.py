import pickle
import socket
from infoManager import InfoManager

im = InfoManager()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.1.87', 17000))

def send(msg):

    msg = im.encryptInfo(msg)
    s.send(msg)

def receive(oggetto_da_ricevere):
    global s

    if oggetto_da_ricevere == "oggetto":
        HEADERSIZE = 10

        full_msg = b''
        new_msg = True
        while True:
            msg = s.recv(16)
            if new_msg:
                msglen = int(msg[:HEADERSIZE])
                new_msg = False

            full_msg += msg

            if len(full_msg)-HEADERSIZE == msglen:
                oggetto = pickle.loads(full_msg[HEADERSIZE:])
                new_msg = True
                full_msg = b""
                break
        return oggetto
    
    elif oggetto_da_ricevere == "stringa":
        
        msg = s.recv(1024)
        msg = im.decryptInfo(msg)
        return msg