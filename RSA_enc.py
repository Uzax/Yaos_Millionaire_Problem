from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP


class RSA_ENC:
    PublicKey , PrivateKey = None , None

    def __init__(self):
        
        
        random_generator = Random.new().read
        key = RSA.generate(1024, random_generator) #generate pub and priv key
        self.PrivateKey = key
        self.PublicKey = key.publickey()

    # def get_public(self):
    #     return self.PublicKey

    

    def encrypt(self , message , public = None):
        if public is None :
            public = self.PublicKey
        
        message = str(message)
        message = str.encode(message)
        encryptor = PKCS1_OAEP.new(public)
        encrypted = encryptor.encrypt(message)
        return encrypted
    
    def decrypt(self , message):
        decryptor = PKCS1_OAEP.new(self.PrivateKey)
        decrypted = decryptor.decrypt(message)
        return decrypted.decode()






