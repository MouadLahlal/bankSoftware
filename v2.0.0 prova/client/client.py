import pickle
import socket
from infoManager import InfoManager

im = InfoManager()


def receiveObject():

    # comunica con sendObject

    HEADERSIZE = 10

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    connesso = False
    while connesso==False:
        try:
            s.connect((socket.gethostname(), 7777))
            connesso = True
        except:
            pass

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
    
    s.close()
    return oggetto

def riceviMsg():

    # comunica ocn sendMsg

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    connesso = False

    while connesso == False:

        try:
            s.connect((socket.gethostname(), 8888))
            connesso = True
        except ConnectionRefusedError:
            pass
    
    msg = s.recv(1024)
    msg = msg.decode()

    s.close()
    return msg

def sendMsg(msg):

    # comunica con sendmoney

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((socket.gethostname(), 9999))
    s.listen(5)

    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")
    
    msg = msg.encode()
    clientsocket.send(msg)
    s.close()

def sendLogin(username, psw):

    # comunica con login

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((socket.gethostname(), 1234))
    s.listen(5)

    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")

    msg = im.encryptInfo(username)
    clientsocket.send(msg)
    msg = im.encryptInfo(psw)
    clientsocket.send(msg)

    oggetto = receiveObject()

    s.close()
    return oggetto