import tkinter as tk
import sqlite3
import re
from tkinter import messagebox
import home
from datetime import datetime
import User

user = User.user

def sendmoney():
    database = user.database
    def invia():
        user.getSaldo()

        global saldoAttuale
        somma = float(text2.get("1.0", "end-1c"))
        ibanRicevente = text1.get("1.0", "end-1c")

        if(int(user.saldo)>=somma):
            # aggiorno saldo utente mittente
            user.saldo = int(user.saldo) - somma - 0.5
            database.execute("UPDATE account SET saldo=? WHERE username=?", (user.saldo, user.username,))
            database.commit()
            
            # aggiorno saldo utente ricevente
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

            # aggiorno saldo conto della banca
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
            usernameRicevente = x.replace("'","")

            date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            file = open(user.username+".txt", "a")
            file.write(f"{date},{ibanRicevente},-{somma}\n")
            file.close()
            file = open(usernameRicevente+".txt", "a")
            file.write(f"{date},{user.iban},+{somma}\n")
            file.close()

            frame2.destroy()
            home.frame.destroy()
            home.home()
        else:
            messagebox.showerror("Errore", "Il saldo non è sufficiente per effettuare la transazione")
            frame2.destroy()
        
        database.close()

    frame2 = tk.Tk()
    frame2.title("INVIA DENARO")
    frame2.geometry("300x600")

    user.getSaldo()
    saldoAttuale = user.saldo

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