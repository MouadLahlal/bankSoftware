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

HOST = None
PORT = None
spegniServer = False

s = None


def receive(clientsocket):
    msg = clientsocket.recv(1024)
    try:
        msg = im.decryptInfo(msg)
    except:
        msg = "error"
    return msg


def send(clientsocket, oggetto, msg):
    global s
    if oggetto is not None:
        HEADERSIZE = 10
        msg = pickle.dumps(oggetto)
        msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8') + msg
        clientsocket.send(msg)

    elif msg is not None:
        msg = im.encryptInfo(msg)
        clientsocket.send(msg)


def new_client(clientsocket, address, privateUser):
    while True:
        msg = receive(clientsocket)
        if msg == "aggiorna":
            privateUser.getSaldo()
            publicUser = PublicUser(privateUser.username, privateUser.psw, privateUser.iban, privateUser.saldo)
            send(clientsocket, publicUser, None)
        elif msg == "sendmoney":
            sendmoney(clientsocket, privateUser)
        elif msg == "error":
            print(f"Connessione interrotta da {address}")
            break


def sendmoney(clientsocket, user):
    iban = receive(clientsocket)

    somma = float(receive(clientsocket))

    user.getSaldo()

    if float(user.saldo) >= somma:

        # aggiorno saldo utente mittente
        user.saldo = float(user.saldo) - somma - 0.5
        user.database.execute("UPDATE account SET saldo=? WHERE username=?",
                              (user.saldo, user.username,))
        user.database.commit()

        # aggiorno saldo utente ricevente
        dati = user.database.execute("SELECT saldo FROM account WHERE iban=?", (iban,))
        y = ""
        for x in dati:
            y = y + str(x)
        x = y.replace(",", "")
        re.split('( |)', x)
        x = x.replace("(", "")
        x = x.replace(")", "")
        saldoAttuale = float(x) + float(somma)
        user.database.execute("UPDATE account SET saldo=? WHERE iban=?", (saldoAttuale, iban,))
        user.database.commit()

        # aggiorno saldo conto della banca
        dati = user.database.execute("SELECT saldo FROM account WHERE iban=?", ("666",))
        y = ""
        for x in dati:
            y = y + str(x)
        x = y.replace(",", "")
        re.split('( |)', x)
        x = x.replace("(", "")
        x = x.replace(")", "")
        saldoAttuale = float(x) + 0.5
        user.database.execute("UPDATE account SET saldo=? WHERE iban=?", (saldoAttuale, "666",))
        user.database.commit()

        # prendo l'username dell'utente ricevente
        dati = user.database.execute("SELECT username FROM account WHERE iban=?", (iban,))
        y = ""
        for x in dati:
            y = y + str(x)
        x = y.replace(",", "")
        re.split('( |)', x)
        x = x.replace("(", "")
        x = x.replace(")", "")
        usernameRicevente = x.replace("'", "")

        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        # salvo le operazioni sui rispettivi file degli utenti e della banca
        file = open(user.username + ".txt", "a")
        file.write(f"{date},{iban},-{somma}\n")
        file.close()
        file = open(usernameRicevente + ".txt", "a")
        file.write(f"{date},{user.iban},+{somma}\n")
        file.close()

        send(clientsocket, None, "0")

    else:
        send(clientsocket, None, "-1")


def login(clientsocket, address):
    # funzione che gestisce il login degli utenti

    global s

    privateUser = User.PrivateUser()
    logged = False

    while not logged:

        username = receive(clientsocket)
        psw = receive(clientsocket)

        privateUser.getUsername(username)
        privateUser.getPassword(psw)

        if privateUser.username is not None:
            if privateUser.psw is not None:
                privateUser.getIban()
                privateUser.getSaldo()
                logged = True
        publicUser = PublicUser(privateUser.username, privateUser.psw, privateUser.iban, privateUser.saldo)
        send(clientsocket, publicUser, None)
    new_client(clientsocket, address, privateUser)


def main():
    while True:
        clientsocket, address = s.accept()
        if spegniServer == False:
            print(f"Connesso con {address}")
            t1 = Thread(target=login, args=(clientsocket, address,), daemon=True)
            t1.start()


if __name__ == "__main__":
    ip = input("Inserisci indirizzo ip della macchina : ")
    porta = int(input("Inserisci porta sulla quale eseguire il servizio : "))
    conferma = input(f"Dati inseriti : \n Ip = {ip} \n Porta = {porta} \nCorretto? s/n ")
    if conferma == "s":
        HOST = ip
        PORT = porta
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(5)

    main()
