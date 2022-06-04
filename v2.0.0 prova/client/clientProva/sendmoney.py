import tkinter as tk
from tkinter import messagebox
import clientProva
import home


def sendmoney(user):
    def invia():

        somma = float(text2.get("1.0", "end-1c"))
        ibanRicevente = text1.get("1.0", "end-1c")

        clientProva.send("sendmoney")
        clientProva.send(ibanRicevente)
        clientProva.send(str(somma))

        verifica = clientProva.receive("stringa")

        if verifica == "0":
            messagebox.showerror("Transazione", "La transazione è stata effettuata con successo")
            frame2.destroy()
            home.frame.destroy()
            home.home(user)
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
