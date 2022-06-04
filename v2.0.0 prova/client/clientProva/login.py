import tkinter as tk
from tkinter import messagebox
import clientProva
import home


def login():
    def login(username, psw):
        global user
        clientProva.send(username)
        clientProva.send(psw)
        user = clientProva.receive("oggetto")
        if user.username is not None:
            if user.psw is not None:
                logged = True
            else:
                logged = False
        else:
            logged = False
        return logged

    frame = tk.Tk()
    frame.geometry("400x300")
    frame.title("BANK")

    def cmd1():
        username = text1.get('1.0', 'end-1c')
        psw = text2.get('1.0', 'end-1c')
        verifica = login(username, psw)
        if verifica:
            frame.destroy()
            home.home(user)
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
