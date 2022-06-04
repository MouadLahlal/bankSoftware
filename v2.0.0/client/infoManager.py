from cryptography.fernet import Fernet

class InfoManager:
    
    def __init__(self):
        self.key = self.load_key()
    
    def load_key(self):
        with open("key.key", 'rb') as f:
            return f.read()

    def encryptInfo(self, info):
        encrypted = Fernet(self.key).encrypt(info.encode())
        return encrypted
    
    def decryptInfo(self, info):
        decrypted = Fernet(self.key).decrypt(info).decode()
        return decrypted