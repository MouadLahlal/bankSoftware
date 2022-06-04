import sqlite3
import os

dr = f"{os.getcwd()}\database.db"

database = sqlite3.connect(dr)
database.execute("CREATE TABLE account(id INTEGER PRIMARY KEY AUTOINCREMENT,username text,psw text,iban text,saldo money);")
database.commit()
database.close()