import sqlite3
import tkinter as tk
import re
import sendmoney
import login
import os

dr = f"{os.getcwd()}\database.db"

database = sqlite3.connect(dr)

def aggiornaSaldo():
    dati = database.execute("SELECT saldo FROM account WHERE iban=?", (onlyIban,))
    y=""
    for x in dati:
        y = y + str(x)
    x = y.replace(",","")
    re.split('( |)',x)
    x = x.replace("(","")
    x = x.replace(")","")
    saldo = f"Saldo : €  + {x}"
    label3.configure(text=saldo)

def home(username):
    global frame, label3, onlyIban
    frame = tk.Tk()
    frame.title("HOME")
    frame.geometry("600x300")
    
    dati = database.execute("SELECT iban FROM account WHERE username=?", (username,))
    y=""
    for x in dati:
        y = y + str(x)
    x = y.replace(",","")
    x = x.split("'")
    onlyIban = x[1]
    iban = f"IBAN :  {x[1]}"

    dati = database.execute("SELECT saldo FROM account WHERE username=?", (username,))
    y=""
    for x in dati:
        y = y + str(x)
    x = y.replace(",","")
    re.split('( |)',x)
    x = x.replace("(","")
    x = x.replace(")","")
    saldo = "Saldo : " + "€ " + x

    label = tk.Label(frame, text=f"Ciao {login.username}")
    label.config(font=('Segoe UI',11))
    label1 = tk.Label(frame, text="HOME")
    label2 = tk.Label(frame, text=iban)
    label3 = tk.Label(frame, text=saldo)
    button1 = tk.Button(frame, text="INVIA DENARO", command=sendmoney.sendmoney)
    button2 = tk.Button(frame, text="AGGIORNA", command=aggiornaSaldo)

    label.place(x=10, y=6)
    label1.place(x=10, y=30)
    label2.place(x=10, y=60)
    label3.place(x=10, y=90)
    button1.place(x=10, y=120)
    button2.place(x=120, y=120)

    frame.mainloop()