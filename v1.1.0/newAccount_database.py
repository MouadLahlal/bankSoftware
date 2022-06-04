import sqlite3
import os

dr = f"{os.getcwd()}\database.db"

database = sqlite3.connect(dr)

username = input("Inserisci username : ")
psw = input("Inserisci password : ")
iban = input("Inserisci iban : ")
saldo = input("Inserisci saldo : ")

database.execute(("INSERT INTO account(username,psw,iban,saldo) VALUES (?, ?, ?, ?)"), (username, psw, iban, saldo))
database.commit()
database.close()