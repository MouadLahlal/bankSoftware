import sqlite3
import tkinter as tk
from tkinter import messagebox
import home
import os

dr = f"{os.getcwd()}\database.db"

def login():
    global username
    def login(username, psw):
        y=""
        database = sqlite3.connect(dr)
        dati = database.execute("SELECT psw FROM account WHERE username=?", (username,))
        for x in dati:
            y = y + str(x)
        if psw in y:
            return True
        else:
            return False

    frame = tk.Tk()
    frame.geometry("400x300")
    frame.title("BANK")

    def cmd1():
        global verifica, username
        username = text1.get('1.0','end-1c')
        psw = text2.get('1.0','end-1c')
        verifica = login(username, psw)
        if(verifica):
            frame.destroy()
            home.home(username)
        else:
            messagebox.showerror("Errore", "Credenziali errate, riprova")

    label1 = tk.Label(frame, text="Inserisci username :")
    text1 = tk.Text(frame, height=1, width=30)
    label2 = tk.Label(frame, text="Inserisci password :")
    text2 = tk.Text(frame, height=1, width=30)
    button1 = tk.Button(frame, text="INVIA", command=cmd1)

    label1.place(x=10, y=10)
    text1.place(x=140, y=10)
    label2.place(x=10, y=50)
    text2.place(x=140, y=50)
    button1.place(x=170, y=90)

    frame.mainloop()