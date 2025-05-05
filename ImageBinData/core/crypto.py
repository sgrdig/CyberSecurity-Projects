from cryptography.fernet import Fernet

def genererCle():
    return Fernet.generate_key()

def chiffrerMessage(message, cle):
    f = Fernet(cle)
    return f.encrypt(message.encode())

def dechiffrerMessage(messageChiffre, cle):
    f = Fernet(cle)
    return f.decrypt(messageChiffre).decode()
