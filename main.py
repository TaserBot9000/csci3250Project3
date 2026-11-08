#script goes here
import os as os
import binascii 
import numpy as np 
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes



def get_file_stats(filename):
    with open(filename, 'rb') as f:
        file_bytes = bytearray(f.read())
        data = np.frombuffer(file_bytes, np.uint8)
        return (np.mean(data), np.std(data))
    
def print_stats(filename):
    mean, std = get_file_stats(filename)

    print(f"File: {filename}")
    print(f"Mean: {mean}")
    print(f"Standard Deviation: {std}")

def encrypt_and_stats(filename):
    with open(filename, 'rb') as f:
        file_bytes = bytearray(f.read())
        key = os.urandom(32)
        iv = os.urandom(32)
        aes_cipher = Cipher(algorithms.AES(key), modes.GCM(iv))
        encryptor = aes_cipher.encryptor()
        ciphertext = encryptor.update(file_bytes) + encryptor.finalize()
        data = np.frombuffer(ciphertext, np.uint8)
        return(np.mean(data), np.std(data)) 
    
def print_encrypted(filename):
    mean, std = encrypt_and_stats(filename)

    print(f"Encrypted File: {filename}.encrypted")
    print(f"Mean: {mean}")
    print(f"Standard Deviation: {std}")

def main():
    files = {}
    for filetype in os.scandir('data'):
        if filetype.is_dir():
            files[filetype.name] = os.listdir(filetype.path)

    for filetype in files:
        for filename in files[filetype]:
            with open(f'data/{filetype}/{filename}', 'rb') as f:
                chunk = f.read(32)
                print(f'{binascii.hexlify(chunk)} -- {filename}')

            print_stats(f'data/{filetype}/{filename}')
            print_encrypted(f'data/{filetype}/{filename}')
