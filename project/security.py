import base64
import hashlib
from Cryptodome.Cipher import AES as domeAES
from Cryptodome.Random import get_random_bytes
from Crypto import Random
from Crypto.Cipher import AES as cryptoAES

# Determine the block size of the cipher.
BLOCK_SIZE = 16

# Create the key needed for both encryption and decryption. This is done by both a known string and a random key created by the hashlib library.
key = 'Tullebukk123'.encode()
key2 = hashlib.sha256(key).digest()

print(key2)
# Define the function to encrypt the message using AES encryption. The known key and the random key are used to encrypt the string.
def encrypt(raw):
    BS = cryptoAES.block_size
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
    raw = base64.b64encode(pad(raw).encode('utf8'))
    iv = get_random_bytes(cryptoAES.block_size)
    cipher = cryptoAES.new(key= key2, mode= cryptoAES.MODE_CFB,iv= iv)
    a= base64.b64encode(iv + cipher.encrypt(raw))
    IV = Random.new().read(BLOCK_SIZE)
    aes = domeAES.new(key2, domeAES.MODE_CFB, IV)
    b = base64.b64encode(IV + aes.encrypt(a))
    return b

# Define the function to decrypt the message using AES encryption. The known key and the random key are used to decrypt the string.
def decrypt(enc):
    passphrase = key2
    encrypted = base64.b64decode(enc)
    IV = encrypted[:BLOCK_SIZE]
    aes = domeAES.new(passphrase, domeAES.MODE_CFB, IV)
    enc = aes.decrypt(encrypted[BLOCK_SIZE:])
    unpad = lambda s: s[:-ord(s[-1:])]
    enc = base64.b64decode(enc)
    iv = enc[:cryptoAES.block_size]
    cipher = cryptoAES.new(key2, cryptoAES.MODE_CFB, iv)
    b=  unpad(base64.b64decode(cipher.decrypt(enc[cryptoAES.block_size:])).decode('utf8'))
    return b

