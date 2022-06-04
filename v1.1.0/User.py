import sqlite3
import re
import os

class UserObject:

    def __init__(self):
        self.directory = f"{os.getcwd()}\database.db"
        self.database = sqlite3.connect(self.directory)
        self.username = None
        self.psw = None
        self.iban = None
        self.saldo = None

    def getUsername(self, username):
        dati = self.database.execute("SELECT username FROM account WHERE username=?", (username,))
        y=""
        for x in dati:
            y = y + str(x)
        y = y.replace("(", "")
        y = y.replace(")", "")
        y = y.replace("'", "")
        y = y.replace(",", "")
        print(username)
        print(y)
        if username == y:
            self.username = y
    
    def getPassword(self, psw):
        dati = self.database.execute("SELECT psw FROM account WHERE username=?", (self.username,))
        y=""
        for x in dati:
            y = y + str(x)
        y = y.replace("(", "")
        y = y.replace(")", "")
        y = y.replace("'", "")
        y = y.replace(",", "")
        if psw == y:
            self.psw = y
    
    def getIban(self):
        dati = self.database.execute("SELECT iban FROM account WHERE username=?", (self.username,))
        y=""
        for x in dati:
            y = y + str(x)
        x = y.replace(",","")
        x = x.split("'")
        onlyIban = x[1]
        self.iban = onlyIban
    
    def getSaldo(self):
        dati = self.database.execute("SELECT saldo FROM account WHERE username=?", (self.username,))
        y=""
        for x in dati:
            y = y + str(x)
        x = y.replace(",","")
        re.split('( |)',x)
        x = x.replace("(","")
        x = x.replace(")","")
        self.saldo = x

def main():
    global user
    print("OGGETTO CREATO")
    user = UserObject()