import tkinter as tk
import client, home
from tkinter import messagebox

def sendmoney():
    def invia():

        somma = float(text2.get("1.0", "end-1c"))
        ibanRicevente = text1.get("1.0", "end-1c")

        client.sendMsg(ibanRicevente)
        client.sendMsg(somma)

        verifica = client.riceviMsg()

        if verifica == "1":
            frame2.destroy()
            home.frame.destroy()
            home.home()
        else:
            messagebox.showerror("Errore", "Il saldo non è sufficiente per effettuare la transazione")
            frame2.destroy()


    frame2 = tk.Tk()
    frame2.title("INVIA DENARO")
    frame2.geometry("300x600")

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