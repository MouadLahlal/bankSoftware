import tkinter as tk
import sqlite3
import re
from tkinter import messagebox
import home
import login
from datetime import datetime
import os

dr = f"{os.getcwd()}\database.db"

def sendmoney():
    database = sqlite3.connect(dr)
    def invia():
        global saldoAttuale
        somma = float(text2.get("1.0", "end-1c"))
        ibanRicevente = text1.get("1.0", "end-1c")
        if(saldoAttuale>=somma):
            saldoAttuale = saldoAttuale - somma - 0.5

            database.execute("UPDATE account SET saldo=? WHERE username=?", (saldoAttuale, login.username,))
            database.commit()
            
            dati = database.execute("SELECT saldo FROM account WHERE iban=?", (ibanRicevente,))
            y=""
            for x in dati:
                y = y + str(x)
            x = y.replace(",", "")
            re.split('( |)',x)
            x = x.replace("(","")
            x = x.replace(")","")
            saldoAttuale = float(x)
            saldoAttuale = saldoAttuale + float(somma)
            
            database.execute("UPDATE account SET saldo=? WHERE iban=?", (saldoAttuale, ibanRicevente,))
            database.commit()

            dati = database.execute("SELECT saldo FROM account WHERE iban=?", ("666",))
            y=""
            for x in dati:
                y = y + str(x)
            x = y.replace(",", "")
            re.split('( |)',x)
            x = x.replace("(","")
            x = x.replace(")","")
            saldoAttuale = float(x) + 0.5

            database.execute("UPDATE account SET saldo=? WHERE iban=?", (saldoAttuale, "666",))
            database.commit()

            dati = database.execute("SELECT username FROM account WHERE iban=?", (ibanRicevente,))
            y=""
            for x in dati:
                y = y + str(x)
            x = y.replace(",", "")
            re.split('( |)',x)
            x = x.replace("(","")
            x = x.replace(")","")
            x = x.replace("'","")

            date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            file = open(login.username+".txt", "a")
            file.write(f"{date},{ibanRicevente},-{somma}\n")
            file.close()
            file = open(x+".txt", "a")
            file.write(f"{date},{home.onlyIban},+{somma}\n")
            file.close()

            frame2.destroy()
            home.frame.destroy()
            home.home(login.username)
        else:
            messagebox.showerror("Errore", "Il saldo non è sufficiente per effettuare la transazione")
            frame2.destroy()

    frame2 = tk.Tk()
    frame2.title("INVIA DENARO")
    frame2.geometry("300x600")

    dati = database.execute("SELECT saldo FROM account WHERE username=?", (login.username,))
    y=""
    for x in dati:
        y = y + str(x)
    x = y.replace(",","")
    re.split('( |)',x)
    x = x.replace("(","")
    x = x.replace(")","")

    global saldoAttuale
    saldoAttuale = float(x)

    label1 = tk.Label(frame2, text="IBAN A CUI MANDARE DENARO : ")
    label2 = tk.Label(frame2, text="SOMMA DA INVIARE : ")
    text1 = tk.Text(frame2, height=1, width=30)
    text2 = tk.Text(frame2, height=1, width=30)
    button1 = tk.Button(frame2, text="INVIA", command=invia)

    label1.pack()
    text1.pack()
    label2.pack()
    text2.pack()
    button1.pack()