class PublicUser:

    def __init__(self, username, psw, iban, saldo):
        self.username = username
        self.psw = psw
        self.iban = iban
        self.saldo = saldo
    
    def scheda(self):
        return f"SCHEDA \nUsername : {self.username} \nPassword : {self.psw} \nIban : {self.iban} \nSaldo : {self.saldo}"