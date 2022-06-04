import User
import pickle
import re
import socket
from datetime import datetime
from threading import Thread
from infoManager import InfoManager
from publicUser import PublicUser

im = InfoManager()
User.main()


def sendObject(oggetto):

    # comunica con receiveObject

    HEADERSIZE = 10

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((socket.gethostname(), 7777))
    s.listen(5)

    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")

    msg = pickle.dumps(oggetto)
    msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8')+msg
    clientsocket.send(msg)
    print("Oggetto inviato")

    s.close()

def sendMsg(msg):

    # comunica con riceviMsg

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((socket.gethostname(), 8888))
    s.listen(5)

    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")
    
    msg = msg.encode()
    clientsocket.send(msg)

    s.close()


def sendmoney():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    connesso = False

    while connesso == False:

        try:
            s.connect((socket.gethostname(), 9999))
            connesso = True
        except ConnectionRefusedError:
            pass

    msg = s.recv(1024)
    iban = im.decryptInfo(msg)

    msg = s.recv(1024)
    somma = im.decryptInfo(msg)

    User.user.getSaldo()

    if int(User.user.saldo)>=somma:

        # aggiorno saldo utente mittente
        User.user.saldo = int(User.user.saldo) - somma - 0.5
        User.user.database.execute("UPDATE account SET saldo=? WHERE username=?", (User.user.saldo, User.user.username,))
        User.user.database.commit()

        # aggiorno saldo utente ricevente
        dati = User.user.database.execute("SELECT saldo FROM account WHERE iban=?", (iban,))
        y=""
        for x in dati:
            y = y + str(x)
        x = y.replace(",", "")
        re.split('( |)',x)
        x = x.replace("(","")
        x = x.replace(")","")
        saldoAttuale = float(x) + float(somma)
        User.user.database.execute("UPDATE account SET saldo=? WHERE iban=?", (saldoAttuale, iban,))
        User.user.database.commit()

        # aggiorno saldo conto della banca
        dati = User.user.database.execute("SELECT saldo FROM account WHERE iban=?", ("666",))
        y=""
        for x in dati:
            y = y + str(x)
        x = y.replace(",", "")
        re.split('( |)',x)
        x = x.replace("(","")
        x = x.replace(")","")
        saldoAttuale = float(x) + 0.5
        User.user.database.execute("UPDATE account SET saldo=? WHERE iban=?", (saldoAttuale, "666",))
        User.user.database.commit()

        # prendo l'username dell'utente ricevente
        dati = User.user.database.execute("SELECT username FROM account WHERE iban=?", (iban,))
        y=""
        for x in dati:
            y = y + str(x)
        x = y.replace(",", "")
        re.split('( |)',x)
        x = x.replace("(","")
        x = x.replace(")","")
        usernameRicevente = x.replace("'","")

        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        # salvo le operazioni sui rispettivi file degli utenti e della banca
        file = open(User.user.username+".txt", "a")
        file.write(f"{date},{iban},-{somma}\n")
        file.close()
        file = open(usernameRicevente+".txt", "a")
        file.write(f"{date},{User.user.iban},+{somma}\n")
        file.close()

        sendMsg("0")
    
    else:
        sendMsg("-1")
    
    s.close()


def login():

    # comunica con sendLogin

    global c
    c='a'

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while c!='x':

        connesso = False

        while connesso==False:
            try:
                print("Tentativo di connessione...")
                s.connect((socket.gethostname(), 1234))
                connesso = True
            except ConnectionRefusedError:
                pass

        msg = s.recv(1024)
        username = im.decryptInfo(msg)

        msg = s.recv(1024)
        psw = im.decryptInfo(msg)

        privateUser = User.user
        privateUser.getUsername(username)
        privateUser.getPassword(psw)

        if privateUser.username is not None:
            if privateUser.psw is not None:
                privateUser.getIban()
                privateUser.getSaldo()
                publicUser = PublicUser(privateUser.username, privateUser.psw, privateUser.iban, privateUser.saldo)
                sendObject(publicUser)
    
    s.close()

if __name__ == "__main__":
    global c
    t1 = Thread(target=login, daemon=True)
    t1.start()
    c = input("Fermare ? ")