#script goes here
import os as os
import binascii 
import numpy as np 
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def get_file_stats(filename):
    with open(filename, 'rb') as f:                 #opens file to read binary
        file_bytes = bytearray(f.read())              #stores file content as bytes
        data = np.frombuffer(file_bytes, np.uint8)      #converts to numpy array
        return (np.mean(data), np.std(data))            #calculates mean and std dev
    
def print_stats(filename):
    mean, std = get_file_stats(filename)            #calls file stats function and assigns mean/std to return val

    print(f"File: {filename}")                      
    print(f"Mean: {mean}")                          
    print(f"Standard Deviation: {std}")             


def encrypt_and_stats(filename):
    with open(filename, 'rb') as f:                 #opens file to read binary
        file_bytes = bytearray(f.read())            #stores file content as bytes
        key = os.urandom(32)                        #generate random AES key
        iv = os.urandom(32)                         #generate random initialization
        aes_cipher = Cipher(algorithms.AES(key), modes.GCM(iv))     #AES cipher with GCM mode
        encryptor = aes_cipher.encryptor()          
        ciphertext = encryptor.update(file_bytes) + encryptor.finalize()    #encrypts file
        data = np.frombuffer(ciphertext, np.uint8)          #encrypted bytes to numpy array
        return(np.mean(data), np.std(data))         #encrypted mean and std dev
    
def print_encrypted(filename):
    mean, std = encrypt_and_stats(filename)         #calls file stats function and assigns mean/std to return val

    print(f"Encrypted File: {filename}.encrypted")
    print(f"Mean: {mean}")
    print(f"Standard Deviation: {std}")


def main():
    file_group = {                                  #dictionary to store different file groups
    'Documents' : [],
    'Images' : [],
    'PDF Files' : [],
    "Text Files" : [],
    "Spreadsheets" : []
    }


    for filetype in os.scandir('data'):             #scans data directory
        if filetype.is_dir():
            for filename in os.listdir(filetype.path):  #gets file names inside of dir
                ext = os.path.splitext(filename)[1]     #gets file extension of each file scanned


                if ext == '.docx':
                    file_group['Documents'].append((filetype.name, filename))      #the if block appends files to correct file group
                elif ext == '.jpg':
                 file_group['Images'].append((filetype.name, filename))
                elif ext == '.pdf':
                    file_group['PDF Files'].append((filetype.name, filename))
                elif ext == '.txt':
                    file_group['Text Files'].append((filetype.name, filename))
                elif ext == ".xlsx":
                    file_group['Spreadsheets'].append((filetype.name,filename))


            
    for name, files in file_group.items():                  #loop through dictionary for group name and file names
        print(f'============= {name} ===============')


        for filetype, filename in files:                    #loop for every file in group


            with open(f'data/{filetype}/{filename}', 'rb') as f:
                chunk = f.read(32)                              #read first 32 bytes
                print(f'{binascii.hexlify(chunk)} -- {filename}')   #converts to hexa and prints


            print_stats(f'data/{filetype}/{filename}')          
            print_encrypted(f'data/{filetype}/{filename}')      
            print()


if __name__ == '__main__':
    main()

