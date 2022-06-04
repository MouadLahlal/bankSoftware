import sqlite3
import os


def menu():
    os.system("cls")
    print("### MENU ###")
    print("1 - Cerca conto corrente")
    print("2 - Richieste di prestito")
    print("3 - Regola tassi d'interesse")
    print("0 - Esci")
    return input("=> ")


path = f"{os.getcwd()}\database.db"
database = sqlite3.connect(path, check_same_thread=False)

while True:
    op = int(menu())
    match op:
        case 1:
            os.system("cls")
            print("### CERCA CONTO CORRENTE ###")
            print("1 - Cerca tramite nome")
            print("2 - Cerca tramite iban")
            print("0 - Torna al menu precedente")
            scelta = int(input("=>"))
            match scelta:
                case 1:
                    nome = input("Inserisci nome : ")
                    dati = database.execute("SELECT username,iban,saldo FROM account WHERE username=?", (nome,))
                    y = ""
                    for x in dati:
                        y += str(x)
                    print(y)
                    continua = input("\nPremere 'c' per continuare...")
                case 2:
                    iban = input("Inserisci iban : ")
                    dati = database.execute("SELECT username,iban,saldo FROM account WHERE iban=?", (iban,))
                    y = ""
                    for x in dati:
                        y += str(x)
                    print(y)
                    continua = input("\nPremere 'c' per continuare...")

        case 0:
            os.system("cls")
            print("### ARRIVEDERCI ###")
            exit(0)
