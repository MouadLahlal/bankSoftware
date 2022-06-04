import tkinter as tk
import client

def aggiornaSaldo(user):
    user = client.sendLogin(user.username, user.psw)
    label3.configure(text=f"Saldo : € {user.saldo}")

def home(user):
    global frame, label3
    frame = tk.Tk()
    frame.title("HOME")
    frame.geometry("600x300")

    label = tk.Label(frame, text=f"Ciao {user.username}")
    label.config(font=('Segoe UI',11))
    label1 = tk.Label(frame, text="HOME")
    label2 = tk.Label(frame, text=f"Iban : {user.iban}")
    label3 = tk.Label(frame, text=f"Saldo : € {user.saldo}")
    button1 = tk.Button(frame, text="INVIA DENARO")
    button2 = tk.Button(frame, text="AGGIORNA", command=lambda: aggiornaSaldo(user))

    label.place(x=10, y=6)
    label1.place(x=10, y=30)
    label2.place(x=10, y=60)
    label3.place(x=10, y=90)
    button1.place(x=10, y=120)
    button2.place(x=120, y=120)

    frame.mainloop()